#!/usr/bin/env python3
"""Derive the edges of the viability band on R = d(lnI)/d(lnC).

  A) complexity budget    C_coll(R) from benefit/upkeep scaling   (Tainter)
  B) floor  R_min = gamma from requisite variety                  (Ashby, Van Valen)
  C) ceiling, universal   R <= 1 from finite-time singularity     (Bettencourt & West)
  D) ceiling, relational  R <= mu / theta_top from mediator capacity
  E) band closure         gamma > R_max  =>  no survivable R exists

Run from anywhere:  python3 analysis/scripts/band_bounds.py
Standard library only.
"""

import math

# ---------------------------------------------------------------- A) budget
A_COEF, LAMBDA = 1.0, 0.5     # benefit scale, upkeep per unit complexity

# ---------------------------------------------------------------- B) floor
D0 = 0.3                      # disturbance prefactor


def c_peak(R, a=A_COEF, lam=LAMBDA):
    """Complexity at which net benefit a*C^R - lam*C is maximal (R < 1)."""
    return (a * R / lam) ** (1.0 / (1.0 - R))


def c_collapse(R, a=A_COEF, lam=LAMBDA):
    """Complexity at which net benefit returns to zero (R < 1)."""
    return (a / lam) ** (1.0 / (1.0 - R))


def main():
    print("=" * 76)
    print("A) R < 1 does not mean death. It means a bounded complexity budget.")
    print("=" * 76)
    print("   N(C) = a*C^R - lam*C     with a=%.1f, lam=%.1f" % (A_COEF, LAMBDA))
    print()
    print("   %6s %16s %18s %26s" % ("R", "C* (peak net)", "C_coll (N=0)", "headroom exp 1/(1-R)"))
    for R in (0.50, 2.0 / 3.0, 0.75, 0.85, 0.90, 0.95, 0.99):
        print("   %6.3f %16.4g %18.4g %26.1f" % (R, c_peak(R), c_collapse(R), 1.0 / (1.0 - R)))
    print()
    print("   R >= 1 -> N(C) grows without bound; no complexity ceiling exists:")
    for R in (1.0, 1.15):
        print("     R=%.2f  N(1e6) = %.4g" % (R, A_COEF * (1e6) ** R - LAMBDA * 1e6))
    print()
    print("   => the binding constraint is C < C_coll(R), not R >= R_min.")
    print("      'R >= 1' is correct for systems under UNBOUNDED complexity growth")
    print("      (Tainter's case) and wrong for steady-state systems (Kleiber at 0.75).")
    print("      The growth regime of C is the missing quantifier.")
    print()
    print("   Note the headroom exponent 1/(1-R) is violently nonlinear, so the")
    print("   DERIVATIVE of R is a far better vital sign than its level.")
    print()

    print("=" * 76)
    print("B) The floor is the environment's variety exponent, not a system property")
    print("=" * 76)
    print("   regulator variety I = C^R   vs   disturbance D = %.1f * C^gamma" % D0)
    print("   requisite variety (Ashby): need I >= D")
    print()
    print("   %6s %8s %12s %26s" % ("R", "gamma", "verdict", "fails at C ="))
    for R, g in ((0.75, 0.50), (0.75, 0.75), (0.75, 0.90),
                 (0.85, 0.90), (0.85, 1.10), (1.15, 0.90)):
        if R > g:
            verdict, where = "safe", "never"
        elif abs(R - g) < 1e-12:
            verdict, where = "marginal", "scale-free"
        else:
            verdict, where = "FAILS", "%.4g" % (D0 ** (1.0 / (R - g)))
        print("   %6.2f %8.2f %12s %26s" % (R, g, verdict, where))
    print()
    print("   => R_min = gamma. The identical system is safe, marginal or doomed")
    print("      depending only on its environment. The floor is relational.")
    print()
    print("   Red Queen consequence: in a coupled game the disturbance IS the other")
    print("   players' regulatory variety, so gamma_i = max_{j != i} R_j. Survival for")
    print("   all i then forces R_i = max_j R_j for every i -- every surviving player")
    print("   pinned to the same R, nobody able to deviate. That is a standstill,")
    print("   derived rather than assumed.")
    print()
    print("   Falsifiable: surviving players in a coupled competitive system should show")
    print("   TIGHTLY CLUSTERED R, with dispersion predicting which member fails next.")
    print()

    print("=" * 76)
    print("C) Universal ceiling at 1: no steady state above it")
    print("=" * 76)
    print("   Assume growth is autocatalytic in the variety generated: dC/dt = k*C^R.")
    print("   Then C^(1-R)/(1-R) = kt + const.")
    print()
    k, c0 = 1.0, 1.0
    for R in (0.85, 1.0, 1.15, 1.50):
        if R < 1.0:
            print("     R=%-5.2f sub-linear  : polynomial growth, no singularity" % R)
        elif R == 1.0:
            print("     R=%-5.2f linear      : C(t) = exp(kt), no singularity" % R)
        else:
            tc = c0 ** (1.0 - R) / (k * (R - 1.0))
            print("     R=%-5.2f SUPERLINEAR : finite-time singularity at t_c = %.4f" % (R, tc))
    print()
    print("   => R > 1 is not a viable STATIONARY regime, only a punctuated one that")
    print("      must be reset before t_c. This is why the superlinear urban exponent")
    print("      (~1.15) coexists with persistence: repeated innovation resets.")
    print()
    print("   CAVEAT, load-bearing: R is defined as a relation between I and C.")
    print("   Assuming C's time dynamics follow the same exponent is a SEPARATE posit")
    print("   (autocatalysis). Where C is driven exogenously there is no singularity")
    print("   and this ceiling does not apply.")
    print()

    print("=" * 76)
    print("D) Relational ceiling: the mediator must integrate the variety generated")
    print("=" * 76)
    mu = 1.0
    print("   variety I = C^R; integrating capacity = C^mu with mu = %.1f." % mu)
    print("   What must be integrated is the RELATIONS among the variety, so the")
    print("   binding exponent depends on mediation topology:")
    print()
    print("   %-38s %14s %12s" % ("topology", "cost", "R_max"))
    for name, cost, theta in (("all-to-all", "~ I^2", 2.0),
                              ("modular, k ~ sqrt(I)", "~ I^1.5", 1.5),
                              ("hierarchical / tree", "~ I log I", 1.0)):
        print("   %-38s %14s %12.3f" % (name, cost, mu / theta))
    print()
    print("   => R_max = min(mu / theta_top, 1).")
    print("      This is why hierarchies exist: all-to-all mediation caps you at 0.5,")
    print("      hierarchical mediation doubles the ceiling. It also predicts that")
    print("      systems near the ceiling respond by MODULARISING.")
    print()
    print("   Suggestive: the table independently produces 2/3 and ~3/4-1, which are")
    print("   the two contested biological exponents (Rubner's surface-area 2/3 vs")
    print("   Kleiber/WBE 3/4), and orders them correctly by mediation topology.")
    print("   Loose coincidence, not a fit -- but it was not handed these numbers.")
    print()

    print("=" * 76)
    print("E) The band can close entirely")
    print("=" * 76)
    print("   %8s %10s %18s %30s" % ("gamma", "mu_eff", "band", "status"))
    for g, mu_eff in ((0.5, 1.0), (0.9, 1.0), (0.9, 0.5), (1.2, 1.0)):
        hi = min(mu_eff, 1.0)
        width = hi - g
        status = ("viable, width %.2f" % width) if width > 0 else "CLOSED - no survivable R"
        print("   %8.2f %10.2f %18s %30s" % (g, mu_eff, "[%.2f, %.2f]" % (g, hi), status))
    print()
    print("   => a fourth failure mode, distinct from dissolution, attrition and")
    print("      stalemate: no viable R exists at all. This is the 'encroaching entropic")
    print("      force' of the asymmetric-stalemate paper -- passivity is fatal because")
    print("      a closed band admits no strategy.")
    print()
    print("   The escape is to raise mu_eff: add mediation channels, or restructure")
    print("   topology from all-pairs toward hierarchy. Cooperation is the mu-raising")
    print("   move, which is why trust is not decoration on the game theory.")
    print()

    print("=" * 76)
    print("Assembled criterion")
    print("=" * 76)
    print("   gamma <= R <= min(mu / theta_top, 1)")
    print("   C < C_coll(R)")
    print("   tau_rotation < tau_damage")
    print()
    print("   Four failure modes: dissolution (ceiling), attrition (budget),")
    print("   stalemate (cadence, invisible to R), band closure (gamma > R_max).")
    print()
    print("   gamma, mu and theta_top are all UNMEASURED in this repository. The")
    print("   deliverable is three estimators, not a universal constant.")


if __name__ == "__main__":
    main()
