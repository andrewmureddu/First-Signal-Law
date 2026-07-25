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

```sh
for s in analysis/scripts/*.py; do echo "== $s"; python3 "$s"; done
```

---

## Open items

The framework's edges are **unmeasured**. Nothing in this repository estimates
$\gamma$ (environmental variety exponent), $\mu$ (mediator capacity exponent), or
$\theta_{\text{top}}$ (mediation topology). The deliverable is three estimators,
not a universal constant — and $\gamma$ is the least defended of the three.

Blocking issue for the original criterion: **the definition and units of $C$**.
Until those are fixed, $\hat R$ can be moved across the threshold by choosing
units, so the criterion cannot falsify anything.
