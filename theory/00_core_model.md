# Coordination Under a Decaying Status Quo

*Working title. Formal core of the theory. Origin: the "First Signal Law" notes — but
this document stands on its own in the language of non-cooperative game theory and
makes no metaphysical commitments.*

---

## 1. The question

Why do groups stay locked in a safe-but-deteriorating arrangement when a better,
mutually-preferred arrangement is available and is itself a stable equilibrium? And
what changes the answer?

The standard answer in coordination theory is *risk dominance* (Harsanyi & Selten
1988): when cooperating requires trusting others to cooperate, agents often select the
**safe** equilibrium even though it is **payoff-inferior**, because the safe option does
not expose them to the cost of being the only one who moved. This is the trust/assurance
problem at the heart of the stag hunt (Skyrms 2004).

The contribution proposed here is one added ingredient: **the safe option's payoff
decays over time.** We show this is not merely a source of urgency — it is an *endogenous
equilibrium-selection device*. A deteriorating status quo solves the trust problem that a
stable status quo cannot.

---

## 2. The base game

Two players, symmetric. Each chooses an action: **C** (cooperate / "stag") or **S**
(safe / "hare"). Let `M[i][j]` be the payoff to a player choosing `i` against an
opponent choosing `j`.

|            | opp. C | opp. S |
|------------|--------|--------|
| **play C** | `R`    | `L`    |
| **play S** | `s`    | `s`    |

with `R > s > L`. Two features define the structure:

1. **C is payoff-dominant:** mutual cooperation `R` beats mutual safety `s` (`R > s`).
2. **S is safe:** its payoff is *independent of the opponent* (`M[S][C] = M[S][S] = s`).
   You never need to trust anyone to take the safe action — that is exactly why it traps.
3. **C is exposed:** cooperating against a non-cooperator yields `L < s` (the "sucker"
   payoff — wasted effort).

This is the **stag hunt**. It has two strict pure-strategy Nash equilibria, `(C,C)` and
`(S,S)`. There is no temptation to defect (this is *not* a prisoner's dilemma); the only
obstacle to the good equilibrium is the fear that the other will not join.

---

## 3. The trust threshold and risk dominance

Let `p` be a player's belief that the opponent plays C. Expected payoffs:

```
E[C] = pR + (1-p)L
E[S] = s            (constant — the defining safety property)
```

A player prefers C iff `E[C] > E[S]`, i.e. iff `p > p*` where

```
        s - L
p*  =  ---------          (the "trust threshold")
        R - L
```

`p*` is the minimum confidence in the partner needed to justify cooperating. It is also
the mixed-equilibrium probability and the boundary of the basin of attraction of `(C,C)`
under standard adaptive dynamics.

**Risk dominance.** `(C,C)` risk-dominates `(S,S)` iff the unilateral deviation loss at
`(C,C)` exceeds that at `(S,S)`:

```
(R - s)  >  (s - L)      ⟺      R + L > 2s      ⟺      p* < 1/2
```

With the canonical Skyrms numbers `R=3, s=2, L=0`: `R+L = 3 < 4 = 2s`, so `(S,S)` is
risk-dominant and `p* = 2/3`. You must be 2/3 sure of your partner to hunt stag — so
rational, cautious agents stay on hare. **This is the trap, stated precisely.**

---

## 4. The decay term (the contribution)

Now let the safe payoff erode over time: `s = s(t)` with `s'(t) < 0`. Everything above
holds period-by-period, but the trust threshold becomes time-dependent:

```
          s(t) - L
p*(t)  =  -----------          which is strictly decreasing in t.
           R - L
```

As the status quo decays, **the confidence required to justify cooperation falls.** The
basin of attraction of `(C,C)` grows monotonically. Define the switch time:

> **t\*** = the first time the cooperative equilibrium becomes risk-dominant,
> i.e. the first `t` with `s(t) < (R + L)/2`  (equivalently `p*(t) < 1/2`).

**Closed forms.**

- Linear decay `s(t) = s₀ − δt`:
  ```
  t* = (2 s₀ − R − L) / (2δ)
  ```
- Exponential decay `s(t) = s₀ e^{−δt}`:
  ```
  t* = (1/δ) · ln( 2 s₀ / (R + L) )
  ```

**Proposition 1 (selection under perturbation).** In a stag hunt with a decaying safe
payoff and fixed cooperative payoff, there is a finite `t*` after which `(C,C)` is
risk-dominant. In a 2×2 coordination game the risk-dominant equilibrium is the unique
stochastically stable state (Kandori–Mailath–Rob 1993; Young 1993), so any population
subject to persistent small perturbation selects cooperation for `t > t*`, regardless of
where it started. **Decay is an endogenous equilibrium-selection device.**

**Proposition 2 (the race, unperturbed dynamics).** Without perturbation, a population
whose cooperative mass `x₀` starts *below* the initial threshold `p*(0)` first erodes
toward `S`. It is rescued only if the falling boundary `p*(t)` overtakes the eroding mass
before collapse — i.e. iff the decay rate exceeds a critical value `δ_crit(x₀)`. Below
`δ_crit` the status quo dies too slowly and the group stays trapped; above it, decay
rescues cooperation. This is a genuine **phase transition in the decay rate** (confirmed
numerically: for `x₀ = 0.45`, `R=3, L=0, s₀=2`, `δ_crit ≈ 0.08`).

The two propositions are the honest, complete statement: decay *always* helps under
realistic noise (Prop 1), and even in the deterministic limit it rescues cooperation once
it is fast enough relative to how quickly trust erodes (Prop 2). The interesting,
non-obvious content is Prop 2 — there is such a thing as *too slow* a collapse.

This is the spine. Everything below extends it. See `sim/decay_coordination.py`.

---

## 5. Extensions (the original axioms, formalized)

Each layer restates one "First Signal Law" axiom in standard terms with a named lineage
and a checkable claim. Build order:

1. **Base 2×2** — §2–4 above. *Core result: t\*.*
2. **Weakest-link N-player** (AX18, "collapse begins with the least"): group output
   `V = f(min_i e_i)`. Formalizes why the smallest/weakest link sets the ceiling, and
   why larger groups coordinate worse. Lineage: Hirshleifer 1983; Van Huyck, Battalio &
   Beil 1990. Add decay to the status-quo effort level; show t\* analog.
3. **Asymmetric / leading-by-example** (AX19, "restraint at the greatest"): heterogeneous
   capacities; the efficient first move is a costly visible action by the high-capacity
   player. Lineage: Hermalin 1998; costly signaling (Spence 1973).
4. **The middle as mediator** (AX20, "alignment in the middle"): an intermediary
   implements a correlated equilibrium / creates a focal point. Lineage: Aumann 1974/87;
   Schelling 1960.
5. **Repetition** (AX21, "persistence is relation"): folk-theorem conditions sustaining
   the cooperative path; the round-robin turn-taking protocol as a public strategy.
   Lineage: Friedman 1971; Fudenberg & Maskin 1986.

---

## 6. What is and is not claimed

- **Claimed:** the decaying-status-quo coordination game and the `t*` result appear to be
  a genuine (and clean) synthesis; the role-structured escape ties known mechanisms
  together around it.
- **Not claimed:** no quantum mechanics, no consciousness-causes-collapse, no theology.
  Those were the generative intuition, not load-bearing argument, and are omitted by
  design.
- **To verify before any novelty claim:** literature check on dynamic/non-stationary
  coordination games and "deadline/urgency" effects in equilibrium selection — the
  decay-as-selection-device angle must be confirmed as not-already-standard.
