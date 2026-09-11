# Run Notes

This folder records an incomplete Windows run of the AppliedModelingLib
paper-formalization workflow at project commit
`e952266be81e96bbeecea6af83d639af324a4438`.

- The repository audit protocol was validated before scope or status edits.
- The official NBER page and an arXiv search were checked; no arXiv version of
  this paper was found. The February 2026 NBER PDF is the canonical source.
- The source PDF was copied locally as `source-audited.pdf` and is ignored by
  the generated `.gitignore`. Text was extracted with `pdfminer` because the
  optional `pdftotext` utility is unavailable.
- The generated statement-spec path was attempted first. Its Lean validation
  failed because the Windows search path could not resolve the local
  `AppliedModelingLib` module. The supported empty-interface scaffold route was
  then used and completed.
- The workflow requires a context-isolated semantic reviewer. No independent
  reviewer was available in this execution context, so the source inventory,
  v11 statement judgment, intake freeze, and final adversarial review remain
  open.
- The partial Lean surface proves only deterministic existence and uniqueness
  of equation (7)'s recurrence after the effort response is fixed. It does not
  establish the paper's Perfect Bayesian equilibrium claim or any other named
  result.
- The required paper-scoped fast check completed with exit code 0. The separate
  exact proof-endpoint build also completed with exit code 0.

The exact required fast-check command and its output are retained in
`FAST_CHECK_RESULT.txt` after execution.
