import QX26AgenticDelegation.MainTheorems

/-!
# Paper Assumptions: AI, Human Cognition and Knowledge Collapse

This file is the only paper-local place for assumptions that are not derived in
Lean. Keep it small. Each declaration must be explicitly stated by the paper,
listed in `status.json` `review_surface.assumption_names`, and judged in
`audit/assumption_match_llm.json` as a true source/model assumption rather than a
proof convenience.

The audit discovers proposition-valued theorem premises from Lean's elaborated
claim manifests. Do not add `audit-premise` comments or duplicate a binder in a
sidecar to make it discoverable; instead, keep the proposition explicit in the
source-facing `Spec` and route any reusable paper assumption through this
module and `status.json`.

Start empty. Add a proposition here only after locating it as a literal source
antecedent. Never move an unproved lemma or target conclusion here merely to
make a statement skeleton compile.
-/

namespace QX26AgenticDelegation

/-- Assumption 1, PDF page 10. -/
def assumptionOneSpec (deltaI deltaX : ℝ) : Prop :=
  deltaI = 0 ∧ 0 < deltaX

/-- Assumption 2, PDF page 27. -/
def assumptionTwoSpec (sigmaInvVariance : ℝ) : Prop :=
  ∃ sqrtTwo : ℝ,
    0 ≤ sqrtTwo ∧ sqrtTwo * sqrtTwo = 2 ∧ sqrtTwo - 1 ≤ sigmaInvVariance

end QX26AgenticDelegation
