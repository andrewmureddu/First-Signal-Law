# The Viability Band: a two-sided reformulation of $R$

**Status:** derivation notes. This document proposes a successor to the FSL
endurance criterion $R = d(\ln I)/d(\ln C) \ge 1$. It is constructive — the
empirical problems that motivate it are recorded separately in
[`empirical_review.md`](empirical_review.md).

All numerical claims are reproduced by
[`scripts/band_bounds.py`](scripts/band_bounds.py) and
[`scripts/cadence_blindness.py`](scripts/cadence_blindness.py).

---

## The claim in one line

$$\boxed{\;\gamma \;\le\; R \;\le\; \min\!\left(\tfrac{\mu}{\theta_{\text{top}}},\; 1\right), \qquad C < C_{\text{coll}}(R), \qquad \tau_{\text{rot}} < \tau_{\text{damage}}\;}$$

Endurance is not a floor on $R$. It is a **band**, plus a complexity budget, plus
a cadence condition. The band's lower edge is set by the environment, its upper
edge by the mediator, and the original law's constant $1$ is real — but it is a
**ceiling, not a floor**.

---

## 0. Orientation

Read $I$ as **variety / optionality generated** and $C$ as **constraint or
complexity accumulated**. Then

$$R = \frac{d\ln I}{d\ln C} = \frac{C}{I}\cdot\frac{dI}{dC}$$

is an **elasticity** — a log-log slope — and the two failure directions are:

| direction | mechanism | failure mode |
|---|---|---|
| $R$ too low | constraint accumulates, no new moves are generated | **rigidity / stalemate** |
| $R$ too high | variety outruns whatever binds it | **dissolution / losing the thread** |

This orientation is a choice, and it should be stated explicitly in any published
form, because it determines the band's geometry. It is the reading adopted here
because it is the one under which the empirical record coheres:

| $R$ | system | status |
|---|---|---|
| ~0.50 | FSL KL-complexity runs | low; drifting toward the rigidity floor |
| 0.667 | surface-area scaling (Rubner) | mid-band |
| 0.75 | Kleiber metabolic scaling | mid-band; persists ~10⁸ yr |
| 0.85 | urban infrastructure (Bettencourt & West) | mid-band |
| **1.0** | — | **ceiling** |
| 1.15 | urban socioeconomic output | above ceiling; crisis-prone, requires resets |

**Mammals and cities have $R < 1$ and they persist.** Sublinear scaling is the
signature of efficient, enduring systems — economies of scale — not collapsing
ones. Kleiber's exponent has held across ~20 orders of magnitude of body mass for
a century. Any criterion that reads $R < 1$ as fatal is contradicted by the
best-established instances of its own estimator.

---

## 1. $R < 1$ does not mean death — it means a bounded complexity budget

Make Tainter's mechanism explicit. Let benefit scale with elasticity $R$ and
upkeep grow at least linearly in complexity:

$$N(C) = aC^R - \lambda C$$

For $R < 1$ this peaks at $C^* = (aR/\lambda)^{1/(1-R)}$ and returns to zero at

$$C_{\text{coll}} = (a/\lambda)^{1/(1-R)}$$

For $R \ge 1$, $N$ grows without bound and **no complexity ceiling exists at all**.

With $a = 1, \lambda = 0.5$:

| $R$ | 0.50 | 0.667 | 0.75 | 0.85 | 0.90 | 0.95 | 0.99 |
|---|---|---|---|---|---|---|---|
| $C^*$ | 1 | 2.37 | 5.06 | 34.4 | 357 | 3.8×10⁵ | 4.6×10²⁹ |
| $C_{\text{coll}}$ | 4 | 8.00 | 16 | 102 | 1024 | 1.05×10⁶ | 1.27×10³⁰ |
| $1/(1-R)$ | 2 | 3 | 4 | 6.7 | 10 | 20 | 100 |

**The binding constraint is $C < C_{\text{coll}}(R)$, not $R \ge R_{\min}$.** A
system at $R = 0.5$ persists indefinitely provided it never pushes complexity past
its budget.

### This partially vindicates the original law

$R \ge 1$ is **exactly correct for systems under unbounded complexity growth** —
Tainter's case, and arguably a civilisation's. It is wrong only when applied to
steady-state systems. Mammals survive at 0.75 because mature organisms do not
accumulate $C$ without limit; societies at 0.85 die because they do.

**The growth regime of $C$ is the missing quantifier.** The repo never states
which regime it claims, and the claim is only true in one of them.

### The derivative of $R$ matters far more than its level

The headroom exponent $1/(1-R)$ is violently nonlinear. The θ=2.0 drift recorded
in [`empirical_review.md`](empirical_review.md) §1a — 0.931 → 0.697 — is not a
modest decline: it is complexity headroom collapsing from ~10⁴ to ~10¹. **The
level of $R$ is nearly uninformative; its trend is the vital sign.**

---

## 2. The floor is the environment's variety exponent

Where a genuine lower bound comes from is Ashby's law of requisite variety: a
regulator must possess at least as much variety as the disturbance it regulates.
If disturbance variety scales as $C^\gamma$ and regulatory variety as $C^R$:

$$R_{\min} = \gamma$$

| $R$ | $\gamma$ | verdict | regulation fails at $C$ = |
|---|---|---|---|
| 0.75 | 0.50 | safe | never |
| 0.75 | 0.75 | marginal | scale-free |
| 0.75 | 0.90 | **fails** | 3,061 |
| 0.85 | 0.90 | **fails** | 2.9×10¹⁰ |
| 0.85 | 1.10 | **fails** | 124 |
| 1.15 | 0.90 | safe | never |

The identical system is safe, marginal or doomed depending only on its
environment. **The floor is not a property of the system** — which is exactly
FSL's own thesis that persistence is relational, now with a measurable
right-hand side.

### The Red Queen consequence: stalemate, derived

In a coupled multiplayer game the disturbance *is* the other players' regulatory
variety, so $\gamma_i = \max_{j \ne i} R_j$. Survival for all $i$ requires
$R_i \ge \max_{j\ne i} R_j$. Let $M = \max_j R_j$ and let $i^*$ achieve it; then
for every other $i$, $R_i \ge R_{i^*} = M$, and since $M$ is the maximum,
$R_i = M$.

**The floor forces every surviving player to the same $R$.** Everyone running at
maximum merely to stay in place, no unilateral deviation profitable, nobody able
to move. This is Van Valen's Red Queen — and it is the "Degenerative Equilibrium"
of `15.Asymmetric Stalemate`, obtained by derivation rather than stipulation.

Asymmetry follows too: a Large player sustains high $R$ at lower relative cost,
raising $\gamma$ for everyone. The Small player, holding the least headroom, meets
its $C_{\text{coll}}$ first. The paper's "Player C is most vulnerable" is a
consequence, not an assumption.

**New falsifiable prediction.** In any coupled competitive system, surviving
players' $R$ should be **tightly clustered**, with dispersion predicting which
member fails next. Testable on firms within an industry, species within a guild,
cities within a network.

---

## 3. The ceiling: two bounds of different character

The binding ceiling is whichever is lower.

### 3a. Universal, at exactly 1 — no steady state above it

If growth is autocatalytic in the variety generated, $dC/dt = kC^R$, then
$C^{1-R}/(1-R) = kt + \text{const}$. For $R > 1$ the exponent is negative and
$C \to \infty$ at **finite time**:

| $R$ | behaviour |
|---|---|
| 0.85 | polynomial growth, no singularity |
| 1.00 | exponential, no singularity |
| 1.15 | **singularity at $t_c = 6.67$** |
| 1.50 | **singularity at $t_c = 2.00$** |

So $R > 1$ is not a viable *stationary* regime — only a punctuated one, reset
before $t_c$. This is why the superlinear urban exponent (~1.15) coexists with
persistence: repeated innovation resets, each restarting the clock.

> **Load-bearing caveat.** $R$ is *defined* as a relation between $I$ and $C$.
> Assuming $C$'s time dynamics follow the same exponent is a **separate posit**
> (autocatalysis). Where $C$ is driven exogenously there is no singularity and
> this ceiling does not apply. It should be stated as a domain condition, not
> assumed universally.

### 3b. Relational — the mediator must integrate the variety generated

The dual of the floor. Let integrating capacity scale as $C^\mu$. What must be
integrated is not the variety itself but the **relations among** it, so the
binding exponent depends on mediation topology:

| mediation topology | integration cost | condition | $R_{\max}$ at $\mu = 1$ |
|---|---|---|---|
| all-to-all | $\propto I^2$ | $2R \le \mu$ | **0.500** |
| modular, $k \sim \sqrt{I}$ | $\propto I^{1.5}$ | $1.5R \le \mu$ | **0.667** |
| hierarchical / tree | $\propto I \log I$ | $R \lesssim \mu$ | **1.000** |

$$R_{\max} = \min\!\left(\frac{\mu}{\theta_{\text{top}}},\; 1\right)$$

**This is why hierarchies exist.** All-to-all mediation caps you at 0.5;
hierarchical mediation doubles the ceiling. It predicts that systems approaching
their dissolution ceiling respond by **modularising** — which is what organs,
divisions, software modules and city neighbourhoods are.

**An unplanned check.** The table independently produces 2/3 and ~3/4–1, which are
the two most-contested exponents in biological scaling — Rubner's surface-area 2/3
versus Kleiber/WBE's 3/4 — and orders them correctly by mediation topology, since
WBE's argument is precisely that fractal hierarchical networks beat naive surface
scaling. This is suggestive rather than confirmatory (loose coincidence, no data
fitted), but it is the first number this framework produced that it was not
handed.

---

## 4. AX20 is the ceiling; AX21 is the missing instrument

### 4a. Alignment sets the upper edge

[`empirical_review.md`](empirical_review.md) §2e records that AX20 ("the middle
aligns the extremes") has no variable anywhere in the formalism. It has one now:
**$\mu$ is the Middle's capacity exponent, and it sets $R_{\max}$.** The band's
geometry *is* the three-role structure:

| Role | Formal object | Function |
|---|---|---|
| **The Greatest** / environment | $\gamma$ | sets the **floor** |
| **The Middle** / alignment | $\mu / \theta_{\text{top}}$ | sets the **ceiling** |
| **The Least** | $R$ itself | must live **in the band** |

FSL's central claim — that the least persists only when the greatest is restrained
and the middle aligns — is recovered as: *the viable interval for $R$ is bounded
below by the environment and above by the mediator.*

### 4b. $R$ is blind to stalemate — a proof, not a caveat

`scripts/cadence_blindness.py`. Two systems are given identical $I$ and $C$
trajectories, hence identical $R$ by construction, and identical activity — every
agent acts in every round. They differ only in whether roles rotate:

| system | $R$ | $H$(greatest) | $H$(least) | distinct configs | moves |
|---|---|---|---|---|---|
| cadence | 0.850000 | 1.585 bits | 1.585 bits | 3 | 72 |
| stalemate | 0.850000 | 0.000 bits | 0.000 bits | 1 | 72 |

$R$ is identical to six decimal places; both read as healthy mid-band. **Nobody is
idle in the stalemate** — each agent re-chooses *Stay* every round, which is a
move. What separates them is reachability: 3 configurations versus 1.

The reason is structural, not a calibration failure: **$R$ is a derivative along a
realised trajectory, while stalemate is a property of the reachable set** — the
moves you *don't* have. No derivative measured inside a basin can detect the
absence of routes out of it. A second instrument is therefore *required*, and no
tuning of $R_{\min}$ can substitute.

The physical archetype is the **glass**: locally jiggling, globally arrested,
non-ergodic, no longer exploring configuration space.

### 4c. Cadence — and the correct form of the condition

AX21 already contains the instrument: *"persistence is not carried by one role
alone but by their cadence together… each rotating through restraint, alignment,
and persistence."* The survival equation has **no time index**, so it cannot
express rotation, so it cannot detect stalemate.

The condition is best written as a **timescale separation**, not an entropy level:

$$\tau_{\text{rotation}} < \tau_{\text{damage}}$$

Roles must rotate faster than damage accumulates in any single role. Cadence
entropy $H$ is a convenient screen but only a proxy — a system can rotate role
*labels* cosmetically without changing what is reachable and would score well.
The quantity of record is reachable-set volume, or perturbation response /
relaxation time, which is how physics actually measures rigidity.

### 4d. This closes the loop with the stalemate paper

The asymmetric standoff is a **frozen role assignment**: A permanently dominant,
C permanently vulnerable, nobody rotating. The escape proposed there — A
deliberately creates a vulnerability that C could exploit — is *the greatest
voluntarily occupying the Least's position*. **That is a cadence event.** AX21
predicts the paper's own solution, and the rigidity ceiling is AX21 violated.

---

## 5. Band closure: a fourth failure mode

The band collapses when $\gamma > \min(\mu_{\text{eff}}, 1)$:

| $\gamma$ | $\mu_{\text{eff}}$ | band | status |
|---|---|---|---|
| 0.5 | 1.0 | [0.50, 1.00] | viable, width 0.50 |
| 0.9 | 1.0 | [0.90, 1.00] | viable, width 0.10 |
| 0.9 | 0.5 | [0.90, 0.50] | **CLOSED** |
| 1.2 | 1.0 | [1.20, 1.00] | **CLOSED** |

**No survivable $R$ exists.** This is distinct from dissolution, attrition and
stalemate, and it is the "encroaching entropic force that guarantees collective
annihilation if they remain passive" of the stalemate paper: **passivity is fatal
because a closed band admits no strategy.**

The escape is to raise $\mu_{\text{eff}}$ — add mediation channels, or restructure
topology from all-pairs toward hierarchy. **Cooperation is the $\mu$-raising
move**, which is why trust is not decoration bolted onto the game theory: it is
the only available action that changes the band. AX20 is the mechanism.

---

## 6. The four failure modes

| mode | condition | detected by |
|---|---|---|
| **Dissolution** | $R > R_{\max}$ | $R$ |
| **Attrition** | $C > C_{\text{coll}}(R)$ | $R$ + complexity accounting |
| **Stalemate** | $R$ in band, cadence frozen | **cadence / reachability only** |
| **Band closure** | $\gamma > R_{\max}$ | $\gamma$ and $\mu$ jointly |

Only the first is visible to the original criterion, and it is visible with the
inequality reversed.

---

## 7. What this does to the original law

**FSL's constant $1$ is real.** It is a genuine boundary — above it no stationary
regime exists (§3a). The law found the right number and inverted the inequality:

$$R \ge 1 \quad \longrightarrow \quad R \le 1$$

And the band is **asymmetric**: the floor is purely relational ($\gamma$), while
the ceiling is relational with a hard universal lid. An earlier conjecture in this
analysis — that the ceiling might also be purely relational, making the band
entirely relational — is **wrong**, and §3a is the correction.

The reframing also rescues the repository's own results. The θ=2.0 series is not
"failing a threshold at 0.854"; it is **drifting down through the band toward the
rigidity floor**, from 0.931 to 0.697. That is a diagnosable dynamic rather than a
null result.

---

## 8. Honest limitations

1. **$\gamma$, $\mu$ and $\theta_{\text{top}}$ are all unmeasured.** Nothing in
   this repository estimates any of them, and the whole framework now rests on
   them. This is the same class of problem as the original $C$-definition gap.
2. **The universal ceiling needs autocatalysis** (§3a). State it as a domain
   condition.
3. **$\theta_{\text{top}}$ assumes integration cost is a clean power of variety.**
   Real mediators will not obey this exactly.
4. **Cadence entropy is a proxy** for reachable-set volume (§4c), and is gameable
   by cosmetic rotation.
5. **The 2/3 and 3/4 correspondence is a coincidence, not a fit** (§3b). No data
   was regressed; do not present it as validation.
6. **$R$ is not always a control variable.** WBE *derive* 3/4 from space-filling
   fractal branching — it is forced by topology, not selected. In such domains the
   question is not what sets $R_{\min}$ but what sets $R$. Any published form must
   say which domains treat $R$ as a dial and which inherit it from structure.

---

## 9. What the deliverable actually is

$R$ is a dimensionless control parameter whose critical values must be *measured
per domain* — structurally like a Reynolds number, where $Re_{\text{crit}} \approx
2300$ for pipe flow and differs for every other geometry. Universal in **form**,
domain-specific in **value**. That is respectable physics, but it carries an
obligation:

**Ship three estimators, not a universal constant.**

1. **$\gamma$** — from environmental variety scaling. The least defended number in
   the structure, and the natural next target.
2. **$\mu$** — from mediator throughput.
3. **$\theta_{\text{top}}$** — from mediation topology.

Prior art for all of the above is mapped in [`prior_art.md`](prior_art.md).

---

## Reproducing

```sh
python3 analysis/scripts/band_bounds.py        # sections 1, 2, 3, 5
python3 analysis/scripts/cadence_blindness.py  # section 4b
```

Standard library only; no third-party dependencies.
