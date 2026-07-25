# Prior Art for $R = d(\ln I)/d(\ln C)$

**Status:** literature mapping. The FSL endurance criterion is built on an object
that is already among the most-studied quantities in quantitative science, under
at least six different names. This document maps the correspondence so the theory
can cite its ancestors, position its actual novelty, and — importantly — inherit
their empirical results.

**Why this matters practically:** several of these literatures have *measured* the
quantity FSL posits, across many orders of magnitude, for decades. Those
measurements bear directly on whether the law's threshold points the right way.
See §7.

---

## 0. What the object is

$$R = \frac{d\ln I}{d\ln C} = \frac{C}{I}\cdot\frac{dI}{dC}$$

An **elasticity**. Equivalently a **log-log slope**, a **scaling exponent**, or a
**power-law index**. The condition $R \ge 1$ is a **marginal-returns threshold**.

Note on orientation: the repository's canonical form is $d(\ln I)/d(\ln C)$.
Inverting the ratio flips the threshold from $\ge 1$ to $\le 1$, so the direction
must be stated explicitly wherever the criterion appears.

---

## 1. Economics — elasticity and returns to scale

The oldest claim on this object.

- **Marshall (1890)**, *Principles of Economics* — elasticity as the log-log
  derivative. $R > 1$ is "elastic".
- **Returns to scale** in production theory: the output elasticity with respect to
  inputs *is* returns to scale. $R > 1$ increasing (IRS), $R = 1$ constant (CRS),
  $R < 1$ decreasing (DRS).
- **Cobb–Douglas** exponents sum to the returns to scale — which is the same
  logarithmic form as the $\ln p$ repair proposed in
  [`empirical_review.md`](empirical_review.md) §2f.
- **The law of diminishing marginal returns.** The monotone decline of local
  $d\ln I/d\ln C$ from 0.931 to 0.697 in the θ=2.0 series is textbook DRS.

**Correspondence:** "endurance requires $R \ge 1$" restates as *"the system must
exhibit non-decreasing returns to scale in information per unit constraint."*

---

## 2. Collapse studies — Tainter

- **Tainter, J. (1988)**, *The Collapse of Complex Societies.* Cambridge
  University Press.

Societies collapse when the **marginal return on added complexity** declines past
sustainability. Same variables (benefit vs complexity cost), same mechanism, same
*survival* framing, published 37 years before FSL. This is the closest match to
the law's central thesis and the citation the repository most conspicuously lacks.

Tainter also supplies the complexity budget derived in
[`viability_band.md`](viability_band.md) §1: with benefit $aC^R$ against upkeep
$\lambda C$, sub-unity $R$ implies a finite ceiling
$C_{\text{coll}} = (a/\lambda)^{1/(1-R)}$.

---

## 3. Cybernetics and control — the floor

- **Ashby, W. R. (1956)**, *An Introduction to Cybernetics* — the **Law of
  Requisite Variety**: *"only variety can destroy variety."* A regulator must
  possess at least as much variety as the disturbance it regulates.
- **Van Valen, L. (1973)**, "A New Evolutionary Law" — the **Red Queen**: in
  coevolution, continuous improvement is required merely to maintain position.
- **Reachability / controllability** in control theory. Rigidity is loss of
  reachable-set volume; Ashby gives the floor, over-constraint gives the ceiling.

**Correspondence:** Ashby yields $R_{\min} = \gamma$, the environment's variety
exponent ([`viability_band.md`](viability_band.md) §2). Van Valen yields the
mutual-pinning result that derives the asymmetric stalemate rather than assuming
it.

---

## 4. Information theory and learning theory — the tightest formal cousins

- **Rissanen, J. (1978)** — **Minimum Description Length**. A model component is
  worth adding iff information gain ≥ complexity cost: $\Delta I \ge \Delta C$ in
  bits. **This is $R \ge 1$ in differential form**, already proved and already
  operationalised.
- **Tishby, Pereira & Bialek (1999)** — **the Information Bottleneck**. The
  tradeoff curve between compression $I(X;T)$ and prediction $I(T;Y)$, whose slope
  is a Lagrange multiplier. The repository's **KL-divergence complexity measure is
  an IB-style compression term**, so the KL column of
  `KL-divergence_complexity_results.csv` is structurally an IB curve slope.
- **Vapnik & Chervonenkis** — VC dimension, sample complexity, structural risk
  minimisation. Generalisation requires information to grow at least as fast as
  capacity.
- **Kaplan et al. (2020)**; **Hoffmann et al. (2022)** — **neural scaling laws**.
  Loss-versus-compute log-log slopes: literally the same estimator, with
  well-developed practice on how to fit it and how not to.
- **Bennett, C. (1988)** — logical depth; **Kolmogorov complexity** more broadly,
  for the $I$-versus-$C$ growth relation.

**Correspondence:** MDL is the sharpest formal statement of the original
criterion. If FSL wants $R \ge 1$ as a *bit-accounting* claim, MDL already
provides it with proofs.

---

## 5. Biology and complex systems — allometric scaling

- **Kleiber, M. (1932)** — metabolic rate $\propto M^{3/4}$. An elasticity of
  **0.75**, stable across ~20 orders of magnitude of body mass for a century.
- **Rubner (1883)** — the competing surface-area exponent **2/3**.
- **West, Brown & Enquist (1997)** — derive 3/4 from space-filling fractal
  branching networks. Note that here the exponent is **forced by topology, not
  selected** — see §8.
- **Bettencourt & West (2007)**, "Growth, innovation, scaling, and the pace of
  life in cities", *PNAS* — urban infrastructure $\beta \approx 0.85$;
  socioeconomic output $\beta \approx 1.15$. Superlinear scaling implies
  **finite-time singularities** requiring periodic innovation resets.
- **Fractal / box-counting dimension**: $D = \lim d\ln N(\epsilon)/d\ln(1/\epsilon)$
  — the same log-log derivative structure.
- **Renormalisation group critical exponents**, where a threshold at a particular
  exponent value is a **marginality / relevance condition** on an operator.

**Correspondence:** Bettencourt & West supply the universal ceiling at 1
([`viability_band.md`](viability_band.md) §3a). Rubner's 2/3 and WBE's 3/4 are
reproduced as a *mediation-topology* distinction in §3b.

---

## 6. The rigidity ceiling — prior art for the second wall

The upper failure mode is equally well formalised, and one source names **both**
walls:

- **Holling, C. S. & Gunderson, L. (2002)**, *Panarchy.* Island Press. The
  **rigidity trap** (high connectedness, high capital, no flexibility — efficient
  and locked) versus the **poverty trap** (cannot accumulate; falls apart).
  Resilience lives between them. **This is the viability band, in ecology, with
  both failure modes named.**
- **Glass transition / ergodicity breaking.** A glass is dynamically arrested
  while locally still jiggling: *moving*, yet unable to explore configuration
  space. This is the physical archetype for "you can still be moving during a
  stalemate," and the reason activity is not evidence of viability.
- **Langton (1990); Kauffman (1993)** — the **edge of chaos**. The ordered regime
  is literally termed **frozen**; the chaotic regime cannot accumulate; adaptation
  occupies the boundary. Two-sided by construction.
- **Lipsitz & Goldberger (1992)**, "Loss of complexity and aging", *JAMA* — a
  dying heart becomes **more regular**, not less; declining heart-rate variability
  predicts mortality while the patient is still beating. Rigidity as a mortality
  signal in a system that never stops working.
- **March, J. (1991)** — exploration versus exploitation; the **competency trap**.
  **Leonard-Barton (1992)** — **core rigidities**. Over-exploitation locks a highly
  productive system into a local optimum.
- **Real options / optionality.** Rigidity as loss of convexity: the value of
  moves not yet taken.

**Correspondence:** Holling & Gunderson is the single best citation for the
two-sided band. The glass transition is the best citation for the specific insight
that $R$ cannot detect stalemate.

---

## 7. The consequence FSL has to face

Several of these literatures have measured this exact quantity, and the result
cuts against the law as written:

| measured $R$ | system | persists? |
|---|---|---|
| 0.667 | surface-area scaling | yes |
| 0.75 | mammalian metabolism | yes, ~10⁸ years |
| 0.85 | urban infrastructure | yes |
| 1.15 | urban socioeconomic output | only with repeated resets |

**Sublinear scaling is the signature of efficient, enduring systems.** And in the
urban literature it is the **superlinear** regime that is flagged as accelerating
and crisis-prone. FSL's requirement $R \ge 1$ therefore lands precisely in the
regime this literature identifies as unsustainable.

This is why [`viability_band.md`](viability_band.md) concludes that the constant
$1$ is real but the inequality is inverted. The FSL runs reporting
$\hat R \approx 0.50$–$0.85$ may not be failures at all — they may be correct
measurements against a threshold pointed the wrong way.

---

## 8. A caveat on novelty and on method

Two distinct issues:

**Priority.** The object is not new, and neither is the survival framing (Tainter),
the floor (Ashby), the ceiling (Holling & Gunderson), or the bit-accounting form
(MDL). FSL's defensible novelty is narrower and worth stating precisely: the
**synthesis** — a two-sided band whose edges are identified with the Greatest and
the Middle, plus the cadence condition as an independent third instrument, plus
band closure as a distinct fourth failure mode.

**Is $R$ even a dial?** In WBE, 3/4 is *derived* from network geometry — it is
forced, not chosen. Where an exponent is determined by structure, asking "what
sets $R_{\min}$" is the wrong question; the question is what sets $R$. Any
published form of the law must say which domains treat $R$ as a control variable
and which inherit it from topology.

---

## 9. Suggested minimum citation set

If only six references are added to the corpus:

1. Tainter (1988) — declining marginal returns on complexity as a collapse mechanism
2. Ashby (1956) — requisite variety; the floor
3. Holling & Gunderson (2002) — rigidity trap vs poverty trap; the two-sided band
4. Bettencourt & West (2007) — urban scaling exponents; finite-time singularity
5. Rissanen (1978) — MDL; $\Delta I \ge \Delta C$ in bits
6. Van Valen (1973) — Red Queen; the coevolutionary floor

Kleiber (1932) and West, Brown & Enquist (1997) should be added if the biological
correspondence is pursued; Lipsitz & Goldberger (1992) if the rigidity/variability
diagnostic is developed.
