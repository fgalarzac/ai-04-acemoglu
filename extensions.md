# Extensions, checked against the paper

**PAPER** labels the authors' model/results; **DERIVATION** my algebra; **INTERPRETATION** an economic reading; **OPEN QUESTION** proposed work. Novelty means absent from this paper, not absent from the literature.

## Section 5 audit — PAPER

| Baseline restriction | §5.1 Community versus AI aggregation | §5.2 Synthetic data | §5.3 (Imperfect) separability |
|---|---|---|---|
| Fixed aggregation $I$ | $I_0+\exp(\eta\tau_A)$ | Retained | Retained |
| Only human effort creates new public input | Retained | Adds $\tau_{syn}$ | Retained for $\beta>0$; constant input at $\beta=0$ |
| Linear public-learning input | Retained | Human component retained | $\lambda_G\int e_i^\beta di$ |
| Assumption 1: $\Delta_I=0$ | Retained | Retained | Retained |
| Assumption 1: $\Delta_X>0$ | Retained | Retained | Retained |
| Monotone $f$, $\Delta_G+\Delta_I+\Delta_X=1$ | Retained | Retained | Retained |
| Cost $e^\alpha/\alpha$, $\alpha>1$ | Retained | Retained | Explicitly retained |
| Private precision $\lambda_Ie$; additive AI precision | Retained | Retained | Explicitly retained |

§5.1, Proposition 14: high-state knowledge vanishes at high AI precision if $\eta<\varepsilon/2$. This does not mean aggregation never helps. §5.2, Proposition 15: finite positive synthetic precision gives positive least and greatest steady states and comparative statics, not the baseline exact root count. Strict zero collapse is removed. §5.3, Proposition 16: the local boundary becomes $\varepsilon\beta=4$ for $\beta>0$. It changes the public-learning technology, **not production complementarity**. Despite the introduction's allocation language, the formal model retains one chosen effort and exogenous $\beta$.

**The production restriction never relaxed is that context-specific knowledge is useless alone, $\Delta_I=0$.** Assumption 1, all three §5 models, and their Appendix B proofs retain it in both versions. Strict complementarity $\Delta_X>0$ and the power cost also remain. Thus there is no literal “only one assumption left unchanged” conclusion. The course-suggested $\Delta_I>0$ extension is indeed untouched, as verified against the equations.

## 1. Standalone value of context-specific knowledge

**OPEN QUESTION.** Set $0<\Delta_I<1$, keep $\Delta_X>0$, and adjust $\Delta_G\ge0$ to preserve normalization. Which positive low-knowledge traps and welfare losses persist?

**DERIVATION (static only).** Utility gains $\Delta_IG(Y)$ and the FOC becomes

$$e^{\alpha-1}=\lambda_I[\Delta_I+\Delta_XG(X)]g(Y).$$

For finite AI precision and positive prior precision, marginal benefit at $(X,e)=(0,0)$ is positive. Thus $e(0,\tau_A)>0$ and $F(0)>0$: exact zero collapse disappears. Interior public complementarity persists; AI still substitutes because $U_{e\tau_A}=\lambda_I[\Delta_I+\Delta_XG(X)]g'(Y)<0$. **INTERPRETATION:** no exact zero collapse does not imply no crowd-out. **OPEN QUESTION:** the global root structure needs new analysis.

**Overlap check.** §5.2 also prevents zero collapse, but via an exogenous public signal. This proposal changes private production payoffs and effort at zero public precision. §§5.1 and 5.3 do neither.

## 2. Nonconstant effort elasticity

**OPEN QUESTION.** Use $c(e)=e^\alpha/\alpha+\kappa e^\gamma/\gamma$, with $\kappa>0$ and $\gamma>\alpha>1$. Does the global root structure survive varying effort elasticity?

**DERIVATION (static only).** The FOC becomes $\Delta_X\lambda_IG(X)g(Y)=e^{\alpha-1}+\kappa e^{\gamma-1}$ and retains a unique private optimum. **INTERPRETATION:** the lower power controls very low effort, while the added term changes effort away from zero. **OPEN QUESTION:** global uniqueness or the exact two-positive-root bound is not established here.

**Overlap check.** §5.3 changes public learning to $e^\beta$ while explicitly keeping the power cost. §§5.1–5.2 keep costs too. Simply making public learning nonlinear is already covered and is not proposed as new.

## 3. Reward public contributions instead of garbling advice

**OPEN QUESTION.** Add an observable-contribution payment $s\lambda_Ge$ funded with a specified tax or budget. Compare optimal rewards with §4.5's precision caps, accounting for fiscal cost and verification constraints.

**DERIVATION (static only).** Perfectly observable contributions add $s\lambda_G$ to marginal benefit. **INTERPRETATION:** rewards address the public spillover while retaining advice; this is not a proved welfare improvement after financing costs. **OPEN QUESTION:** design and solve the budget and information constraints.

**Overlap check.** §4.5 already studies Gaussian garbling and a two-phase policy among eventually constant policies, under long-run average welfare and a recoverable initial condition. §§5.1–5.3 change technologies rather than contribution payments. This proposal is distinct, while building on the authors' externality diagnosis.
