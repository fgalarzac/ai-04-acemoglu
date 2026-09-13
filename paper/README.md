# Sources and version audit

Acemoglu, D., Kong, D., & Ozdaglar, A. (2026), *AI, Human Cognition and Knowledge Collapse*, NBER WP 34910, [DOI](https://doi.org/10.3386/w34910). Unrefereed working paper. Retrieved September 10, 2026.

The course GitHub repository **does not version PDFs**. Its [download script](https://github.com/alexanderquispe/AI-Econ-Modeling/blob/main/papers/fetch.sh) obtains `07-acemoglu-kong-ozdaglar-2026-knowledge-collapse.pdf` from MIT. The course copy read here is that documented source, not a binary purportedly fetched from GitHub or an unverifiable instructor-local copy.

| Download | Version | SHA-256 |
|---|---|---|
| [MIT PDF](https://economics.mit.edu/sites/default/files/2026-05/AI%2C%20Human%20Cognition%20and%20Knowledge%20Collapse%2005-05-26.pdf) | May 5, 2026; 69 pages | `63e37f2af463422e587c9bd81cda3bb555404a6ad65763aca0f9bebb8e2d4ec6` |
| [NBER PDF](https://www.nber.org/system/files/working_papers/w34910/w34910.pdf) | February 2026 cover; alpha notation | `10fa85cc57d8c28fe14922d603b93b642f0eb1fb456233cfcdadea9de3a19f30` |

The PDFs differ. All 69 course-linked pages, including references and Appendices A–B, were read before authoring repository content. NBER was cross-checked for section numbering, the static problem, dynamic thresholds, welfare conditions, and Section 5. MIT adds exposition and uses $\varepsilon$; NBER uses $\alpha$. The costs agree exactly under $\alpha=1+1/\varepsilon$.

Both versions have this section numbering:

1. Introduction
2. Related Literature
3. Model: 3.1 Environment; 3.2 Belief Updates and Knowledge; 3.3 Definition of Equilibrium; 3.4 Substitutes and Complements; 3.5 Existence and Characterization of Equilibrium; 3.6 Steady-State Equilibria; 3.7 Unique Steady State Regime; 3.8 Multiple Steady States Regime and Knowledge Collapse.
4. Welfare: 4.1 Steady-State Expected Utility; 4.2 The Impact of General Knowledge; 4.3 The Effects of Agentic AI; 4.4 Asymptotics for $I\to+\infty$; 4.5 Information Design.
5. Extensions: 5.1 Community versus AI Aggregation; 5.2 Synthetic Data; 5.3 (Imperfect) Separability of Effort.
6. Conclusion.

**Issue correction:** §2 is not the static problem. In MIT, §3.3/equation (6) is on printed pp. 13–14; Observation 1 on pp. 14–15; optimization on pp. 15–16. NBER has earlier pagination but identical section numbers. No section-location disagreement triggers the user's stop condition.

**Internal qualification:** §4.1 and some policy discussion say collapse for $\tau_A\ge\tau_A^c$. Proposition 5(ii) uses $>$, and Appendix A.4 explicitly retains a positive tangency at equality if $\tau_A^c>0$. We follow the proposition and Appendix A.4. The equality $\varepsilon=4$ is also outside Lemma 2's strict cases. These are qualifications, not reproductions of dynamic proofs.

Source PDFs and extracted full text are local working materials excluded from the commit. `presentation.pdf` is our own tracked deliverable.
