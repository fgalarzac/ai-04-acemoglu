"""Simulate the alpha and AI-precision thresholds in AKO (2026).

This is a deterministic numerical illustration, not a proof of the paper's
global results. Run from the repository root with:

    python threshold_simulation/simulate_thresholds.py
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, replace
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.special import erf, expit


@dataclass(frozen=True)
class Parameters:
    alpha: float = 1.2
    tau_a: float = 0.0
    prior_precision: float = 0.5
    lambda_i: float = 1.0
    lambda_g: float = 1.0
    island_size: float = 1000.0
    drift_variance: float = 1.0
    delta_x: float = 1.0


def success_probability(precision):
    """Return G(q) = 2 Phi(sqrt(q)) - 1."""
    return erf(np.sqrt(np.asarray(precision) / 2.0))


def log_marginal_success(precision: float) -> float:
    """Return log g(q), evaluated this way for numerical stability."""
    if precision <= 0:
        raise ValueError("precision must be strictly positive")
    return -0.5 * (np.log(2.0 * np.pi) + np.log(precision) + precision)


def log_effort(public_precision: float, p: Parameters) -> float:
    """Solve the private first-order condition in log effort."""
    if public_precision == 0:
        return -np.inf
    if public_precision < 0 or p.alpha <= 1 or p.prior_precision <= 0:
        raise ValueError("require X >= 0, alpha > 1 and positive prior precision")

    private_baseline = p.prior_precision + p.tau_a
    log_scale = np.log(p.delta_x * p.lambda_i * success_probability(public_precision))
    upper = (log_scale + log_marginal_success(private_baseline)) / (p.alpha - 1.0)

    def residual(log_e: float) -> float:
        effort_level = np.exp(log_e)
        private_precision = private_baseline + p.lambda_i * effort_level
        return (
            log_scale
            + log_marginal_success(private_precision)
            - (p.alpha - 1.0) * log_e
        )

    lower = upper - 32.0
    while residual(lower) < 0:
        lower -= 32.0
    if abs(residual(upper)) < 1e-13:
        return upper
    return brentq(residual, lower, upper, xtol=1e-12, rtol=1e-13)


def effort(public_precision: float, p: Parameters) -> float:
    return float(np.exp(log_effort(public_precision, p)))


def transition(public_precision: float, p: Parameters) -> float:
    updated_precision = (
        public_precision
        + p.lambda_g * p.island_size * effort(public_precision, p)
    )
    return updated_precision / (1.0 + p.drift_variance * updated_precision)


def balance(public_precision: float, p: Parameters) -> float:
    """Stable residual with the same sign as F(X)-X for positive X."""
    d = p.drift_variance
    if not 0 < public_precision < 1.0 / d:
        raise ValueError("balance requires 0 < X < 1 / Sigma^2")
    return (
        np.log(p.lambda_g * p.island_size)
        + log_effort(public_precision, p)
        + np.log1p(-d * public_precision)
        - np.log(d)
        - 2.0 * np.log(public_precision)
    )


def balance_peak(p: Parameters) -> tuple[float, float]:
    """Find the global numerical maximum of the balance residual."""
    logit_grid = np.linspace(-65.0, 25.0, 500)
    states = expit(logit_grid) / p.drift_variance
    values = np.array([balance(x, p) for x in states])
    index = int(np.argmax(values))
    lo = logit_grid[max(0, index - 1)]
    hi = logit_grid[min(len(logit_grid) - 1, index + 1)]
    optimum = minimize_scalar(
        lambda z: -balance(expit(z) / p.drift_variance, p),
        bounds=(lo, hi),
        method="bounded",
        options={"xatol": 1e-13},
    )
    state = float(expit(optimum.x) / p.drift_variance)
    return state, float(-optimum.fun)


def critical_ai_precision(p: Parameters) -> tuple[float, float]:
    """Compute tau_A^c and its tangency state in the elastic regime."""
    if p.alpha >= 1.25:
        raise ValueError("tau_A^c calculation requires alpha - 1 < 1/4")
    if balance_peak(replace(p, tau_a=0.0))[1] <= 0:
        return 0.0, 0.0

    upper = 1.0
    while balance_peak(replace(p, tau_a=upper))[1] > 0:
        upper *= 2.0
    threshold = brentq(
        lambda tau: balance_peak(replace(p, tau_a=tau))[1],
        0.0,
        upper,
        xtol=1e-12,
        rtol=1e-12,
    )
    critical_state, _ = balance_peak(replace(p, tau_a=threshold))
    return float(threshold), critical_state


def positive_fixed_points(p: Parameters) -> list[float]:
    """Locate sign-changing positive fixed points; tangencies are added separately."""
    upper = (1.0 - 1e-10) / p.drift_variance
    states = np.unique(
        np.r_[np.geomspace(1e-24, upper, 900), np.linspace(1e-6, upper, 900)]
    )
    values = np.array([balance(x, p) for x in states])
    roots: list[float] = []
    for left, right, f_left, f_right in zip(
        states[:-1], states[1:], values[:-1], values[1:]
    ):
        if f_left * f_right < 0:
            root = float(
                brentq(lambda x: balance(x, p), left, right, xtol=1e-14, rtol=1e-12)
            )
            if not roots or abs(root - roots[-1]) > 1e-8:
                roots.append(root)
    return roots


def transition_slope(state: float, p: Parameters) -> float:
    step = min(1e-5, max(1e-8, state * 1e-5))
    left = max(0.0, state - step)
    right = min((1.0 - 1e-10) / p.drift_variance, state + step)
    return (transition(right, p) - transition(left, p)) / (right - left)


def simulate(initial_state: float, p: Parameters, periods: int) -> np.ndarray:
    values = np.empty(periods + 1)
    values[0] = initial_state
    for period in range(periods):
        values[period + 1] = transition(values[period], p)
    return values


def fixed_point_records(p: Parameters) -> list[dict[str, float | str]]:
    records = []
    for root in positive_fixed_points(p):
        slope = transition_slope(root, p)
        records.append(
            {
                "state": root,
                "slope": slope,
                "stability": "stable" if abs(slope) < 1.0 else "unstable",
            }
        )
    return records


def plot_case_grid(
    cases: list[Parameters],
    labels: list[str],
    initial_states: list[list[float]],
    output_path: Path,
    title: str,
    tangencies: list[float | None] | None = None,
    periods: int = 5000,
) -> None:
    tangencies = tangencies or [None] * len(cases)
    fig, axes = plt.subplots(2, len(cases), figsize=(13.2, 7.2), constrained_layout=True)
    colors = ["#D55E00", "#0072B2", "#009E73"]
    state_grid = np.linspace(0.0, 1.0, 500)

    for column, (p, label, starts, tangency) in enumerate(
        zip(cases, labels, initial_states, tangencies)
    ):
        map_axis = axes[0, column]
        time_axis = axes[1, column]
        map_axis.plot(state_grid, state_grid, "--", color="#8A8A8A", lw=1.1)
        map_axis.plot(
            state_grid,
            [transition(x, p) for x in state_grid],
            color="#243B53",
            lw=2.2,
        )
        for record in fixed_point_records(p):
            stable = record["stability"] == "stable"
            map_axis.plot(
                record["state"],
                record["state"],
                "o",
                ms=7,
                color="#243B53",
                markerfacecolor="#243B53" if stable else "white",
            )
        if tangency is not None:
            map_axis.plot(tangency, tangency, "D", color="#CC79A7", ms=7)

        for index, initial in enumerate(starts):
            values = simulate(initial, p, periods)
            time_axis.plot(
                np.arange(periods + 1),
                np.maximum(values, 1e-18),
                color=colors[index],
                lw=1.6,
                label=rf"$X_0={initial:.4g}$",
            )
        map_axis.set(
            title=label,
            xlabel=r"$X_t$",
            ylabel=r"$F(X_t)$",
            xlim=(0.0, 1.0),
            ylim=(0.0, 1.0),
        )
        map_axis.set_aspect("equal", adjustable="box")
        time_axis.set(
            xlabel="Cohorte t (escala log)",
            ylabel=r"$X_t$ (escala log)",
        )
        time_axis.set_xscale("symlog", linthresh=1.0)
        time_axis.set_yscale("log")
        time_axis.grid(alpha=0.18)
        time_axis.legend(frameon=False, fontsize=8)

    fig.suptitle(title, fontsize=14)
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def plot_bifurcations(
    baseline: Parameters, threshold: float, critical_state: float, output_path: Path
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8), constrained_layout=True)

    for alpha in np.linspace(1.15, 1.40, 101):
        p = replace(baseline, alpha=float(alpha), tau_a=0.0)
        for record in fixed_point_records(p):
            axes[0].plot(
                alpha,
                record["state"],
                ".",
                color="#0072B2" if record["stability"] == "stable" else "#D55E00",
                ms=4,
            )
    axes[0].axvline(1.25, color="#333333", ls="--", lw=1.2)
    axes[0].text(1.253, 0.06, r"$\alpha=1.25$", rotation=90, va="bottom")
    axes[0].set(
        title=r"Puntos fijos al variar $\alpha$ ($\tau_A=0$)",
        xlabel=r"$\alpha$",
        ylabel=r"Punto fijo positivo $\bar X$",
        xlim=(1.15, 1.40),
        ylim=(0.0, 1.0),
    )

    tau_grid = np.linspace(0.0, 1.3 * threshold, 101)
    elastic = replace(baseline, alpha=1.2)
    for tau in tau_grid:
        p = replace(elastic, tau_a=float(tau))
        for record in fixed_point_records(p):
            axes[1].plot(
                tau,
                record["state"],
                ".",
                color="#0072B2" if record["stability"] == "stable" else "#D55E00",
                ms=4,
            )
    axes[1].plot(threshold, critical_state, "D", color="#CC79A7", ms=6)
    axes[1].axvline(threshold, color="#333333", ls="--", lw=1.2)
    axes[1].set(
        title=r"Puntos fijos al variar $\tau_A$ ($\alpha=1.2$)",
        xlabel=r"$\tau_A$",
        ylabel=r"Punto fijo positivo $\bar X$",
        xlim=(0.0, 1.3 * threshold),
        ylim=(0.0, 0.7),
    )

    for axis in axes:
        axis.grid(alpha=0.18)
        axis.plot([], [], ".", color="#0072B2", label="estable")
        axis.plot([], [], ".", color="#D55E00", label="inestable")
        axis.legend(frameon=False)
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def validate(
    baseline: Parameters, threshold: float, critical_state: float
) -> dict[str, float | str]:
    max_foc_residual = 0.0
    for alpha in (1.20, 1.25, 1.30):
        for tau in (0.0, 0.75 * threshold, threshold, 1.25 * threshold):
            p = replace(baseline, alpha=alpha, tau_a=tau)
            assert transition(0.0, p) == 0.0
            states = np.geomspace(1e-12, 0.99, 80)
            transitions = np.array([transition(x, p) for x in states])
            assert np.all(np.diff(transitions) > 0)
            assert np.all((transitions > 0) & (transitions < 1.0))
            for state in states:
                log_e = log_effort(state, p)
                private_precision = p.prior_precision + p.lambda_i * np.exp(log_e) + tau
                residual = abs(
                    np.log(p.delta_x * p.lambda_i * success_probability(state))
                    + log_marginal_success(private_precision)
                    - (alpha - 1.0) * log_e
                )
                max_foc_residual = max(max_foc_residual, residual)

    elastic = replace(baseline, alpha=1.2)
    below = positive_fixed_points(replace(elastic, tau_a=0.75 * threshold))
    above = positive_fixed_points(replace(elastic, tau_a=1.25 * threshold))
    critical_gap = abs(
        transition(critical_state, replace(elastic, tau_a=threshold)) - critical_state
    )
    assert max_foc_residual < 1e-9
    assert len(below) == 2
    assert len(above) == 0
    assert critical_gap < 1e-8

    return {
        "max_log_foc_residual": max_foc_residual,
        "critical_fixed_point_gap": critical_gap,
        "checks": "FOC, zero corner, map monotonicity and bounds, root counts, and tangency passed",
    }


def case_record(p: Parameters, starts: list[float], periods: int) -> dict:
    return {
        "parameters": asdict(p),
        "positive_fixed_points": fixed_point_records(p),
        "initial_conditions": starts,
        "terminal_states": [float(simulate(x, p, periods)[-1]) for x in starts],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parent / "outputs",
        help="directory for figures and results.json",
    )
    parser.add_argument("--periods", type=int, default=5000)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )

    baseline = Parameters()
    threshold, critical_state = critical_ai_precision(baseline)

    alpha_cases = [replace(baseline, alpha=a, tau_a=0.0) for a in (1.20, 1.25, 1.30)]
    alpha_starts = [[0.02, 0.8] for _ in alpha_cases]
    plot_case_grid(
        alpha_cases,
        [
            r"$\alpha=1.20$ (debajo)",
            r"$\alpha=1.25$ (igualdad)",
            r"$\alpha=1.30$ (encima)",
        ],
        alpha_starts,
        args.out / "alpha_crossing.png",
        r"Dinámica al cruzar $\alpha-1=1/4$",
        periods=args.periods,
    )

    tau_multipliers = (0.75, 1.0, 1.25)
    tau_cases = [replace(baseline, tau_a=m * threshold) for m in tau_multipliers]
    tau_starts = [
        [0.02, 0.8],
        [0.02, critical_state, 0.8],
        [0.02, 0.8],
    ]
    plot_case_grid(
        tau_cases,
        [
            r"$\tau_A=0.75\tau_A^c$",
            r"$\tau_A=\tau_A^c$",
            r"$\tau_A=1.25\tau_A^c$",
        ],
        tau_starts,
        args.out / "tau_crossing.png",
        r"Dinámica al cruzar el umbral de colapso $\tau_A^c$ ($\alpha=1.20$)",
        tangencies=[None, critical_state, None],
        periods=args.periods,
    )

    plot_bifurcations(
        baseline, threshold, critical_state, args.out / "bifurcation_diagrams.png"
    )

    results = {
        "purpose": "Deterministic numerical illustration of the alpha and tau_A thresholds",
        "baseline": asdict(baseline),
        "periods": args.periods,
        "alpha_threshold": 1.25,
        "alpha_equality_qualification": (
            "The paper's strict cases do not classify alpha=1.25; this is a parameter-specific simulation."
        ),
        "alpha_cases": [
            case_record(p, starts, args.periods)
            for p, starts in zip(alpha_cases, alpha_starts)
        ],
        "tau_a_critical": threshold,
        "critical_state": critical_state,
        "tau_cases": [
            case_record(p, starts, args.periods)
            for p, starts in zip(tau_cases, tau_starts)
        ],
        "validation": validate(baseline, threshold, critical_state),
    }
    (args.out / "results.json").write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
