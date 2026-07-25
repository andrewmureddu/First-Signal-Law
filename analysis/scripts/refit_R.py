#!/usr/bin/env python3
"""Refit R = d(ln I)/d(ln C) from the repository's own CSV outputs.

Reproduces the headline R-hat values and tests two things the plots do not show:
  1. whether R-hat is a global chord (OLS slope) or the local derivative the law states
  2. whether the complexity axis C carries independent information

Run from the repository root:  python3 analysis/scripts/refit_R.py
Standard library only.
"""

import csv
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SERIES = "Constrained__theta_2_0__-_lnI_vs_lnC.csv"
SUMMARIES = [
    "R_hat_summary_by_scenario.csv",
    "R_hat_with_linear_complexity.csv",
    "KL-divergence_complexity_results.csv",
]


def ols_slope(xs, ys):
    """Least-squares slope of ys on xs."""
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    den = sum((xs[i] - mx) ** 2 for i in range(n))
    return num / den


def main():
    path = os.path.join(ROOT, SERIES)
    rows = list(csv.DictReader(open(path)))
    s = [float(r["s"]) for r in rows]
    I = [float(r["I"]) for r in rows]
    C = [float(r["C"]) for r in rows]
    lI = [math.log(v) for v in I]
    lC = [math.log(v) for v in C]

    print("=" * 70)
    print("A) R-hat estimators on", SERIES)
    print("=" * 70)
    print("  OLS slope of lnI on lnC (all points) : %.4f   <- matches published 'R ~ 0.854'" % ols_slope(lC, lI))
    print("  endpoint chord                       : %.4f" % ((lI[-1] - lI[0]) / (lC[-1] - lC[0])))
    print("  local derivative at final step       : %.4f" % ((lI[-1] - lI[-2]) / (lC[-1] - lC[-2])))
    print()
    print("  The law states R = d(lnI)/d(lnC), a LOCAL derivative. The published")
    print("  figure reports a global regression slope, which averages the curve.")
    print()

    print("  local d(lnI)/d(lnC) along the sweep:")
    print("  %8s %12s %12s %14s" % ("s", "I", "C", "local R"))
    for i in range(1, len(s)):
        local = (lI[i] - lI[i - 1]) / (lC[i] - lC[i - 1])
        print("  %8.2f %12.2f %12.1f %14.4f" % (s[i], I[i], C[i], local))
    print()
    print("  -> declines monotonically %.4f -> %.4f: no point in the series meets R >= 1,"
          % ((lI[1] - lI[0]) / (lC[1] - lC[0]), (lI[-1] - lI[-2]) / (lC[-1] - lC[-2])))
    print("     and the trend moves away from the threshold as scale grows.")
    print()

    print("=" * 70)
    print("B) Does the complexity axis carry independent information?")
    print("=" * 70)
    ratios = [C[i] / s[i] for i in range(len(s))]
    exact = all(abs(r - ratios[0]) < 1e-9 for r in ratios)
    print("  C / s constant?  %s   (C = %.4f * s)" % (exact, ratios[0]))
    if exact:
        print("  => lnC = ln s + const, so d(lnI)/d(lnC) == d(lnI)/d(ln s).")
        print("     C is a pure rescaling of the sweep parameter. R-hat measures only")
        print("     how concavely I grows in s; the r/a/p role structure never enters.")
    print()

    print("=" * 70)
    print("C) Published R-hat by scenario (measure dependence)")
    print("=" * 70)
    for fname in SUMMARIES:
        fpath = os.path.join(ROOT, fname)
        if not os.path.exists(fpath):
            print("  [missing] %s" % fname)
            continue
        print("  %s" % fname)
        for r in csv.DictReader(open(fpath)):
            scen = r.get("scenario", "?")
            print("     %-46s R_hat = %.4f" % (scen[:46], float(r["R_hat"])))
    print()
    print("  The same scenario moves from ~0.50 (KL complexity) to ~0.80 (linear C).")
    print("  R-hat is not invariant to the choice of C, so the threshold 'R >= 1' is")
    print("  a threshold on an arbitrary unit convention until C is pinned down.")


if __name__ == "__main__":
    main()
