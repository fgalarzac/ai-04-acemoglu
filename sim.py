"""Numerical illustration of AKO (2026), Figures 1 and 2, not a new result.

Run: python sim.py --out figures
Only the private FOC is solved; no appendix proof is reproduced.
The source paper uses alpha (NBER) or epsilon=1/(alpha-1) (MIT May 5).
"""
from dataclasses import dataclass, asdict, replace
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.special import erf, expit
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


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
    delta_g: float = 0.0


def G(tau):
    """2 Phi(sqrt(tau))-1; erf avoids cancellation for tiny tau."""
    return erf(np.sqrt(np.asarray(tau) / 2))


def log_g(tau):
    if tau <= 0:
        raise ValueError("g requires strictly positive precision")
    return -0.5 * (np.log(2 * np.pi) + np.log(tau) + tau)


def g(tau):
    return np.exp(log_g(tau))


def log_effort(x, p):
    """Solve the FOC in log effort, preserving very small positive responses."""
    if x == 0:
        return -np.inf
    if x < 0 or p.alpha <= 1 or p.prior_precision <= 0:
        raise ValueError("Require X>=0, alpha>1 and positive prior precision")
    b = p.prior_precision + p.tau_a
    a = np.log(p.delta_x * p.lambda_i * G(x))
    upper = (a + log_g(b)) / (p.alpha - 1)

    def residual(z):
        return a + log_g(b + p.lambda_i * np.exp(z)) - (p.alpha - 1) * z

    lower = upper - 32.0
    while residual(lower) < 0:
        lower -= 32.0
    if abs(residual(upper)) < 1e-13:
        return upper
    return brentq(residual, lower, upper, xtol=1e-12, rtol=1e-13)


def effort(x, p):
    return np.exp(log_effort(x, p))


def F(x, p):
    u = x + p.lambda_g * p.island_size * effort(x, p)
    return u / (1 + p.drift_variance * u)


def balance(x, p):
    """Log ratio of new public precision to the flow needed to keep X fixed.

    Equivalent to sign(F(X)-X), but avoids subtracting nearly equal numbers.
    This is a numerical residual for root finding, not a dynamic proof.
    """
    d = p.drift_variance
    return (np.log(p.lambda_g * p.island_size) + log_effort(x, p)
            + np.log1p(-d * x) - np.log(d) - 2 * np.log(x))


def peak(p):
    # Search a dense grid before refining, so a local optimizer is not trusted alone.
    z = np.linspace(-65, 25, 450)
    vals = np.array([balance(expit(t) / p.drift_variance, p) for t in z])
    k = int(np.argmax(vals))
    lo, hi = z[max(0, k-1)], z[min(len(z)-1, k+1)]
    opt = minimize_scalar(lambda t: -balance(expit(t) / p.drift_variance, p),
                          bounds=(lo, hi), method="bounded")
    return expit(opt.x) / p.drift_variance, -opt.fun


def critical_precision(p):
    if p.alpha >= 1.25:
        raise ValueError("Complete-collapse threshold is computed only for epsilon>4")
    if peak(replace(p, tau_a=0))[1] <= 0:
        return 0.0
    hi = 1.0
    while peak(replace(p, tau_a=hi))[1] > 0:
        hi *= 2
    return brentq(lambda t: peak(replace(p, tau_a=t))[1], 0, hi, xtol=1e-11)


def fixed_points(p):
    xs = np.unique(np.r_[np.geomspace(1e-24, 0.99, 800),
                        np.linspace(1e-5, 1-1e-10, 800)]) / p.drift_variance
    bs = [balance(x, p) for x in xs]
    return [brentq(lambda t: balance(t, p), a, b, xtol=1e-25, rtol=1e-12)
            for a, b, va, vb in zip(xs[:-1], xs[1:], bs[:-1], bs[1:])
            if va * vb < 0]


def path(x0, p, periods):
    values = [x0]
    for _ in range(periods):
        values.append(F(values[-1], p))
    return np.array(values)


def plot_panels(params, starts, titles, filename, periods=3000):
    fig, axes = plt.subplots(2, len(params), figsize=(12, 6.1), constrained_layout=True)
    colors = ["#c45a36", "#008783"]
    for col, (p, initials, title) in enumerate(zip(params, starts, titles)):
        ax, timeax = axes[:, col]
        xs = np.linspace(0, 1.0, 420)
        ax.plot(xs, [F(x, p) for x in xs], color="#203550", lw=2, label="$F(X)$")
        ax.plot(xs, xs, color="#92989f", ls="--", lw=1, label=r"$45^\circ$")
        roots = fixed_points(p)
        for root in roots:
            slope = (F(root*1.00001, p)-F(root*0.99999, p))/(root*0.00002)
            ax.plot(root, root, "o", color="#203550", mfc="white" if slope>1 else "#203550")
        for j, initial in enumerate(initials):
            values = path(initial, p, periods)
            cx, cy = [initial], [0.0]
            for current, nxt in zip(values[:70], values[1:71]):
                cx.extend([current, nxt]); cy.extend([nxt, nxt])
            ax.plot(cx, cy, color=colors[j], lw=0.85, alpha=0.85)
            timeax.plot(np.arange(periods+1), values, color=colors[j],
                        label=f"$X_0={initial:g}$", lw=1.5)
        ax.set(title=title, xlabel="$X_t$", ylabel="$X_{t+1}$", xlim=(0,1), ylim=(0,1))
        ax.set_aspect("equal", adjustable="box")
        timeax.set(xlabel="Cohort t (log scale)", ylabel="$X_t$ (log scale)")
        timeax.set_xscale("symlog", linthresh=1)
        timeax.set_yscale("log")
        timeax.grid(alpha=0.15)
        timeax.legend(fontsize=8, frameon=False)
    axes[0,0].legend(fontsize=8, frameon=False, loc="upper left")
    fig.suptitle("Illustration of AKO (2026), Figures 1–2 · not a new result", fontsize=13)
    fig.savefig(filename, dpi=180)
    plt.close(fig)


def validate(p, tc):
    max_resid = 0.0
    for alpha in [1.2, 1.25, 1.4]:
        for tau in [0, tc*0.75, tc*1.25]:
            q = replace(p, alpha=alpha, tau_a=tau)
            assert F(0, q) == effort(0, q) == 0
            grid = np.geomspace(1e-12, 0.99, 60)
            fs = np.array([F(x, q) for x in grid])
            assert np.all(np.diff(fs)>0) and np.all((fs>0)&(fs<1/q.drift_variance))
            for x in grid:
                z = log_effort(x, q)
                err = abs(np.log(q.delta_x*q.lambda_i*G(x))
                          + log_g(q.prior_precision+tau+q.lambda_i*np.exp(z))
                          - (alpha-1)*z)
                max_resid = max(max_resid, err)
                assert effort(x, replace(q,tau_a=tau+0.05)) < np.exp(z)
    assert max_resid < 1e-9
    assert len(fixed_points(replace(p,alpha=1.4))) == 1
    assert len(fixed_points(replace(p,tau_a=tc*0.75))) == 2
    assert len(fixed_points(replace(p,tau_a=tc*1.25))) == 0
    return {"max_log_FOC_residual": max_resid,
            "critical_peak_residual": peak(replace(p,tau_a=tc))[1],
            "checks": "FOC, corner, map bounds and monotonicity, AI crowd-out, root counts passed"}


def slide_overview(p, tc, filename):
    """Larger labels and selected cases for projection; full cobwebs are separate."""
    with plt.rc_context({"font.size":11}):
        fig, axes = plt.subplots(2,2,figsize=(8.8,4.2),constrained_layout=True)
        cases = [[replace(p,alpha=1.4),p],
                 [replace(p,tau_a=.75*tc),replace(p,tau_a=1.25*tc)]]
        labels = [[r"$\alpha=1.4$",r"$\alpha=1.2$"],
                  [r"$\tau_A=0.75\tau_A^c$",r"$\tau_A=1.25\tau_A^c$"]]
        xs = np.linspace(0,1,250)
        for col in range(2):
            ax, tx = axes[:,col]
            ax.plot(xs,xs,'--',color='#aaaaaa',lw=.8)
            for q,label,color in zip(cases[col],labels[col],['#008783','#c45a36']):
                ax.plot(xs,[F(x,q) for x in xs],label=label,color=color,lw=1.5)
                for x0,style in [(0.02,'--'),(.8,'-')]:
                    vals=path(x0,q,3000)
                    tx.plot(np.arange(3001),vals,style,color=color,lw=1.3)
            ax.set(xlim=(0,1),ylim=(0,1),xlabel='$X_t$',ylabel='$F(X_t)$')
            ax.legend(fontsize=9,frameon=False,loc='lower right')
            tx.set_xscale('symlog',linthresh=1); tx.set_yscale('log')
            tx.set(xlabel='Cohort t',ylabel='$X_t$')
            tx.grid(alpha=.15)
        fig.savefig(filename,dpi=200)
        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path(__file__).parent / "figures")
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":10,
                         "axes.spines.top":False, "axes.spines.right":False})
    p = Parameters()
    tc = critical_precision(p)
    alpha_cases = [replace(p,alpha=a) for a in [1.4,1.25,1.2]]
    tau_cases = [replace(p,tau_a=t) for t in [0,tc*0.75,tc*1.25]]
    # Same positive starts in each panel make comparisons transparent.
    starts = [[0.02,0.8]]*3
    plot_panels(alpha_cases, starts,
                [rf"$\alpha={q.alpha:g},\ \epsilon={1/(q.alpha-1):g}$" for q in alpha_cases],
                args.out/"alpha_cobweb_paths.png")
    plot_panels(tau_cases, starts,
                [rf"$\tau_A={q.tau_a:.3f}$" for q in tau_cases],
                args.out/"ai_cobweb_paths.png")
    slide_overview(p, tc, args.out/"slide_overview.png")
    summary = {"purpose":"Illustration of AKO Figures 1 and 2; not a new result or proof",
               "baseline":asdict(p), "tau_a_critical":tc,
               "critical_x":peak(replace(p,tau_a=tc))[0],
               "initial_conditions":[0.02,0.8], "periods":3000,
               "alpha_cases":[{"alpha":q.alpha,"positive_fixed_points":fixed_points(q)} for q in alpha_cases],
               "tau_cases":[{"tau_a":q.tau_a,"positive_fixed_points":fixed_points(q),
                              "terminal_X":[path(x,q,3000)[-1] for x in starts[0]]} for q in tau_cases],
               "validation":validate(p,tc)}
    raw = json.dumps(summary,indent=2)
    (args.out/"results.json").write_text(raw+"\n",encoding="utf-8")
    print(raw)


if __name__ == "__main__":
    main()
