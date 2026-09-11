import Mathlib.Data.Real.Basic

/-!
# Paper-Facing Theorems: AI, Human Cognition and Knowledge Collapse

This file is the implementation theorem layer for the source paper. Keep
source-faithful definitions and theorem wrappers here, and expose only the
compact human-review subset in `PaperInterface.lean`.

During the statement-first phase, each exact paper-facing proposition lives in a
transparent `<name>Spec : Prop` declaration in `PaperInterface.lean`; the paired
theorem/lemma endpoint belongs in `ProofInterface.lean` and has exactly that
type. Add proof implementations here only after those specifications pass v11
raw-source-to-expanded-Spec review and recursive premise provenance audit. Before full closeout, the v11
realization audit independently binds pinned source atoms to the elaborated Spec
and accounts for the complete Lean closure; a proof hole or a declaration name
is never evidence for that correspondence.
-/

namespace QX26AgenticDelegation

/-- Equation (7)'s one-period update, indexing the paper's period one by zero. -/
noncomputable def dynamicTransition
    (SigmaSq lambdaG aggregation tauA : ℝ)
    (effort : ℝ → ℝ → ℝ) (state : ℝ × ℝ) : ℝ × ℝ :=
  let nextX := 1 / (SigmaSq + 1 / (state.1 + lambdaG * aggregation * state.2))
  (nextX, effort nextX tauA)

/-- The displayed recurrence component of Proposition 1. -/
def IsDynamicRecurrence
    (X₁ SigmaSq lambdaG aggregation tauA : ℝ)
    (effort : ℝ → ℝ → ℝ) (path : ℕ → ℝ × ℝ) : Prop :=
  path 0 = (X₁, effort X₁ tauA) ∧
  (∀ t, 0 ≤ (path t).2) ∧
  ∀ t, path (t + 1) = dynamicTransition SigmaSq lambdaG aggregation tauA effort (path t)

/-- A deterministic recurrence has a unique path once the initial state and
best-response function are fixed. -/
theorem dynamicRecurrence_existsUnique
    (X₁ SigmaSq lambdaG aggregation tauA : ℝ)
    (effort : ℝ → ℝ → ℝ)
    (effort_nonnegative : ∀ X, 0 ≤ effort X tauA) :
    ∃! path : ℕ → ℝ × ℝ,
      IsDynamicRecurrence X₁ SigmaSq lambdaG aggregation tauA effort path := by
  let initial : ℝ × ℝ := (X₁, effort X₁ tauA)
  let step : ℝ × ℝ → ℝ × ℝ :=
    dynamicTransition SigmaSq lambdaG aggregation tauA effort
  let path : ℕ → ℝ × ℝ := fun n => Nat.rec initial (fun _ state => step state) n
  have path_zero : path 0 = initial := by simp [path]
  have path_step : ∀ t, path (t + 1) = step (path t) := by
    intro t
    simp [path]
  refine ⟨path, ?_, ?_⟩
  · refine ⟨?_, ?_, ?_⟩
    · simpa [initial] using path_zero
    · intro t
      cases t with
      | zero => simpa [path, initial] using effort_nonnegative X₁
      | succ t =>
          simpa [path, step, dynamicTransition] using
            effort_nonnegative
              (1 / (SigmaSq + 1 /
                ((path t).1 + lambdaG * aggregation * (path t).2)))
    · intro t
      simpa [step] using path_step t
  · intro other other_path
    funext t
    induction t with
    | zero =>
        exact other_path.1.trans (by simpa [initial] using path_zero.symm)
    | succ t induction_hypothesis =>
        calc
          other (Nat.succ t) = step (other t) := by
            simpa only [Nat.succ_eq_add_one] using other_path.2.2 t
          _ = step (path t) := congrArg step induction_hypothesis
          _ = path (Nat.succ t) := by
            simpa only [Nat.succ_eq_add_one] using (path_step t).symm

end QX26AgenticDelegation
