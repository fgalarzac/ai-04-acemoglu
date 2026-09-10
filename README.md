# Repository 1 — Aouad, Lykouris & Zhong (2026)

*Human-AI Productivity Paradoxes: Modeling the Interplay of Skill, Effort, and AI Assistance*
[arXiv:2605.11350](https://arxiv.org/abs/2605.11350) · [cs.GT]

> **This is the worked example** for *Artificial Intelligence and Economic
> Modeling* (UP 2026-II). It shows what a weekly repository looks like when it is
> done well. Yours does not have to be this long — see "What is required" below.

---

## What question the paper answers

When does AI assistance make a worker **less** productive?

The paper picks one mechanism and pushes it: AI is a **perfectly substitutable
input**. Skill $s$, effort $e$ and assistance $a$ enter production only through
their sum, $x = s + e + a$. Nothing else is going on — no learning, no
complementarity, no contracting. Everything that follows comes from that single
modelling choice plus a linear cost of effort.

## The agent's problem

$$\max_{e \ge 0}\; p(s+e+a) - \gamma e$$

with $p$ weakly increasing, concave and twice differentiable, $\gamma > 0$, and
one constraint that turns out to carry the whole result: $e \ge 0$.

## The main result, with all its conditions

Let $x^{*}$ be the **largest** maximiser of $p(x) - \gamma x$:

$$x^{*} = \max \arg\max_{x} \left[\, p(x) - \gamma x \,\right]$$

This requires a **regularity condition**, without which $x^{*}$ need not exist:

$$\limsup_{x \to \infty} \frac{p(x)}{x} < \gamma$$

**Proposition 2.1.** Under those conditions,

$$e^{*}(s,a) = \left(x^{*} - s - a\right)_{+}, \qquad
  p^{*}(s,a) = \max\left\{ p(x^{*}),\, p(s+a) \right\}$$

*Intuition in one sentence:* the agent has a single target level of total input,
tops it up with effort, and once skill plus AI already reach it he stops working.

Two things worth noticing about the proof. It is a **case split** — interior
versus corner — and contains **no differentiation at all**; and the largest-argmax
tie-break is not decoration, it is what makes $e^{*}$ well defined when
$p(x)-\gamma x$ has a flat maximum.

## Sections 3–5: stated, not derived

The three headline results — the deskilling paradox, the unreliability paradox
and skill polarisation — use machinery well beyond Section 2: a continuous-time
birth–death Markov chain and its steady state, Arrow–Pratt risk aversion applied
to a *production* function with IARA/DARA driving the sign, and Bayesian updating
over a binary signal. They are worth understanding; they are not worth trying to
reproduce in a week. See `extra/tutorial-alz-completo.pdf` for the full walk.

---

## What is in this repository

| File | What it is |
|---|---|
| `README.md` | This page |
| `prompts.md` | The full LLM conversation, unedited |
| `extensions.md` | Which assumptions could be relaxed, and which are dead ends |
| `hand/` | The derivation of Proposition 2.1, written out by hand |
| `presentation.tex` / `.pdf` | The 5-minute Beamer deck |
| `paper/` | The article itself |
| `extra/` | Above the floor: a full tutorial of the paper and two lecture decks |

## What is required

Only four things. The rest of this repository is above the floor.

1. **`README.md`** — one page: the question, the agent's problem, the main result
   **with all its conditions**.
2. **`prompts.md`** — your prompts and the answers, **raw**. Do not tidy them up:
   the value is in seeing where the model went wrong.
3. **`hand/`** — at least one photograph of something you derived by hand. Not the
   whole paper: the one step you did not believe until you did it yourself.
4. **`presentation.tex` / `.pdf`** — the 5-minute deck, source and compiled.

Deadline is **Tuesday 22:00**, work merged into `main` through a pull request,
and the repository URL posted as a comment on that week's issue.

## About `hand/`

`hand/prop-2-1-derivacion-a-mano.pdf` is three phone photos of a notebook page.
That is exactly the standard: crooked, with crossings-out, no transcription. What
it shows is the first-order condition and the interior-versus-corner split written
out step by step — the part I did not want to take on trust.

## About the LLM conversation

`prompts.md` is the export of the session that produced the tutorial in `extra/`.
Read it for what it gets wrong as much as for what it gets right. The episode
worth studying is on slide 4 of the presentation: asked for "the most natural
extension", the model confidently proposed relaxing the linear cost — which the
authors had already done in Appendix D. It took opening the appendix to find out.
