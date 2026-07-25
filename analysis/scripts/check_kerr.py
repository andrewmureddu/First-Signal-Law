#!/usr/bin/env python3
"""Verify the GR baselines in rebraided_prediction_slate.pdf and analyse r_b scaling.

Recomputes the Kerr outer horizon, prograde photon sphere and prograde ISCO from
standard closed forms and compares them against the values tabulated in the slate.
Then examines how the novel first-signal boundary r_b shifts with release zeta.

Run from anywhere:  python3 analysis/scripts/check_kerr.py
Standard library only.
"""

import math

# Values transcribed from rebraided_prediction_slate.pdf, table A.
# spin a*, r_+, r_ph, r_ISCO, r_b(zeta=0.0), r_b(zeta=0.3)
SLATE = [
    (0.50, 1.866, 2.347, 4.233, 2.409, 2.051),
    (0.90, 1.436, 1.558, 2.321, 1.943, 1.686),
    (0.99, 1.141, 1.168, 1.454, 1.611, 1.402),
]

# The arXiv draft (section 3.1) and the slate quote different slopes.
ARXIV_QUOTED = 0.3
SLATE_QUOTED = 0.916


def r_horizon(a):
    return 1.0 + math.sqrt(1.0 - a * a)


def r_photon_prograde(a):
    return 2.0 * (1.0 + math.cos((2.0 / 3.0) * math.acos(-a)))


def r_isco_prograde(a):
    z1 = 1.0 + (1.0 - a * a) ** (1.0 / 3.0) * ((1.0 + a) ** (1.0 / 3.0) + (1.0 - a) ** (1.0 / 3.0))
    z2 = math.sqrt(3.0 * a * a + z1 * z1)
    return 3.0 + z2 - math.sqrt((3.0 - z1) * (3.0 + z1 + 2.0 * z2))


def main():
    print("=" * 74)
    print("A) GR baselines: slate value vs recomputed Kerr")
    print("=" * 74)
    print("  %5s  %-18s %-18s %-18s" % ("a*", "r_+", "r_ph (prograde)", "r_ISCO (prograde)"))
    ok = True
    for a, rp, rph, risco, _, _ in SLATE:
        tp, tph, tisco = r_horizon(a), r_photon_prograde(a), r_isco_prograde(a)
        for claim, true in ((rp, tp), (rph, tph), (risco, tisco)):
            if abs(claim - true) > 5e-4:
                ok = False
        print("  %5.2f  %8.3f/%-9.3f %8.3f/%-9.3f %8.3f/%-9.3f"
              % (a, rp, tp, rph, tph, risco, tisco))
    print()
    print("  all three baselines match to the printed precision: %s" % ok)
    print("  => the GR scaffolding is genuine, not hand-waved.")
    print()

    print("=" * 74)
    print("B) The novel boundary r_b and its release shift")
    print("=" * 74)
    print("  %5s %9s %9s %14s %14s %14s"
          % ("a*", "r_b(0)", "r_b(.3)", "abs/unit z", "frac/unit z", "r_b - r_ISCO"))
    abs_shifts, frac_shifts = [], []
    for a, _, _, risco, b0, b3 in SLATE:
        abs_s = (b0 - b3) / 0.3
        frac_s = (b0 - b3) / b0 / 0.3
        abs_shifts.append(abs_s)
        frac_shifts.append(frac_s)
        print("  %5.2f %9.3f %9.3f %14.3f %14.3f %+14.3f"
              % (a, b0, b3, abs_s, frac_s, b0 - r_isco_prograde(a)))
    print()

    mean_abs = sum(abs_shifts) / len(abs_shifts)
    mean_frac = sum(frac_shifts) / len(frac_shifts)
    print("  mean absolute shift  : %.4f M per unit zeta  (slate quotes %.3f)" % (mean_abs, SLATE_QUOTED))
    print("  spread, absolute     : %.3fx  (%.3f .. %.3f)" % (max(abs_shifts) / min(abs_shifts),
                                                              min(abs_shifts), max(abs_shifts)))
    print("  mean fractional shift: %.4f per unit zeta" % mean_frac)
    print("  spread, fractional   : %.3fx" % (max(frac_shifts) / min(frac_shifts)))
    print()
    print("  => the shift is multiplicative, not additive: expressed fractionally the")
    print("     spread collapses from %.2fx to %.2fx. The defensible prediction is"
          % (max(abs_shifts) / min(abs_shifts), max(frac_shifts) / min(frac_shifts)))
    print("     'r_b contracts ~%.0f%% per unit zeta', not a single absolute figure in M."
          % (100 * mean_frac))
    print("  => r_b also changes side relative to the ISCO across this spin range")
    print("     (inside at a*=0.50, outside at a*=0.99), which needs a physical account.")
    print()

    print("=" * 74)
    print("C) Cross-document inconsistency in the headline GR prediction")
    print("=" * 74)
    mean_per_point3 = sum((b0 - b3) for _, _, _, _, b0, b3 in SLATE) / len(SLATE)
    print("  arXiv draft, section 3.1 : ~%.1f M per unit zeta  (rounded)" % ARXIV_QUOTED)
    print("  slate, table A           :  %.3f M per unit zeta" % SLATE_QUOTED)
    print("  ratio as quoted          :  %.2fx" % (SLATE_QUOTED / ARXIV_QUOTED))
    print()
    print("  mean shift per 0.3 zeta  :  %.4f  <- rounds to the arXiv's '~0.3'" % mean_per_point3)
    print("  %.4f / %.4f          :  %.3fx = exactly 1/0.3"
          % (mean_abs, mean_per_point3, mean_abs / mean_per_point3))
    print()
    print("  => the arXiv figure is the shift per 0.3 zeta mislabelled as per unit zeta.")
    print("     The two documents disagree by a factor of 1/0.3 on the headline GR")
    print("     prediction, and the erroneous form is the one in the abstract.")


if __name__ == "__main__":
    main()
