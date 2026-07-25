#!/usr/bin/env python3
"""Measurement protocol for mu and theta_top, the viability band's upper edge.

The dissolution ceiling is R_max = min(mu / theta_top, 1), where mu is the exponent
with which the mediator's INTEGRATING CAPACITY grows with system scale and theta_top
is the exponent of integration cost in the variety being integrated
(see ../viability_band.md section 3b).

Headline results (reproduced below):
  * A throughput-versus-scale regression does NOT measure mu. Observed throughput is
    demand-limited whenever the mediator is not saturated, so it recovers the DEMAND
    exponent delta -- and it does so with a near-zero confidence interval. A tight,
    confident, wrong answer.
  * Capacity information lives in the delay-load relationship, which only carries
    signal near saturation. mu is recoverable from delay data, but the estimator is
    unusable below ~50% peak utilisation. Above ~90% the bias collapses to -0.02 and
    precision becomes the binding limit: +/-0.13 on 12 load points at 12% latency
    noise, tightening to +/-0.007 on 100 points at 2% noise.
  * At low utilisation the delay estimator frequently REFUSES (fitted slope of the
    wrong sign) rather than returning a wrong number. That is the desirable failure
    mode, and the opposite of the throughput regression's.
  * delta = R * theta_top exactly. So the throughput regression is the right
    estimator for the wrong parameter: given R it yields theta_top, not mu.

Consequence for the theory: you cannot measure a capacity by observing an unstressed
system, so the band's UPPER edge is intrinsically harder to observe than its lower
edge. A system far from its ceiling cannot locate it. What is observable throughout
is utilisation itself -- so the operational early warning is the TREND in rho, not
a measurement of mu.

Run from anywhere:  python3 analysis/scripts/mu_estimator.py
Standard library only. Deterministic (fixed seeds).
"""

import math
import random

# Ground truth for the simulated world.
MU_TRUE = 0.70        # mediator capacity exponent: kappa(C) = K0 * C^mu
DELTA_TRUE = 0.90     # demand exponent: offered load Lambda(C) = L0 * C^delta
K0 = 50.0             # capacity scale
SERVICE_TIME = 0.02   # unloaded latency per coordination act
SCALES = [10, 30, 100, 300, 1000]
LOAD_SWING = 0.45     # multiplicative load variation observed at each scale
NOISE = 0.12          # lognormal latency measurement noise (sigma)
REPS = 300


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def linfit(xs, ys):
    """Return (slope, intercept) of ys on xs."""
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    denom = sum((xs[i] - mx) ** 2 for i in range(n))
    slope = sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / denom
    return slope, my - slope * mx


def summarise(vals):
    if not vals:
        return float("nan"), float("nan"), float("nan")
    vals = sorted(vals)
    return (sum(vals) / len(vals), vals[int(0.025 * len(vals))],
            vals[int(0.975 * len(vals))])


def capacity(C):
    return K0 * C ** MU_TRUE


# --------------------------------------------------------------------------
# the mediator under observation
# --------------------------------------------------------------------------

def observe_scale(C, load_base, rng_noise, npts=12):
    """Observed (load, mean delay) pairs at one scale.

    Delay model: W = W0 / (1 - rho), rho = Lambda / kappa. This separates service
    time W0 from capacity kappa -- unlike M/M/1, where they are locked together and
    capacity could be read straight off the unloaded latency. The separation is what
    makes capacity genuinely hard to observe at low load.
    """
    kap = capacity(C)
    pairs = []
    for i in range(npts):
        factor = 1.0 + LOAD_SWING * (2.0 * i / (npts - 1.0) - 1.0)
        lam = load_base * factor
        rho = lam / kap
        if rho >= 0.99:
            continue
        W = (SERVICE_TIME / (1.0 - rho)) * math.exp(random.gauss(0, rng_noise))
        pairs.append((lam, W))
    return pairs


def estimate(peak_utilisation, reps=REPS, noise=NOISE, npts=12, seed=11):
    """Run both estimators. peak_utilisation is rho at the largest system's peak load."""
    random.seed(seed)
    cmax = max(SCALES)
    l0 = (peak_utilisation * K0 * cmax ** MU_TRUE
          / (cmax ** DELTA_TRUE * (1.0 + LOAD_SWING)))

    log_scales = [math.log(c) for c in SCALES]
    throughput_slopes, capacity_slopes = [], []
    refusals = 0
    peak_seen = 0.0

    for _ in range(reps):
        mean_loads, kappa_hats = [], []
        bad = False
        for C in SCALES:
            base = l0 * C ** DELTA_TRUE
            pairs = observe_scale(C, base, noise, npts)
            if len(pairs) < 3:
                bad = True
                break
            peak_seen = max(peak_seen, max(p[0] for p in pairs) / capacity(C))
            loads = [p[0] for p in pairs]
            inv_delays = [1.0 / p[1] for p in pairs]
            # 1/W = (1/W0) - Lambda/(W0*kappa): intercept/-slope recovers kappa.
            slope, intercept = linfit(loads, inv_delays)
            if slope >= 0 or intercept <= 0:
                bad = True          # noise swamped the load signal: refuse
                break
            kappa_hats.append(-intercept / slope)
            mean_loads.append(sum(loads) / len(loads))
        if bad or any(v <= 0 for v in kappa_hats):
            refusals += 1
            continue
        throughput_slopes.append(linfit(log_scales, [math.log(v) for v in mean_loads])[0])
        capacity_slopes.append(linfit(log_scales, [math.log(v) for v in kappa_hats])[0])

    return (summarise(throughput_slopes), summarise(capacity_slopes),
            peak_seen, refusals, reps)


# --------------------------------------------------------------------------

def main():
    print("=" * 78)
    print("A) The trap: a throughput regression does not measure capacity")
    print("=" * 78)
    print("   truth: mu = %.2f (CAPACITY exponent), delta = %.2f (DEMAND exponent)"
          % (MU_TRUE, DELTA_TRUE))
    print("   utilisation rises with scale as C^(delta-mu) = C^%.2f"
          % (DELTA_TRUE - MU_TRUE))
    print()
    print("   %-11s %9s %26s %26s"
          % ("peak rho", "refused", "throughput slope [95% CI]", "delay-based mu [95% CI]"))
    rows = []
    for peak in (0.10, 0.30, 0.50, 0.75, 0.90, 0.97):
        (tm, tl, th), (cm, cl, ch), _, ref, reps = estimate(peak)
        rows.append((peak, tm, cm, ch - cl, ref / reps))
        print("   %-11.2f %8.0f%% %11.3f [%.3f,%.3f] %13.3f [%.3f,%.3f]"
              % (peak, 100.0 * ref / reps, tm, tl, th, cm, cl, ch))
    print()
    print("   The throughput slope sits on delta = %.2f at every utilisation, with a"
          % DELTA_TRUE)
    print("   confidence interval near zero. It is not noisy -- it is confidently")
    print("   measuring the wrong quantity. Bias %+.2f that no amount of data removes."
          % (DELTA_TRUE - MU_TRUE))
    print()

    print("=" * 78)
    print("B) Capacity is only observable near saturation")
    print("=" * 78)
    print("   %-11s %14s %12s %14s %12s"
          % ("peak rho", "mu_hat", "bias", "95% CI width", "refused"))
    for peak, _, cm, ciw, refrate in rows:
        if refrate >= 0.10:
            verdict = "unusable (refuses)"
        elif ciw > 0.30:
            verdict = "order-of-magnitude only"
        else:
            verdict = "usable, +/-%.2f" % (ciw / 2.0)
        print("   %-11.2f %14.3f %+12.3f %14.3f %11.0f%%   %s"
              % (peak, cm, cm - MU_TRUE, ciw, 100 * refrate, verdict))
    print()
    print("   Capacity information lives in the CURVATURE of delay against load, which")
    print("   is negligible while the mediator is idle. Below ~50% peak utilisation the")
    print("   estimator is unusable. Above it the bias collapses, but PRECISION stays")
    print("   the binding limit -- see the data-budget table below.")
    print()
    print("   Data budget required, at peak utilisation 0.90:")
    print("   %-13s %-9s %12s %14s %10s"
          % ("load points", "noise", "mu_hat", "95% CI width", "refused"))
    for npts, noise in ((12, 0.12), (30, 0.12), (100, 0.12),
                        (30, 0.05), (100, 0.05), (100, 0.02)):
        _, (cm, cl, ch), _, ref, reps = estimate(0.90, noise=noise, npts=npts)
        print("   %-13d %-9.2f %12.3f %14.3f %9.0f%%"
              % (npts, noise, cm, ch - cl, 100.0 * ref / reps))
    print()
    print("   => the limit is instrument precision, not rare events. Latency is cheap to")
    print("      measure densely, so a good budget is realistic wherever the mediator can")
    print("      be observed under load -- which is the real constraint.")
    print()
    print("   Note the failure MODE. At low utilisation the delay estimator refuses")
    print("   outright (fitted slope of the wrong sign) rather than returning a wrong")
    print("   number. That is the property worth having, and it is exactly opposite to")
    print("   the throughput regression, which never refuses and is always wrong.")
    print()

    print("=" * 78)
    print("C) The reframe: the throughput regression measures theta_top")
    print("=" * 78)
    print("   If variety I = I0*C^R and integration load Lambda = c*I^theta_top, then")
    print("   Lambda is proportional to C^(R*theta_top), so delta = R * theta_top.")
    print()
    i0, cost = 5.0, 0.3
    log_scales = [math.log(c) for c in SCALES]
    print("   %-8s %11s %22s %16s %18s"
          % ("R", "theta_top", "predicted R*theta", "measured delta", "theta_hat=delta/R"))
    for R, theta in ((0.60, 1.0), (0.60, 1.5), (0.60, 2.0),
                     (0.85, 1.0), (0.85, 1.5), (0.40, 2.0)):
        variety = [i0 * C ** R for C in SCALES]
        load = [cost * v ** theta for v in variety]
        delta = linfit(log_scales, [math.log(v) for v in load])[0]
        print("   %-8.2f %11.2f %22.4f %16.4f %18.4f"
              % (R, theta, R * theta, delta, delta / R))
    print()
    print("   Exact. So the throughput regression is the RIGHT estimator for the WRONG")
    print("   parameter: given an independent estimate of R it yields theta_top.")
    print("   One instrumented dataset therefore delivers both ceiling parameters --")
    print("   delay-versus-load gives mu, throughput-versus-scale gives theta_top.")
    print()

    print("=" * 78)
    print("D) Assembling the ceiling")
    print("=" * 78)
    print("   R_max = min(mu / theta_top, 1) = min(mu * R / delta, 1)")
    print()
    print("   %-8s %9s %11s %13s %11s" % ("mu", "delta", "R", "theta_top", "R_max"))
    for mu, delta, R in ((0.70, 0.90, 0.60), (0.70, 1.20, 0.60),
                         (1.00, 0.85, 0.85), (0.50, 1.00, 0.50)):
        theta = delta / R
        print("   %-8.2f %9.2f %11.2f %13.2f %11.3f"
              % (mu, delta, R, theta, min(mu / theta, 1.0)))
    print()
    print("   Sanity check: R must itself lie below the R_max it implies. Rows where")
    print("   R > R_max describe a system already past its dissolution ceiling.")
    print()
    print("=" * 78)
    print("E) The structural consequence")
    print("=" * 78)
    print("   mu is measurable only under stress, so a system far from its ceiling")
    print("   cannot locate it. The band's upper edge is intrinsically harder to observe")
    print("   than its lower edge, and systems will tend to discover their ceiling by")
    print("   reaching it.")
    print()
    print("   What IS observable throughout is utilisation rho, and rho grows as")
    print("   C^(delta-mu). So the operational early warning is not a measurement of mu")
    print("   but the TREND in rho -- which parallels the earlier finding that the")
    print("   derivative of R matters more than its level.")
    print()
    print("   This also explains why modularisation (raising theta_top's efficiency)")
    print("   must be triggered by rising delay rather than by knowing mu: delay is the")
    print("   only signal available before the ceiling is reached.")


if __name__ == "__main__":
    main()
