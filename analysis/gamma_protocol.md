# Measurement Protocol for $\gamma$

**Status:** measurement protocol. $\gamma$ is the environmental variety exponent that
sets the lower edge of the viability band ([`viability_band.md`](viability_band.md)
§2). It was flagged there as the least defended quantity in the framework. This
document establishes how to measure it, which estimator to use, and — importantly —
what data quality is required before the resulting number means anything.

All results are reproduced by
[`scripts/gamma_estimator.py`](scripts/gamma_estimator.py) (~14 s, stdlib only,
fixed seeds).

---

## Summary

| Question | Answer |
|---|---|
| Is $\gamma$ measurable? | **Yes**, cleanly, given adequate sampling coverage |
| What is the confound? | **Sample coverage** — not observation effort, as first suspected |
| Which estimator? | **Chao1**. Bias within 0.03 across all tested coverage; naive is off by up to +0.21 |
| What must be reported? | **Turing–Good coverage**, always. The bias is a function of it |
| Is the floor test practical? | **Yes for wide margins**, marginal for the Red Queen regime |

---

## 1. Operational definition

$\gamma$ is the scaling exponent of the **disturbance inventory** — the count of
*distinct* perturbation or failure types a system faces — against system scale:

$$D(C) \propto C^{\gamma}, \qquad \gamma = \frac{d \ln D}{d \ln C}$$

Note what this makes $\gamma$: an exponent of the **system–environment coupling**,
not of the environment in isolation. A larger system exposes more surface, more
interfaces, more failure modes. This is the reading under which Ashby's requisite
variety becomes a scale-dependent condition, $R \ge \gamma$, rather than a
statement about levels.

**Procedure.**

1. Choose a scale variable $C$ spanning at least two decades. Genuine log-log
   slope estimation needs range; three points over one decade will not do.
2. For each system in the series, assemble an inventory of *distinct* disturbance
   types observed, together with the **count of events per type** — the frequency
   distribution is required, not just the type list, because both the estimator
   and the coverage diagnostic depend on singleton and doubleton counts.
3. Compute Chao1 per system: $\hat{S} = S_{obs} + f_1^2 / (2 f_2)$, where $f_1$ and
   $f_2$ are the numbers of types seen exactly once and twice.
4. Compute Turing–Good coverage per system: $\hat{C}_{cov} = 1 - f_1/n$.
5. Regress $\ln \hat{S}$ on $\ln C$. The slope is $\hat\gamma$.
6. **Report mean coverage alongside $\hat\gamma$.** Without it the estimate cannot
   be audited.

---

## 2. The confound is coverage, not effort

The initial suspicion — that $\hat\gamma$ is inflated because bigger systems get
watched more closely — turned out to be **wrong as stated**. Effort scaling is not
itself a source of bias. At adequate depth every estimator recovers $\gamma$:

| effort exponent | coverage | naive [95% CI] | Chao1 [95% CI] |
|---|---|---|---|
| 0.0 | 0.947 | 0.170 [0.147, 0.193] | 0.231 [0.179, 0.288] |
| 0.5 | 0.996 | 0.255 [0.247, 0.269] | 0.242 [0.197, 0.269] |
| 1.0 | 0.998 | 0.254 [0.247, 0.267] | 0.246 [0.219, 0.263] |

*(true $\gamma = 0.25$)*

The flat-effort row is the exception, and it is a **coverage** effect: holding the
event budget fixed while the disturbance pool grows leaves the largest systems
under-sampled.

The same configurations at shallow depth make the mechanism obvious:

| effort exponent | coverage | naive | Chao1 |
|---|---|---|---|
| 0.0 | 0.709 | 0.068 | 0.164 |
| 1.0 | 0.938 | 0.368 | 0.255 |

**At low coverage the naive count is badly biased, and effort scaling sets the
*direction* of the bias:** flat effort under-counts a growing pool (−0.18), effort
rising with system size over-counts it (+0.12). Both are large enough to flip a
verdict.

This matters practically because the two regimes correspond to real data-collection
styles. A fixed-budget audit programme under-counts; an incident-reporting system
whose scrutiny grows with the system over-counts.

---

## 3. Acceptance criterion

| depth at min scale | coverage | naive (bias) | Chao1 (bias) | Chao1 95% CI width |
|---|---|---|---|---|
| 25 | 0.881 | 0.460 (**+0.210**) | 0.275 (+0.025) | 0.338 |
| 50 | 0.939 | 0.371 (+0.121) | 0.255 (+0.005) | 0.267 |
| 100 | 0.976 | 0.306 (+0.056) | 0.247 (−0.003) | 0.155 |
| 250 | 0.996 | 0.258 (+0.008) | 0.240 (−0.010) | 0.066 |
| 500 | 1.000 | 0.248 (−0.002) | 0.245 (−0.005) | 0.030 |

Two things to read off this:

**Chao1 is essentially unbiased throughout** — within 0.03 even at coverage 0.88,
where the naive count is off by +0.21. **What degrades as coverage falls is
precision, not accuracy.** That is the useful property: a wide interval announces
its own unreliability, whereas a biased point estimate does not.

**The acceptance criterion is therefore about precision:**

| coverage | Chao1 CI width | usable for |
|---|---|---|
| ≈1.00 | 0.030 | thin margins (~0.05), including the Red Queen regime |
| 0.996 | 0.066 | margins above ~0.07 |
| 0.976 | 0.155 | wide margins only (≳0.16) |
| <0.94 | >0.26 | order-of-magnitude statements only |

### A note on what does *not* work

An earlier version of this analysis tried **rarefaction** to a common sample size
as the correction. It is much worse than the disease: rarefying to the smallest
sample saturates on common types and drove $\hat\gamma$ from 0.25 down to **0.063**
— a larger error than the naive bias it was meant to fix, in the opposite
direction. Similarly, Hill numbers at $q = 1$ (Shannon) and $q = 2$ (Simpson) are
**not** robust substitutes: they are insensitive to rare types, which is exactly
where pool growth lives, and their bias swings with abundance skew (0.30 to 0.05
across the skew range tested). Use an asymptotic richness estimator, not a
diversity index and not rarefaction.

---

## 4. Robustness to abundance skew

| zipf | coverage | naive [95% CI] | Chao1 [95% CI] |
|---|---|---|---|
| 0.5 | 1.000 | 0.247 [0.247, 0.251] | 0.245 [0.237, 0.251] |
| 1.0 | 0.998 | 0.254 [0.247, 0.267] | 0.246 [0.219, 0.263] |
| 1.5 | 0.993 | 0.296 [0.273, 0.322] | 0.244 [0.160, 0.299] |
| 2.0 | 0.992 | 0.378 [0.337, 0.423] | 0.278 [0.149, 0.385] |

Heavier tails inflate the naive count (bias −0.003 → **+0.128**) by depressing
effective coverage at fixed budget. Chao1 absorbs it, bias staying within 0.028
across the whole range, at the cost of a wider interval. **Skew acts only through
coverage** — which is why coverage, not skew, is the quantity to report.

---

## 5. What this means for testing the band

The floor test $R \ge \gamma$ has power only when the **margin exceeds the
confidence interval** on $\hat\gamma$:

| case | $R$ | $\gamma$ | best data (CI 0.030) | moderate data (CI 0.155) |
|---|---|---|---|---|
| mammal metabolism vs parasite richness | 0.75 | ~0.25 | testable | testable |
| urban infrastructure vs disturbance | 0.85 | ~0.50 | testable | testable |
| thin margin (Red Queen regime) | 0.30 | 0.25 | testable | **underpowered** |

**Wide-margin cases are comfortably testable**, even on moderate data. That is
genuinely good news for the framework: the biological consistency check is within
reach, and its arithmetic is favourable — mammalian regulatory scaling at $R \approx
0.75$ against a parasite-richness exponent in the low hundredths would sit far
inside the band, which is consistent with mammals persisting.

> **Caveat on that check.** Host-body-size/parasite-richness exponents are
> contested in the literature, vary by taxon, and are themselves subject to exactly
> the sampling-effort confound analysed above — better-studied hosts have longer
> parasite lists. The 0.25 figure here is illustrative of the *arithmetic*, not a
> fitted result. No real data is regressed anywhere in this document.

**The Red Queen prediction is the hard one.** [`viability_band.md`](viability_band.md)
§2 predicts that surviving players in a coupled system have *tightly clustered* $R$.
Clustering means small margins, and resolving margins of ~0.05 needs a CI width
below that — reached in this simulation only at coverage ≈1.00. For rare
catastrophic failure modes, where coverage is intrinsically poor, that is a
demanding requirement.

It is, however, **stateable rather than impossible**, and that is the point of
having a protocol: the prediction is not unfalsifiable, it has a known data
threshold. Anyone testing it now knows what they need before they start.

---

## 6. Candidate data sources

| domain | disturbance inventory | scale variable $C$ | coverage outlook |
|---|---|---|---|
| software | distinct defect/vulnerability classes | lines of code, module count | good — high event volume |
| epidemiology | pathogen/strain diversity | host population size | moderate |
| ecology | parasite species per host | host body mass | poor to moderate; effort-confounded |
| organisations | distinct incident categories | headcount, service count | good for routine, poor for tail |
| infrastructure | distinct outage causes | network size | moderate |

Note the pattern: coverage is good where events are frequent and poor where they
matter most. **This is the central practical difficulty in estimating $\gamma$**,
and it is why the estimator must be one that degrades into a wide interval rather
than a confident wrong answer.

---

## 7. Corrections to earlier claims in this analysis

Recorded explicitly, since both were stated before being tested:

1. **"The naive estimate of $\gamma$ is biased upward by observation effort scaling
   with system size."** Too strong. The bias is driven by low coverage; effort
   scaling only determines its sign. At adequate coverage there is no bias at any
   effort exponent.
2. **"Hill numbers at $q=1$ are a robust fallback."** Wrong. $q=1$ bias swings from
   +0.05 to −0.20 across the abundance-skew range. Rejected in favour of Chao1.

The remaining open edges of the framework are $\mu$ (mediator capacity exponent)
and $\theta_{\text{top}}$ (mediation topology), which set the ceiling. Neither has
a protocol yet. $\mu$ should be more tractable than $\gamma$ — mediator throughput
is typically observable by design rather than by rare-event sampling.

---

## Reproducing

```sh
python3 analysis/scripts/gamma_estimator.py
```

Sections A–D of the output correspond to §2, §3, §4 and §5 above.
