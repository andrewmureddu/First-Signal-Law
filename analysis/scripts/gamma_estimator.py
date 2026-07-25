#!/usr/bin/env python3
"""Measurement protocol for gamma, the environmental variety exponent.

gamma sets the lower edge of the viability band (see ../viability_band.md section 2):
disturbance variety scales as C^gamma, and requisite variety demands R >= gamma.

gamma is estimated as the log-log slope of a DISTURBANCE INVENTORY -- the count of
distinct failure/perturbation types a system faces -- against system scale C. This
script establishes, by simulation against a known ground truth, which estimator to
use and what data quality is required.

Headline results (reproduced below):
  * The single controlling variable is SAMPLE COVERAGE. Observation-effort scaling and
    abundance skew matter only through their effect on it.
  * The naive distinct-type count is exact only when coverage is near 1. Otherwise it
    is badly biased, and effort scaling sets the DIRECTION: flat effort under-counts a
    growing disturbance pool (-0.18), effort rising with system size over-counts it
    (+0.12). Heavy abundance tails push it further up (+0.13 at zipf=2.0).
  * Chao1 is near-unbiased across the whole coverage range tested (within 0.03),
    where the naive count is off by up to +0.21. Its cost is precision, not accuracy.
  * Acceptance criterion: report Turing-Good coverage. A 95% CI width around 0.03
    needs coverage ~1.00; at 0.976 the width is ~0.16, which cannot resolve a thin
    margin. Coverage must be reported for a gamma estimate to be auditable.

Run from anywhere:  python3 analysis/scripts/gamma_estimator.py
Standard library only. Deterministic (fixed seeds).
"""

import math
import random
from collections import Counter

# Ground truth for the simulated world.
GAMMA_TRUE = 0.25          # true disturbance-variety exponent
POOL_SCALE = 20.0          # disturbance pool size = POOL_SCALE * C^gamma
SCALES = [10, 30, 100, 300, 1000]   # system complexities C (two decades)
REPS = 80                  # replicates per configuration
REPS_CRITERION = 250       # replicates for the acceptance-criterion table
ADEQUATE = 300             # events at the smallest scale giving coverage ~0.99


# --------------------------------------------------------------------------
# estimators
# --------------------------------------------------------------------------

def richness(sample):
    """Naive q=0 variety: number of distinct disturbance types observed."""
    return len(set(sample))


def chao1(sample):
    """Chao1 asymptotic richness estimator: corrects for unobserved types."""
    counts = Counter(sample)
    freq = Counter(counts.values())
    observed = len(counts)
    f1, f2 = freq.get(1, 0), freq.get(2, 0)
    if f2 > 0:
        return observed + f1 * f1 / (2.0 * f2)
    return observed + f1 * (f1 - 1) / 2.0


def coverage(sample):
    """Turing-Good sample coverage: fraction of probability mass observed."""
    counts = Counter(sample)
    f1 = sum(1 for v in counts.values() if v == 1)
    return 1.0 - f1 / len(sample)


def ols_slope(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    return (sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
            / sum((xs[i] - mx) ** 2 for i in range(n)))


# --------------------------------------------------------------------------
# simulated world
# --------------------------------------------------------------------------

_POOL_CACHE = {}


def disturbance_pool(C, zipf):
    """The true set of disturbance types at scale C, with a Zipf abundance profile.

    Real disturbance inventories are dominated by a few common modes with a long
    tail of rare ones; zipf controls how heavy that tail is.

    Returns (population, cumulative_weights). Cached, and cumulative weights are
    precomputed so random.choices does not rebuild them on every draw.
    """
    key = (C, zipf)
    if key not in _POOL_CACHE:
        size = max(2, int(round(POOL_SCALE * C ** GAMMA_TRUE)))
        cum, running = [], 0.0
        for rank in range(size):
            running += 1.0 / (rank + 1) ** zipf
            cum.append(running)
        _POOL_CACHE[key] = (list(range(size)), cum)
    return _POOL_CACHE[key]


def observe(C, n_events, zipf):
    pop, cum = disturbance_pool(C, zipf)
    return random.choices(pop, cum_weights=cum, k=n_events)


def run(depth_at_min_scale, effort_exponent, zipf, reps=REPS, seed=5):
    """Estimate gamma by both methods across the scale series.

    depth_at_min_scale : absolute number of observed events at the SMALLEST system
    effort_exponent    : observation effort scales as C^effort_exponent
    """
    random.seed(seed)
    n0 = depth_at_min_scale / (min(SCALES) ** effort_exponent)
    log_scales = [math.log(c) for c in SCALES]

    naive_slopes, chao_slopes, coverages = [], [], []
    for _ in range(reps):
        naive_pts, chao_pts, cov_pts = [], [], []
        for C in SCALES:
            n_events = max(2, int(round(n0 * C ** effort_exponent)))
            sample = observe(C, n_events, zipf)
            naive_pts.append(richness(sample))
            chao_pts.append(chao1(sample))
            cov_pts.append(coverage(sample))
        naive_slopes.append(ols_slope(log_scales, [math.log(v) for v in naive_pts]))
        chao_slopes.append(ols_slope(log_scales, [math.log(v) for v in chao_pts]))
        coverages.append(sum(cov_pts) / len(cov_pts))

    def summarise(vals):
        vals = sorted(vals)
        return (sum(vals) / len(vals), vals[int(0.025 * len(vals))],
                vals[int(0.975 * len(vals))])

    return summarise(naive_slopes), summarise(chao_slopes), sum(coverages) / len(coverages)


# --------------------------------------------------------------------------

def main():
    print("=" * 78)
    print("A) The confound is sampling COVERAGE, not observation-effort scaling")
    print("=" * 78)
    print("   true gamma = %.2f. Adequate depth: %d events at the smallest system." % (GAMMA_TRUE, ADEQUATE))
    print()
    print("   %-9s %9s %22s %22s"
          % ("effort", "coverage", "naive [95% CI]", "Chao1 [95% CI]"))
    for eff in (0.0, 0.5, 1.0):
        (nm, nl, nh), (cm, cl, ch), cov = run(ADEQUATE, eff, 1.0)
        print("   %-9.1f %9.3f %8.3f [%.3f,%.3f] %13.3f [%.3f,%.3f]"
              % (eff, cov, nm, nl, nh, cm, cl, ch))
    print()
    print("   Once effort rises with system size, both estimators recover gamma. The")
    print("   flat-effort row is the exception, and it is a COVERAGE effect: holding")
    print("   the event budget fixed while the pool grows leaves the largest systems")
    print("   under-sampled, so the naive count under-states their variety.")
    print()
    print("   The same configurations at shallow depth (50 events at the smallest):")
    print("   %-9s %9s %22s %22s"
          % ("effort", "coverage", "naive [95% CI]", "Chao1 [95% CI]"))
    shallow = {}
    for eff in (0.0, 1.0):
        (nm, nl, nh), (cm, cl, ch), cov = run(50, eff, 1.0)
        shallow[eff] = nm
        print("   %-9.1f %9.3f %8.3f [%.3f,%.3f] %13.3f [%.3f,%.3f]"
              % (eff, cov, nm, nl, nh, cm, cl, ch))
    print()
    print("   => at low coverage the naive count is badly biased, and the SIGN of the")
    print("      bias is set by effort scaling: flat effort under-counts the growing")
    print("      pool (%+.2f), effort rising with size over-counts it (%+.2f)."
          % (shallow[0.0] - GAMMA_TRUE, shallow[1.0] - GAMMA_TRUE))
    print()

    print("=" * 78)
    print("B) Acceptance criterion: bias and precision versus coverage")
    print("=" * 78)
    print("   %-11s %9s %21s %21s %10s"
          % ("depth@Cmin", "coverage", "naive (bias)", "Chao1 (bias)", "Chao1 CI"))
    criterion = []
    for depth in (25, 50, 100, 250, 500):
        (nm, _, _), (cm, cl, ch), cov = run(depth, 1.0, 1.0, reps=REPS_CRITERION)
        criterion.append((cov, nm - GAMMA_TRUE, cm - GAMMA_TRUE, ch - cl))
        print("   %-11d %9.3f %8.3f (%+.3f) %12.3f (%+.3f) %10.3f"
              % (depth, cov, nm, nm - GAMMA_TRUE, cm, cm - GAMMA_TRUE, ch - cl))
    print()
    worst_naive = max(abs(b) for _, b, _, _ in criterion)
    worst_chao = max(abs(b) for _, _, b, _ in criterion)
    print("   Across this range the naive count is off by up to %+.3f while Chao1 stays"
          % worst_naive)
    print("   within %.3f. What degrades as coverage falls is PRECISION, not accuracy."
          % worst_chao)
    print()
    print("   Acceptance criterion, derived from the table above (Chao1):")
    for cov, _, bias, ciw in criterion:
        usable = "usable" if ciw <= 0.12 else "too imprecise to test a thin margin"
        print("     coverage %.3f  ->  bias %+.3f, 95%% CI width %.3f   (%s)"
              % (cov, bias, ciw, usable))
    print()
    print("   Report coverage alongside every gamma estimate. An estimate without a")
    print("   coverage figure cannot be audited, because the bias is a function of it.")
    print()

    print("=" * 78)
    print("C) Robustness to the abundance profile (adequate depth, effort=1.0)")
    print("=" * 78)
    print("   %-8s %9s %22s %22s"
          % ("zipf", "coverage", "naive [95% CI]", "Chao1 [95% CI]"))
    skew = []
    for z in (0.5, 1.0, 1.5, 2.0):
        (nm, nl, nh), (cm, cl, ch), cov = run(ADEQUATE, 1.0, z)
        skew.append((z, cov, nm - GAMMA_TRUE, cm - GAMMA_TRUE))
        print("   %-8.1f %9.3f %8.3f [%.3f,%.3f] %13.3f [%.3f,%.3f]"
              % (z, cov, nm, nl, nh, cm, cl, ch))
    print()
    print("   => heavier tails degrade the NAIVE count (bias %+.3f at zipf=0.5 rising to"
          % skew[0][2])
    print("      %+.3f at zipf=2.0) because they depress coverage at fixed budget."
          % skew[-1][2])
    print("      Chao1 absorbs this: bias stays within %.3f across the whole range,"
          % max(abs(b) for _, _, _, b in skew))
    print("      at the cost of a wider interval. Skew acts only through coverage.")
    print()

    print("=" * 78)
    print("D) What this implies for testing the band")
    print("=" * 78)
    print("   The floor test is R >= gamma. It has power only when the MARGIN exceeds")
    print("   the confidence interval on gamma_hat.")
    print()
    best_cov, _, _, best_ciw = criterion[-1]
    mid_cov, _, _, mid_ciw = criterion[2]
    print("   Using the CI widths derived in (B): %.3f at coverage %.3f (best data),"
          % (best_ciw, best_cov))
    print("   %.3f at coverage %.3f (moderate data).\n" % (mid_ciw, mid_cov))
    print("   %-34s %8s %8s %12s %12s"
          % ("case", "R", "gamma", "best data", "moderate"))
    for name, R, g in (("mammal metabolism vs parasites", 0.75, 0.25),
                       ("urban infra vs disturbance", 0.85, 0.50),
                       ("thin margin (Red Queen regime)", 0.30, 0.25)):
        margin = R - g
        v1 = "TESTABLE" if margin > best_ciw else "underpowered"
        v2 = "TESTABLE" if margin > mid_ciw else "underpowered"
        print("   %-34s %8.2f %8.2f %12s %12s" % (name, R, g, v1, v2))
    print()
    print("   => wide-margin cases are testable even on moderate data. The Red Queen")
    print("      prediction of TIGHTLY CLUSTERED R is the hard one: a margin of ~0.05")
    print("      needs a CI width below that, which this simulation reaches only at")
    print("      coverage ~1.00. For rare failure modes that is a demanding but")
    print("      stateable data requirement -- not an impossibility.")


if __name__ == "__main__":
    main()
