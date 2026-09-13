# Handwritten welfare derivation

`derivation.jpg` is the user's handwritten verification supporting slide 5 of
`presentation.tex`, titled "Where I did not trust the AI: welfare." It derives
the decomposition of the effect of AI precision on high-knowledge steady-state
welfare:

```text
d Ubar+ / d tau_A
  = Delta_X G(Xbar_h) g(Ybar_h)
    + g(Xbar_h)[Delta_G + Delta_X G(Ybar_h)] d Xbar_h / d tau_A.
```

The first term is the direct information gain. The second term is the indirect
knowledge loss because `d Xbar_h / d tau_A < 0`. The derivation must show that
the terms multiplying `d ebar_h / d tau_A` cancel by the private first-order
condition. This is the calculation behind the slide's verdict: more accurate AI
does not necessarily increase welfare, and an interior optimum is not
guaranteed.

## What to write by hand

1. Define `Ybar_h = sigma^(-2) + lambda_I ebar_h + tau_A`.
2. Write high-state welfare:
   `Ubar+ = Delta_G G(Xbar_h) + Delta_X G(Xbar_h)G(Ybar_h)
   - ebar_h^alpha/alpha`.
3. Differentiate the three terms with respect to `tau_A`, using
   `d Ybar_h/d tau_A = 1 + lambda_I d ebar_h/d tau_A`.
4. Collect all terms multiplying `d ebar_h/d tau_A`.
5. Apply the private first-order condition
   `ebar_h^(alpha-1) = Delta_X lambda_I G(Xbar_h)g(Ybar_h)`
   to cancel that bracket.
6. Box the remaining direct and indirect terms and state their signs.

The photograph is stored without image editing as `hand/derivation.jpg`. The
deck includes it on its final slide with a caption identifying the welfare
calculation.
