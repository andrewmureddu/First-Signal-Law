# Analysis

Review and derivation notes on the First Signal Law. These are **secondary
documents** — they analyse the primary theory in [`../law.md`](../law.md) and
[`../axioms.md`](../axioms.md) rather than restating it, and they are critical in
places.

Every quantitative claim is reproduced by a script in [`scripts/`](scripts/).
Standard library Python only, no third-party dependencies. Run from the repository
root.

---

## Contents

### [`empirical_review.md`](empirical_review.md)
What the repository's own data says when recomputed from source.

- $\hat R \approx 0.854$ reproduces — but as an OLS chord, not the local derivative
  the law states; the local slope declines 0.931 → 0.697 and meets $R \ge 1$ nowhere
- the complexity axis $C$ is exactly linear in the sweep parameter, so the role
  structure never enters the estimator
- $\hat R$ is not invariant to the measure of $C$ (0.50 vs 0.80 for one scenario)
- the logistic survival law contradicts AX18: $p = 0$ is still rated a survivor
- the GR baselines are **correct** and match Kerr closed forms exactly
- the $r_b$ release shift is multiplicative, so the quoted absolute figure is the
  wrong statistic; two documents disagree on it by a factor of $1/0.3$
- the "Black Hole Law Grid" is *exactly* a plane to machine precision
- the quantum-circuit prediction is `nan` throughout, yet reported as "verified"

### [`viability_band.md`](viability_band.md)
A two-sided reformulation: endurance as a band rather than a floor.

$$\gamma \le R \le \min(\mu/\theta_{\text{top}},\, 1), \qquad C < C_{\text{coll}}(R), \qquad \tau_{\text{rot}} < \tau_{\text{damage}}$$

- $R < 1$ implies a bounded complexity budget, not death
- the floor is the environment's variety exponent $\gamma$ (Ashby); the Red Queen
  consequence *derives* the asymmetric stalemate
- the ceiling has a universal part (1, from finite-time singularity) and a
  relational part (mediator capacity and topology)
- AX20 turns out to *be* the ceiling; AX21 is the only detector for stalemate
- $R$ is provably blind to stalemate — four failure modes, not one

### [`gamma_protocol.md`](gamma_protocol.md)
How to actually measure $\gamma$, the environmental variety exponent that sets the
band's lower edge — the quantity flagged as least defended.

- the confound is **sample coverage**, not observation-effort scaling as first
  suspected; effort scaling only sets the *sign* of the bias
- **Chao1** is near-unbiased throughout (within 0.03) where the naive distinct-type
  count is off by up to +0.21; what degrades is precision, not accuracy
- rarefaction is *worse than the disease* (drove $\hat\gamma$ to 0.063), and Hill
  numbers at $q{=}1,2$ are not robust substitutes
- acceptance criterion tied to Turing-Good coverage, with the data quality each
  margin requires
- wide-margin tests are practical; the Red Queen clustering prediction needs
  coverage ~1.00

### [`mu_protocol.md`](mu_protocol.md)
How to measure $\mu$ and $\theta_{\text{top}}$, which set the band's upper edge.

- **corrects a prediction made in `gamma_protocol.md`**: $\mu$ is *harder* than
  $\gamma$, not easier
- a throughput regression measures **demand, not capacity** — bias +0.20 with a CI
  width of 0.000, a confidently wrong answer that no diagnostic catches
- capacity lives in the **delay-load** relationship and is only visible near
  saturation; below ~50% peak utilisation the estimator refuses
- $\delta = R\,\theta_{\text{top}}$ exactly, so the failed throughput regression
  yields $\theta_{\text{top}}$ for free — one dataset gives the whole ceiling
- structural consequence: a system far from its ceiling **cannot locate it**, so the
  early-warning signal is the trend in utilisation, not $\mu$

### [`prior_art.md`](prior_art.md)
$R$ is an **elasticity**, already formalised in at least six literatures:
economics (returns to scale), collapse studies (Tainter), cybernetics (Ashby, Van
Valen), information theory (MDL, Information Bottleneck, scaling laws), allometry
(Kleiber, Bettencourt & West), and resilience theory (Holling & Gunderson's
rigidity trap). Includes a minimum citation set and the empirical conflict those
measurements create for $R \ge 1$.

---

## Scripts

| script | reproduces |
|---|---|
| [`scripts/refit_R.py`](scripts/refit_R.py) | `empirical_review.md` §1 |
| [`scripts/logistic_structure.py`](scripts/logistic_structure.py) | `empirical_review.md` §2 |
| [`scripts/check_kerr.py`](scripts/check_kerr.py) | `empirical_review.md` §3 |
| [`scripts/check_grid_plane.py`](scripts/check_grid_plane.py) | `empirical_review.md` §4b |
| [`scripts/band_bounds.py`](scripts/band_bounds.py) | `viability_band.md` §1, 2, 3, 5 |
| [`scripts/cadence_blindness.py`](scripts/cadence_blindness.py) | `viability_band.md` §4b |
| [`scripts/gamma_estimator.py`](scripts/gamma_estimator.py) | `gamma_protocol.md` §2–5 |
| [`scripts/mu_estimator.py`](scripts/mu_estimator.py) | `mu_protocol.md` §2, 4, 5, 6 |

```sh
for s in analysis/scripts/*.py; do echo "== $s"; python3 "$s"; done
```

---

## Open items

All three band parameters now have protocols: $\gamma$ in
[`gamma_protocol.md`](gamma_protocol.md), $\mu$ and $\theta_{\text{top}}$ in
[`mu_protocol.md`](mu_protocol.md). None has been applied to real data — the
protocols are validated against simulated ground truth, which establishes the
estimators, not any empirical value.

The band's two edges turn out to have opposite observability. $\gamma$ is limited by
rare events but degrades honestly into a wide interval. $\mu$ is limited by whether
the mediator can be stressed at all, and its naive estimator fails *silently* — a
tight confidence interval around the wrong quantity. A system far from its
dissolution ceiling cannot measure where it is.

Blocking issue for the original criterion: **the definition and units of $C$**.
Until those are fixed, $\hat R$ can be moved across the threshold by choosing
units, so the criterion cannot falsify anything.
