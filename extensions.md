# Extensions — what could be relaxed, and what is already taken

The paper names its own assumptions in a block just before §1.2, and lists
exactly three: **substitutability/additivity**, **linear cost**, and **myopic
users**. That block is the natural starting point, but it needs checking against
the appendices before anything is claimed to be open.

## Dead end: linear → convex cost

This is the first thing anyone suggests, including every LLM I asked. It is
**already done**. Appendix D is titled *"Extension to convex cost functions
(Remark 2.3)"* and redoes Sections 2, 3 and 4 under strictly convex $c(e)$, with
Propositions D.3 and D.6.

Proposing it as an extension is replication, and it is the clearest example in
this course of why the appendices have to be read before an idea is called new.

**But there is a gap inside the gap.** Appendix D covers §§2–4. It does **not**
cover §5. Convex cost applied to the skill-polarisation result is technically
untouched — a narrow opening, but a real one.

## Live: myopia

The agent maximises **short-term** utility at each state: he chooses effort to
maximise current output net of cost, ignoring that effort today changes skill
tomorrow. The paper is explicit that this is a maintained assumption, and it is
never relaxed anywhere — no discount factor, no forward-looking agent, nothing.

A **two-period agent** who internalises the skill transition is the most tractable
version: solve period 2 as the static problem already characterised, then period 1
with the continuation value attached. The question worth asking is whether the
deskilling result survives when the agent can see it coming.

## Harder: complementarity inside $p(\cdot)$

The obvious move — add an interaction term between $s$ and $a$ — is partly
pre-empted: §4.4 micro-founds AI unreliability as a negative interaction and §5.3
micro-founds AI literacy as a positive one. So an extension has to change the
**production primitive itself**, not bolt a term onto it. Harder to make
tractable, and easier to end up with a model whose results are assumed rather
than derived.

## How to tell a real extension from a fake one

Three questions, in order:

1. **Is it in the appendices?** Check before anything else. This is where most
   proposed extensions die.
2. **Does one equation change, or all of them?** If relaxing the assumption
   rewrites the whole model, it is a new paper, not an extension.
3. **Can you say what you expect to happen?** If you cannot state the expected
   direction of the result beforehand, you do not yet understand the mechanism
   well enough to relax it.
