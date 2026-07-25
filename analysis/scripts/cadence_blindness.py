#!/usr/bin/env python3
"""Show that R = d(lnI)/d(lnC) cannot detect stalemate.

Two systems are given IDENTICAL I and C trajectories, so they have identical R by
construction, and identical activity (every agent acts every round). They differ
only in whether roles rotate. R sees nothing; cadence entropy separates them
completely.

This is the formal content of "you can still be moving during a stalemate":
R is a derivative along a realised path, while stalemate is a property of the
reachable set. No derivative measured inside a basin can detect the absence of
routes out of it.

Run from anywhere:  python3 analysis/scripts/cadence_blindness.py
Standard library only.
"""

import math
from collections import Counter

T = 24          # rounds
AGENTS = ("A", "B", "C")
ROLES = ("greatest", "middle", "least")


def entropy_bits(seq):
    n = len(seq)
    counts = Counter(seq)
    return -sum((v / n) * math.log2(v / n) for v in counts.values())


def ols_slope(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    return (sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
            / sum((xs[i] - mx) ** 2 for i in range(n)))


def R_of(I, C):
    return ols_slope([math.log(v) for v in C], [math.log(v) for v in I])


def main():
    # One macro trajectory, shared by both systems. Mid-band elasticity.
    C = [100.0 * (1.0 + 0.15 * t) for t in range(T)]
    I = [20.0 * (C[t] / C[0]) ** 0.85 for t in range(T)]

    # System 1 -- cadence: roles rotate among the agents (AX21 satisfied).
    rotation = [("A", "B", "C"), ("B", "C", "A"), ("C", "A", "B")]
    cadence = [rotation[t % 3] for t in range(T)]

    # System 2 -- stalemate: role assignment frozen. Every agent still acts every
    # round (each re-chooses "Stay"), so activity is identical, not reduced.
    stalemate = [("A", "B", "C") for _ in range(T)]

    print("=" * 78)
    print("Two systems, identical macro trajectory, differing only in role rotation")
    print("=" * 78)
    print("  %-11s %10s %14s %12s %12s %8s"
          % ("system", "R", "H(greatest)", "H(least)", "configs", "moves"))
    for name, assign in (("cadence", cadence), ("stalemate", stalemate)):
        greatest = [a[0] for a in assign]
        least = [a[2] for a in assign]
        print("  %-11s %10.6f %11.3f bits %7.3f bits %12d %8d"
              % (name, R_of(I, C), entropy_bits(greatest), entropy_bits(least),
                 len(set(assign)), T * len(AGENTS)))

    print()
    print("  R is identical to 6 decimal places -- both sit mid-band and both read")
    print("  as healthy. Activity is identical: %d moves each, nobody idle." % (T * len(AGENTS)))
    print("  What separates them is reachability: %d distinct configurations vs %d."
          % (len(set(cadence)), len(set(stalemate))))
    print()
    print("  => a viability criterion on R alone cannot see the rigidity wall.")
    print("     A second instrument is structurally required, not merely desirable.")
    print()
    print("  Caveat: cadence entropy is a PROXY. A system can rotate role labels")
    print("  cosmetically without changing what is actually reachable, and would score")
    print("  well here. The quantity of record is reachable-set volume (or perturbation")
    print("  response / relaxation time, which is how physics measures rigidity).")
    print("  Treat H_cadence as a screen, not a proof.")


if __name__ == "__main__":
    main()
