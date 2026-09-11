import QX26AgenticDelegation.PaperInterface

/-!
# Proof Interface: AI, Human Cognition and Knowledge Collapse

This file contains exact-type proof endpoints for the transparent propositions
in `PaperInterface.lean`. It is not a human semantic-review surface: one source
claim is reviewed once, against its expanded `...Spec : Prop` declaration.
-/

namespace QX26AgenticDelegation

/-- Exact proof endpoint for the recurrence-only component of Proposition 1. -/
theorem paper_proposition1_dynamic_recurrence :
    paper_proposition1_dynamic_recurrenceSpec := by
  unfold paper_proposition1_dynamic_recurrenceSpec
  intro X₁ SigmaSq lambdaG aggregation tauA effort _ effort_nonnegative
  exact dynamicRecurrence_existsUnique X₁ SigmaSq lambdaG aggregation tauA
    effort effort_nonnegative

end QX26AgenticDelegation
