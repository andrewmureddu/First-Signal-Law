# Measurement Protocol for $\mu$ and $\theta_{\text{top}}$

**Status:** measurement protocol. Together these set the band's **upper** edge:
$R_{\max} = \min(\mu / \theta_{\text{top}},\, 1)$
([`viability_band.md`](viability_band.md) §3b). $\mu$ is the exponent with which the
mediator's integrating capacity grows with system scale; $\theta_{\text{top}}$ is the
exponent of integration cost in the variety being integrated.

All results are reproduced by
[`scripts/mu_estimator.py`](scripts/mu_estimator.py) (<1 s, stdlib only, fixed seeds).

---

## Summary

| Question | Answer |
|---|---|
| Is $\mu$ easier than $\gamma$? | **No — harder**, and for a worse reason |
| What goes wrong? | Throughput is **demand-limited**; it measures demand, not capacity |
| How bad is the naive estimator? | Bias **+0.20**, with a CI width of **0.000** — confidently wrong |
| Where does capacity information live? | The **delay–load** relationship, near saturation only |
| Data requirement | Peak utilisation **≥0.90**; below ~0.50 unusable |
| Is $\theta_{\text{top}}$ measurable? | **Yes, easily** — $\delta = R\,\theta_{\text{top}}$ exactly |

---

## 1. Correction: $\mu$ is harder than $\gamma$, not easier

[`gamma_protocol.md`](gamma_protocol.md) §7 predicted $\mu$ would be more tractable
than $\gamma$, on the grounds that "mediator throughput is usually observable by
design rather than by rare-event sampling." **That prediction was wrong**, and the
reason matters more than the error.

Throughput *is* easy to observe. But observed throughput is
$X = \min(\text{demand},\ \text{capacity})$, so whenever the mediator is not
saturated — which is the normal operating condition — **you are measuring demand.**
A capacity cannot be observed in a system that is never stressed.

Worse, this failure is silent. Compare the two protocols' behaviour on bad data:

| | bad data produces |
|---|---|
| $\gamma$ (naive count) | biased estimate, but a **wide interval** flags it |
| $\gamma$ (Chao1) | **wide interval** — honest |
| $\mu$ (throughput) | **tight interval around the wrong number** — silent |
| $\mu$ (delay-based) | **refusal** or wide interval — honest |

$\gamma$'s bad estimates announce themselves. $\mu$'s naive estimate does not.

---

## 2. The trap, quantified

Simulated truth: $\mu = 0.70$ (capacity), $\delta = 0.90$ (demand). Utilisation
therefore rises with scale as $C^{\delta - \mu} = C^{0.20}$ — the largest systems sit
closest to saturation, which is itself a useful structural fact.

| peak $\rho$ | refused | throughput slope [95% CI] | delay-based $\hat\mu$ [95% CI] |
|---|---|---|---|
| 0.10 | 88% | 0.900 [0.900, 0.900] | 0.811 [0.360, 1.149] |
| 0.30 | 49% | 0.900 [0.900, 0.900] | 0.729 [−0.014, 1.089] |
| 0.50 | 17% | 0.900 [0.900, 0.900] | 0.687 [0.246, 0.898] |
| 0.75 | 2% | 0.900 [0.900, 0.900] | 0.670 [0.378, 0.800] |
| 0.90 | 0% | 0.900 [0.900, 0.900] | 0.679 [0.503, 0.771] |
| 0.97 | 0% | 0.900 [0.900, 0.900] | 0.682 [0.518, 0.764] |

The throughput slope returns **0.900 at every utilisation, with a confidence
interval of zero width.** It is not noisy. It is precisely measuring the wrong
quantity, with a bias of **+0.20 that no amount of additional data removes.**

An analyst applying it would report $\hat\mu = 0.900 \pm 0.000$ and conclude the
mediator can integrate almost linearly — when the true capacity exponent is 0.70 and
the ceiling is therefore substantially lower than believed. **This is the single most
dangerous measurement error in the framework**, because every diagnostic that would
normally catch a bad estimate says the estimate is excellent.

---

## 3. The estimator: capacity from delay

Model the mediator's delay as

$$W = \frac{W_0}{1 - \Lambda/\kappa}$$

where $W_0$ is unloaded service time, $\Lambda$ offered load, $\kappa$ capacity. Note
this deliberately **separates $W_0$ from $\kappa$**. Under M/M/1 they are locked
together ($W_0 = 1/\kappa$) and capacity could be read straight off the unloaded
latency — but that is an artefact of assuming a single server. Any mediator with
parallelism breaks the link, and the separation is exactly what makes capacity hard
to see at low load.

Rearranging gives a linear form:

$$\frac{1}{W} = \frac{1}{W_0} - \frac{\Lambda}{W_0\,\kappa}$$

**Procedure.**

1. At each scale $C$, collect $(\Lambda, W)$ pairs across whatever load variation the
   system naturally exhibits (diurnal cycles, seasonal peaks) or can be driven to.
2. Regress $1/W$ on $\Lambda$. Then $\hat\kappa = -\text{intercept}/\text{slope}$.
3. **If the fitted slope is not negative, refuse.** The load signal has been swamped
   by noise and no capacity estimate is available.
4. Regress $\ln \hat\kappa$ on $\ln C$. The slope is $\hat\mu$.
5. Report peak observed utilisation $\rho$ alongside $\hat\mu$. It is to this protocol
   what coverage is to $\gamma$.

---

## 4. Acceptance criterion

| peak $\rho$ | $\hat\mu$ | bias | 95% CI width | refused | verdict |
|---|---|---|---|---|---|
| 0.10 | 0.811 | +0.111 | 0.789 | 88% | unusable (refuses) |
| 0.30 | 0.729 | +0.029 | 1.104 | 49% | unusable (refuses) |
| 0.50 | 0.687 | −0.013 | 0.651 | 17% | unusable (refuses) |
| 0.75 | 0.670 | −0.030 | 0.422 | 2% | order-of-magnitude only |
| 0.90 | 0.679 | −0.021 | 0.268 | 0% | usable, ±0.13 |
| 0.97 | 0.682 | −0.018 | 0.246 | 0% | usable, ±0.12 |

Capacity information lives in the **curvature of delay against load**, which is
negligible while the mediator is idle. Below ~0.50 peak utilisation the estimator
mostly refuses; above ~0.90 the bias collapses to −0.02 and **precision** becomes the
binding limit.

### What the data budget buys (at peak $\rho = 0.90$)

| load points | latency noise | $\hat\mu$ | 95% CI width |
|---|---|---|---|
| 12 | 0.12 | 0.679 | 0.268 |
| 30 | 0.12 | 0.694 | 0.149 |
| 100 | 0.12 | 0.700 | 0.082 |
| 30 | 0.05 | 0.699 | 0.057 |
| 100 | 0.05 | 0.700 | 0.033 |
| 100 | 0.02 | 0.700 | 0.013 |

Unlike $\gamma$, the limit here is **instrument precision, not rare events**. Latency
is cheap to measure densely, so the good budget is realistic — *provided the mediator
can be observed under load*. That proviso, not the sampling, is the real constraint.

---

## 5. $\theta_{\text{top}}$ comes free — from the estimator that failed

If variety $I = I_0 C^R$ and integration load $\Lambda = c\,I^{\theta_{\text{top}}}$,
then $\Lambda \propto C^{R\,\theta_{\text{top}}}$, so

$$\boxed{\delta = R \cdot \theta_{\text{top}}}$$

Verified exactly:

| $R$ | $\theta_{\text{top}}$ | predicted $R\theta$ | measured $\delta$ | $\hat\theta = \delta/R$ |
|---|---|---|---|---|
| 0.60 | 1.00 | 0.6000 | 0.6000 | 1.0000 |
| 0.60 | 1.50 | 0.9000 | 0.9000 | 1.5000 |
| 0.60 | 2.00 | 1.2000 | 1.2000 | 2.0000 |
| 0.85 | 1.00 | 0.8500 | 0.8500 | 1.0000 |
| 0.85 | 1.50 | 1.2750 | 1.2750 | 1.5000 |
| 0.40 | 2.00 | 0.8000 | 0.8000 | 2.0000 |

**The throughput regression is the right estimator for the wrong parameter.** Given an
independent estimate of $R$, it yields $\theta_{\text{top}}$ — and $\theta_{\text{top}}$
is what identifies mediation topology (1 ≈ hierarchical, 1.5 ≈ modular, 2 ≈
all-to-all). So one instrumented dataset delivers the whole ceiling:

- **delay vs load, per scale** → $\mu$
- **throughput vs scale** → $\delta$ → $\theta_{\text{top}} = \delta/R$

$$R_{\max} = \min\!\left(\frac{\mu}{\theta_{\text{top}}},\, 1\right) = \min\!\left(\frac{\mu R}{\delta},\, 1\right)$$

| $\mu$ | $\delta$ | $R$ | $\theta_{\text{top}}$ | $R_{\max}$ |
|---|---|---|---|---|
| 0.70 | 0.90 | 0.60 | 1.50 | 0.467 |
| 0.70 | 1.20 | 0.60 | 2.00 | 0.350 |
| 1.00 | 0.85 | 0.85 | 1.00 | 1.000 |
| 0.50 | 1.00 | 0.50 | 2.00 | 0.250 |

Consistency check: $R$ must lie below the $R_{\max}$ it implies. Rows where
$R > R_{\max}$ describe a system already past its dissolution ceiling — in the table
above, row 1 ($R = 0.60 > 0.467$) is such a case.

---

## 6. The structural consequence

**You cannot measure a capacity by observing an unstressed system.** Therefore the
band's upper edge is *intrinsically* harder to observe than its lower edge, and a
system far from its ceiling cannot locate it. Systems will tend to discover their
dissolution ceiling by reaching it.

This is not a defect of the protocol; it is a property of the quantity. And it has a
constructive corollary. What *is* observable throughout is utilisation $\rho$, which
grows as $C^{\delta - \mu}$. So the operational early warning is not a measurement of
$\mu$ but **the trend in $\rho$** — which parallels
[`viability_band.md`](viability_band.md) §1's finding that the derivative of $R$
matters more than its level. In both halves of the band, the rate of change is the
vital sign and the level is nearly uninformative.

It also explains the modularisation prediction of §3b. A system approaching its
ceiling must respond by restructuring mediation topology — but it cannot know $\mu$
at that point. **Rising delay is the only signal available before the ceiling is
reached**, which is presumably why real systems modularise in response to
coordination pain rather than to capacity planning.

---

## 7. Candidate data sources

| domain | mediator | load $\Lambda$ | delay $W$ | can it be stressed? |
|---|---|---|---|---|
| distributed systems | consensus / message layer | requests/s | p50 latency | yes — load testing is routine |
| organisations | management / review layer | decisions queued | time-to-decision | partially; peaks occur naturally |
| biology | circulatory / neural network | flow demand | transit time | yes, under exercise stress |
| markets | clearing / settlement | order volume | settlement latency | at volume spikes only |
| infrastructure | routing/control layer | throughput | queueing delay | yes |

The pattern: $\mu$ is measurable wherever the mediator can be pushed, either
deliberately or by natural peaks. **Over-provisioned mediators have unidentifiable
$\mu$** — which is worth stating plainly, because over-provisioning is precisely what
a well-run system does.

---

## 8. Limitations

1. **The delay model is an idealisation.** $W = W_0/(1-\rho)$ captures the
   utilisation blow-up common to queueing systems but assumes a single bottleneck
   and stationary arrivals. Real mediators have multiple stages, batching, and
   bursty input; those change the shape of the curve and hence $\hat\kappa$.
2. **No real data is fitted anywhere in this document.** Everything is simulation
   against a known ground truth, which validates the *estimator*, not any empirical
   value of $\mu$.
3. **$\theta_{\text{top}} = \delta/R$ inherits $R$'s error**, including the
   measure-dependence of $C$ flagged as blocking in
   [`empirical_review.md`](empirical_review.md) §1c. The identity is exact; the
   estimate is only as good as $\hat R$.
4. **The refusal rule is conservative.** Rejecting every non-negative fitted slope
   discards some usable low-utilisation data. A proper treatment would use a
   constrained fit with an interval that widens appropriately rather than a hard
   reject.
5. **Load and variety must be measured on commensurate units** for
   $\delta = R\theta_{\text{top}}$ to be applied — the same class of problem as
   pinning down $C$.

---

## Reproducing

```sh
python3 analysis/scripts/mu_estimator.py
```

Sections A–E of the output correspond to §2, §4, §5 and §6 above.
