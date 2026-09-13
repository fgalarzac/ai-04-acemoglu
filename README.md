# AI, Human Cognition and Knowledge Collapse

Acemoglu, Kong & Ozdaglar (2026), [NBER WP 34910](https://www.nber.org/papers/w34910). Course: AI-Econ-Modeling, [Issue #3](https://github.com/alexanderquispe/AI-Econ-Modeling/issues/3). [Repository](https://github.com/fgalarzac/ai-04-acemoglu).

**Version and correction.** I read the entire 69-page May 5 MIT PDF linked by the course script and cross-checked the current NBER PDF (September 10, 2026). **The issue's “Sections 2 and 3.4” is wrong about Section 2:** both versions have §2 Related Literature, §3 Model, the static payoff in §3.3, Observation 1 in §3.4, and optimization in §3.5. NBER uses $\alpha$; MIT uses $\varepsilon=1/(\alpha-1)$. See [source audit](paper/README.md).

**Question — PAPER.** Why can personalized AI help today's decisions while eroding tomorrow's general knowledge? Learning jointly produces private context information and a public contribution used by future cohorts. AI substitutes for the private motive to learn; individuals ignore the public spillover. As the common state changes, unreplenished knowledge loses relevance. Collapse means public precision $X_t\to0$, not erasure of every fact or loss of all personalized precision. Medical knowledge versus patient symptoms, or financial knowledge versus an investor's risk tolerance, illustrate the complementary inputs.

**Agent's problem — PAPER, in NBER notation.** Given $X_t$ and $\tau_A$, choose $e\ge0$:

$$\max_{e\ge0}\ f(0,0)+\Delta_GG(X_t)+\Delta_XG(X_t)G(Y)-\frac{e^\alpha}{\alpha},\qquad Y=\sigma^{-2}+\lambda_Ie+\tau_A.$$

Here $G(q)=2\Phi(\sqrt q)-1$, $g(q)=\phi(\sqrt q)/\sqrt q$. Under Assumption 1, $\Delta_I=0$, $\Delta_X>0$; monotone, normalized production implies $\Delta_G\ge0$ and $\Delta_G+\Delta_X=1$. Cost is convex with $\alpha>1$. For $X_t>0$ the unique optimum is interior:

$$e^{\alpha-1}=\Delta_X\lambda_IG(X_t)g(Y).$$

Observation 1: $U_{eX}=\Delta_X\lambda_Ig(X)g(Y)>0$ and $U_{e\tau_A}=\Delta_X\lambda_IG(X)g'(Y)<0$. **Boundary qualification — DERIVATION:** at $X=0$, $e=0$ and $U_{e\tau_A}=0$; $g(0)$ is singular, so the first formula is an interior statement.

**Dynamics and result — PAPER.** With atomistic, short-lived Bayesian agents, Gaussian independent signals, fixed $\lambda_I,\lambda_G,I,\Sigma^2>0$, finite $\tau_A\ge0$, positive prior precision $\sigma^{-2}$, and baseline public learning (no synthetic input, linear bundling):

$$X_t\to e_t=e(X_t,\tau_A)\to E_t=Ie_t\to X_{t+1}=F(X_t)=\frac{X_t+\lambda_GIe_t}{1+\Sigma^2(X_t+\lambda_GIe_t)}.$$

- $\alpha-1>1/4$ ($\varepsilon<4$): exactly two steady states, zero unstable and one positive stable $\bar X_h$; every $X_0>0$ converges to $\bar X_h$ (Lemma 2, Proposition 3).
- $0<\alpha-1<1/4$ ($\varepsilon>4$): zero stable. If $0\le\tau_A<\tau_A^c$, two positive states also exist: unstable $\bar X_m$ separates collapse and high-knowledge basins. If $\tau_A>\tau_A^c$, every initial state converges to zero (Proposition 5). $\tau_A^c$ may be zero. $X_0=\bar X_m$ stays there. Equality cases are outside these strict inequalities; see [notes](analysis.md).

**Welfare — PAPER.** Better AI has a positive direct information effect and a negative effect through $\bar X_h$. Under Assumption 2, $\sigma^{-2}\ge\sqrt2-1$, Propositions 10–11 give a single peak on the high branch (when it exists), possibly at $\tau_A=0$. A rising-then-falling profile requires the direct effect to dominate initially. Welfare is **not necessarily increasing**, and a positive interior optimum is **not guaranteed**.

**Work and verdict.** [Simulation](sim.py), [figures](figures/), and [five-minute deck](presentation.pdf) illustrate Figures 1–2, **not a new result**. A separate [threshold simulation](threshold_simulation/) compares the dynamics across $\alpha-1=1/4$ and $\tau_A=\tau_A^c$. [Analysis](analysis.md) explains the static algebra and welfare; [extensions](extensions.md) audits §5; [prompts](prompts.md) preserves the prompt and raw outputs. The production restriction $\Delta_I=0$ is never relaxed; neither are $\Delta_X>0$ or the power cost. The [handwritten-photo placeholder](hand/) awaits the user's photo and description.
