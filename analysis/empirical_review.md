# Empirical Review of the First Signal Law

**Status:** review notes, not primary theory. This document records what the
repository's own data and documents say when recomputed from source. Every number
below is reproduced by a script in [`scripts/`](scripts/); nothing here is quoted
from a figure caption.

**Provenance:** prepared as an analytical review of the FSL corpus (A. Mureddu).
Findings are critical in places; the constructive successor framework is in
[`viability_band.md`](viability_band.md).

---

## Summary

| Finding | Verdict |
|---|---|
| GR baselines in the prediction slate ($r_+$, $r_{ph}$, $r_{ISCO}$) | **correct**, match Kerr closed forms exactly |
| $\hat R \approx 0.854$ reproduces from the raw series | **confirmed** — it is an OLS chord, not the stated derivative |
| Local $d\ln I/d\ln C$ | declines monotonically 0.931 → 0.697; **no point meets $R \ge 1$** |
| Complexity axis $C$ | **exactly linear in the sweep parameter**; carries no independent information |
| $\hat R$ invariance to the measure of $C$ | **fails** — same scenario moves 0.50 → 0.80 |
| Logistic survival law vs AX18 | **contradicts it** — $p = 0$ still rated a survivor |
| "Black Hole Law Grid" $a_{\min}$ surface | **exactly a plane** to machine precision; no curvature, no black-hole physics |
| Quantum-circuit prediction $p^*_{meas}$ | **empty** — `nan` at all noise levels, yet reported as "verified" |
| GR headline slope | **two documents disagree by 1/0.3** |

---

## 1. The $\hat R$ estimator

`scripts/refit_R.py`, reading `Constrained__theta_2_0__-_lnI_vs_lnC.csv`.

The published value reproduces exactly:

| estimator | value |
|---|---|
| OLS slope of $\ln I$ on $\ln C$, all 10 points | **0.8543** (published: "R ≈ 0.854") |
| endpoint chord | 0.8535 |
| local derivative at final step | 0.6968 |

### 1a. It is a chord, not a derivative

The law states $R = d(\ln I)/d(\ln C) \ge 1$ — a *local* derivative. The reported
figure is a global regression slope, which averages the curve and flatters the
result. The local derivative is not constant:

| $s$ | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 | 1.0 |
|---|---|---|---|---|---|---|---|---|
| local $d\ln I/d\ln C$ | 0.931 | 0.900 | 0.870 | 0.842 | 0.815 | 0.767 | 0.744 | **0.697** |

Read as written, the criterion is met at **no point** in the series, and the trend
moves *away* from the threshold as scale grows. There is no regime in which the
system approaches $R \ge 1$.

### 1b. The complexity axis does no work

$C = 4105.674 \cdot s$ exactly, to machine precision. Therefore
$\ln C = \ln s + \text{const}$ and

$$\frac{d\ln I}{d\ln C} \equiv \frac{d\ln I}{d\ln s}$$

$\hat R$ measures only how concavely $I$ grows in the sweep parameter. The
$r, a, p$ role structure — the substance of the law — never enters the estimator.
This is why the role-zero ablation is nearly indistinguishable from the
constrained case (see §2b).

### 1c. $\hat R$ is not measure-invariant

| scenario | KL complexity | linear $C$ |
|---|---|---|
| Constrained (r,a,p>0; release ∝ roles) | 0.5013 | 0.7978 |
| Ablation: unbalanced release | 0.4712 | 0.7331 |
| Ablation: least role = 0 | 0.4960 | 0.7535 |

The same scenario moves by 60% on a change of complexity measure. **"$R \ge 1$"
is therefore a threshold on an arbitrary unit convention.** Until $C$'s definition
is pinned down, the criterion cannot falsify anything — it can be moved across
the threshold by choosing units. This is the single most important fix.

The scenario *ordering* (constrained > role-zero > unbalanced) is the one the
theory predicts, which is genuinely encouraging. But with three scenarios, no
error bars, and a ~1% spread on the KL measure, it is a weak ordinal signal.

---

## 2. The logistic survival law

$$P_C = \sigma(\alpha p + \beta S - \gamma D + \eta R_{net} + \delta u), \qquad
\text{survive iff } P_C \ge P^*$$

Variables are defined in `first_signal_law_arxiv.pdf` §2: $S$ = slack,
$D$ = dominance pressure, $R_{net}$ = release. They are **not** undefined; the
problems are all in the functional form. `scripts/logistic_structure.py`.

### 2a. The sigmoid is decision-theoretically inert

$\sigma$ is strictly monotone, so
$P_C \ge P^* \iff z \ge \operatorname{logit}(P^*)$. The survival criterion is a
**linear half-space**. The sigmoid never touches the verdict.

### 2b. It contradicts AX18

AX18 states a system endures **if and only if** the least endures — a conjunctive
gate. A linear model is compensatory:

| $p$ | $P_C$ | survives? |
|---|---|---|
| 1.0 | 0.976 | yes |
| 0.4 | 0.957 | yes |
| **0.0** | **0.937** | **yes** |

The least collapses completely and the system is still rated 94% likely to
survive, because slack and release compensate. **The formalism contradicts the
axiom it exists to express** — and this is precisely why the role-zero ablation
shows no effect.

### 2c. Restraint is unrepresentable

$\partial P_C / \partial R_{net} = \eta\,\sigma'(z) > 0$ everywhere:
$R_{net} = 10 \Rightarrow P_C = 0.9999998$; $R_{net} = 1000 \Rightarrow 1.000$.
Unbounded release is always optimal.

But the theory is about *proportion*: "the greatest restrains," "release in
proportion," "proportionality is the gravity of existence." Restraint means an
**interior optimum**; a linear term has none, its argmax is always at a boundary.
The same applies to $+\delta u$ against the stated noise floor, which the prose
describes as explicitly non-monotonic (brittle when too low, chaotic when too
high).

### 2d. The scale is unidentifiable

Scaling $(\alpha,\beta,\gamma,\eta,\delta)$ and $\operatorname{logit}(P^*)$ by
$\lambda > 0$ leaves every survival verdict unchanged while $P_C$ moves freely
(0.826 → 0.991 → 1.000 for $\lambda = 1, 3, 10$). Only coefficient *ratios* are
estimable: 6 parameters, 5 usable degrees of freedom. $P_C$ is not a calibrated
probability without a likelihood and a training set — so the seven-digit
$P_C = 0.9940855$ in `Fitted_milestone_times_and_states.csv` carries precision it
has not earned.

### 2e. AX20 and AX21 have no terms

Of the three roles only $p$ (the Least) appears; the Greatest enters solely as a
penalty $-\gamma D$; **alignment has no variable at all** (AX20). The equation
also has **no time index**, so cadence (AX21) cannot be expressed.

| Axiom | Status in the formalism |
|---|---|
| AX18 — the least endures (iff) | **contradicted** by linear compensation |
| AX19 — restraint at the greatest | **unrepresentable** in a monotone form |
| AX20 — the middle aligns | **no term** |
| AX21 — cadence | **no term, and no time index** |

All four axioms are either contradicted or absent.

### 2f. Minimal repair

$$z = \alpha \ln p + \beta S - \gamma D - \eta (R_{net} - R^*)^2 - \delta (u - u^*)^2$$

- $\alpha p \to \alpha \ln p$ drives $z \to -\infty$ as $p \to 0$, so $P_C \to 0$.
  AX18's "if and only if" now holds **by construction**: $p{=}1.0 \to 0.698$ ✅,
  $p{=}0.1 \to 0.188$ ❌, $p{=}0 \to 0$ ❌. One symbol.
- Quadratic penalties create genuine interior optima: release peaks at $R^*$ and
  *decays* beyond it (0.537 at optimum, 0.0002 at $R_{net}{=}3$, → 0 at 10).
  Restraint becomes expressible.
- For identifiability: fix $P^* = 0.5$, add an explicit intercept, normalise
  $\|(\alpha,\beta,\gamma,\eta,\delta)\| = 1$.

This also makes the law *more* falsifiable: $R^*$ and $u^*$ become estimable
interior optima whose existence is a real empirical claim that can fail.

---

## 3. The GR predictions

`scripts/check_kerr.py`, against `rebraided_prediction_slate.pdf` table A.

### 3a. The baselines are genuine

Recomputing the Kerr outer horizon, prograde photon sphere and prograde ISCO from
standard closed forms reproduces **every tabulated value to the printed
precision** at $a^* = 0.5, 0.9, 0.99$. This part of the work is sound and should
be said plainly.

### 3b. The $r_b$ shift is multiplicative, so the quoted summary is the wrong statistic

| $a^*$ | $r_b(0)$ | $r_b(0.3)$ | abs shift / unit $\zeta$ | frac shift / unit $\zeta$ | $r_b - r_{ISCO}$ |
|---|---|---|---|---|---|
| 0.50 | 2.409 | 2.051 | 1.193 | 0.495 | −1.824 |
| 0.90 | 1.943 | 1.686 | 0.857 | 0.441 | −0.378 |
| 0.99 | 1.611 | 1.402 | 0.697 | 0.432 | **+0.157** |

The quoted "0.916 M/$\zeta$" is a mean over a **1.71× spread**. Expressed
fractionally the spread collapses to 1.15× (≈0.456 per unit $\zeta$, near
constant). The defensible prediction is therefore:

> $r_b$ contracts **≈46% per unit $\zeta$**

— not a single absolute figure in $M$. This is a strictly stronger and cleaner
claim, and it is what the data actually supports.

Separately: $r_b$ **changes side relative to the ISCO** across this spin range
(inside at $a^* = 0.50$, outside at $a^* = 0.99$). If $r_b$ is a physical
endurance boundary, that sign flip needs an account, because it determines
whether the boundary is observationally shadowed.

### 3c. Two documents disagree by a factor of 1/0.3

- arXiv draft §3.1: "~0.3 M per unit $\zeta$"
- prediction slate: "0.916 M per unit $\zeta$"

The mean shift **per 0.3 $\zeta$** is 0.2747, which rounds to the arXiv's "~0.3",
and $0.9156 / 0.2747 = 3.333 = 1/0.3$ exactly. The arXiv figure is the per-0.3-$\zeta$
shift mislabelled as per-unit-$\zeta$ — **a units error in the abstract's headline
prediction**.

---

## 4. Two claims with no content behind them

### 4a. The quantum-circuit prediction is empty

`rebraided_prediction_slate.pdf` table B reports the critical release
$p^*_{meas}$ as `nan` at $p_{noise} = 0.06, 0.12, 0.20$, with the linear fit
printed as `p_meas* ≈ nan·p_noise + nan (N=4, depth=12)`.

The arXiv draft §3.2 states this prediction is "verified for 4-qubit depth-12
circuits" — **the exact configuration that produced `nan`**. One of the law's
three falsifiable pillars currently has no content, and a failed run has been
reported as a verification. This needs either a working simulation or removal of
the claim.

Also in the arXiv draft: the same placeholder figure ("Scientific Figure —
Unified Release Units", three straight lines) is reused for all three predictions
in §3.1–3.3, and its GR line slopes *upward* while the text predicts an *inward*
(decreasing) shift. Reference [4] reads "Placeholder for forthcoming
First-Signal Law simulations and preprints."

### 4b. The "Black Hole Law Grid" contains no black-hole physics

`scripts/check_grid_plane.py`, on `a_min_grid__mid-theta_slice_.csv` (546 cells).
Fitting an affine plane from three cells gives

$$a_{\min} = 1.0860 - 2.000\,r - 0.200\,x$$

with **maximum residual $2.53 \times 10^{-15}$** across the entire grid — machine
epsilon. The surface is *exactly* a plane. No metric is solved; the contour plot
renders a closed-form linear inequality.

Additionally $a_{\min}$ reaches **−0.234**. If $a$ is a non-negative alignment
weight, the plotted region extends past the model's own domain of validity.

---

## 5. What should change

**Blocking.** Pin down the definition and units of $C$. Until then $\hat R$ is
not measure-invariant and the threshold cannot falsify anything (§1c).

**High priority.**
1. Report $\hat R$ as a *local* derivative with its trend, not a global chord (§1a).
   The declining slope is the finding; the averaged level conceals it.
2. Adopt the $\ln p$ + quadratic-penalty repair so the formalism stops
   contradicting AX18 and can express AX19 (§2f).
3. Restate the GR prediction fractionally (§3b) and fix the 1/0.3 units error
   between the two documents (§3c).
4. Either produce a working $p^*_{meas}$ simulation or withdraw the "verified"
   claim (§4a).
5. Relabel the $a_{\min}$ grid as the linear constraint it is, and clip it to
   $a_{\min} \ge 0$ (§4b).

**Structural.** Give AX20 and AX21 terms, and add a time index. Both turn out to
be load-bearing: see [`viability_band.md`](viability_band.md), where alignment
capacity sets the upper edge of the viability band and cadence is the only
detector for one of the four failure modes.

---

## Reproducing

```sh
python3 analysis/scripts/refit_R.py            # section 1
python3 analysis/scripts/logistic_structure.py # section 2
python3 analysis/scripts/check_kerr.py         # section 3
python3 analysis/scripts/check_grid_plane.py   # section 4b
```

Standard library only; no third-party dependencies.
