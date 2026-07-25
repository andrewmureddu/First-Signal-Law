#!/usr/bin/env python3
"""Structural properties of the logistic survival law, and a minimal repair.

    P_C = sigma(alpha*p + beta*S - gamma*D + eta*R_net + delta*u),   survive iff P_C >= P*

Demonstrates four properties of this functional form, then shows that two edits
make it consistent with axioms AX18 and AX19.

Run from anywhere:  python3 analysis/scripts/logistic_structure.py
Standard library only.
"""

import math

# Illustrative coefficients. Nothing here depends on their exact values; each
# demonstration below is a property of the functional FORM, not of the fit.
ALPHA, BETA, GAMMA, ETA, DELTA = 1.0, 0.8, 1.2, 1.5, 0.3
P_STAR = 0.5

# Interior optima for the repaired form.
R_OPT, U_OPT = 0.6, 0.25


def sigma(z):
    if z < -700:
        return 0.0
    return 1.0 / (1.0 + math.exp(-z))


def logit(q):
    return math.log(q / (1.0 - q))


def z_published(p, S, D, R, u):
    return ALPHA * p + BETA * S - GAMMA * D + ETA * R + DELTA * u


def z_repaired(p, S, D, R, u):
    """alpha*ln p  gates on the least (AX18); quadratic penalties create interior
    optima, so restraint and a noise floor become expressible (AX19)."""
    if p <= 0.0:
        return float("-inf")
    return (ALPHA * math.log(p) + BETA * S - GAMMA * D
            - ETA * (R - R_OPT) ** 2 - DELTA * (u - U_OPT) ** 2)


def survives(z):
    return z != float("-inf") and sigma(z) >= P_STAR


def main():
    print("=" * 72)
    print("1) The sigmoid is decision-theoretically inert")
    print("=" * 72)
    print("  P_C >= P*  <=>  z >= logit(P*) = %.4f" % logit(P_STAR))
    print("  sigma is strictly monotone, so it never affects the verdict.")
    print("  The survival criterion is a linear half-space in (p, S, D, R_net, u).")
    print()

    print("=" * 72)
    print("2) The overall scale is not identifiable from survive/die outcomes")
    print("=" * 72)
    p, S, D, R, u = 0.4, 1.0, 0.5, 0.6, 0.2
    base = z_published(p, S, D, R, u)
    for lam in (1, 3, 10):
        z = lam * base
        print("  lambda=%-3d  z=%8.3f  P_C=%.4f  survives=%s"
              % (lam, z, sigma(z), z >= lam * logit(P_STAR)))
    print("  P_C moves from %.4f to %.4f; the verdict never changes."
          % (sigma(base), sigma(10 * base)))
    print("  => only coefficient RATIOS are estimable. 6 parameters, 5 usable")
    print("     degrees of freedom. P_C is not a calibrated probability without a")
    print("     likelihood and a training set.")
    print()

    print("=" * 72)
    print("3) AX18 says a system endures IF AND ONLY IF the least endures")
    print("=" * 72)
    print("  published form (linear in p):")
    for p_ in (1.0, 0.4, 0.0):
        z = z_published(p_, S=1.5, D=0.3, R=1.2, u=0.2)
        print("    p=%.1f  z=%6.3f  P_C=%.4f  SURVIVES=%s" % (p_, z, sigma(z), sigma(z) >= P_STAR))
    print("  => the least collapses completely and the system is still rated a")
    print("     survivor: slack and release compensate. A linear model is")
    print("     compensatory; AX18 is a conjunctive gate. The form contradicts the axiom.")
    print()

    print("=" * 72)
    print("4) Restraint cannot exist in a monotone form")
    print("=" * 72)
    print("  dP_C/dR_net = eta * sigma'(z) > 0 for every value of R_net:")
    for R_ in (1, 10, 100, 1000):
        print("    R_net=%-6d P_C=%.10f" % (R_, sigma(z_published(0.4, 1.0, 0.5, R_, 0.2))))
    print("  => unbounded release is always optimal. 'Proportional release' and")
    print("     'the greatest restrains' require an INTERIOR optimum, which no linear")
    print("     term has. The same applies to +delta*u versus the stated noise floor.")
    print()

    print("=" * 72)
    print("5) Minimal repair")
    print("=" * 72)
    print("  z = alpha*ln p + beta*S - gamma*D - eta*(R_net - R*)^2 - delta*(u - u*)^2")
    print()
    print("  AX18 gate now holds exactly (p -> 0 drives z -> -inf):")
    for p_ in (1.0, 0.5, 0.1, 0.01, 0.0):
        z = z_repaired(p_, 1.5, 0.3, R_OPT, U_OPT)
        pc = 0.0 if z == float("-inf") else sigma(z)
        print("    p=%-5s P_C=%.6f  survives=%s" % (p_, pc, survives(z)))
    print()
    print("  restraint: release now has an interior optimum at R* = %.1f" % R_OPT)
    for R_ in (0.0, 0.3, 0.6, 1.0, 3.0, 10.0):
        print("    R_net=%-5s P_C=%.6f" % (R_, sigma(z_repaired(0.5, 1.5, 0.3, R_, U_OPT))))
    print()
    print("  noise floor: uncertainty now has an interior optimum at u* = %.2f" % U_OPT)
    for u_ in (0.0, 0.1, 0.25, 0.5, 2.0):
        print("    u=%-5s P_C=%.6f" % (u_, sigma(z_repaired(0.5, 1.5, 0.3, R_OPT, u_))))
    print()
    print("  For identifiability: fix P* = 0.5, add an explicit intercept, and")
    print("  normalise ||(alpha,beta,gamma,eta,delta)|| = 1 to remove the free scale.")


if __name__ == "__main__":
    main()
