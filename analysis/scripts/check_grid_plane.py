#!/usr/bin/env python3
"""Test whether the 'Black Hole Law Grid' a_min surface contains any curvature.

Fits an affine plane a_min = b0 + b1*r + b2*x using three cells, then reports the
maximum residual over the entire grid. A residual at machine epsilon means the
published contour plot is rendering a closed-form linear inequality, not a solved
field.

Run from the repository root:  python3 analysis/scripts/check_grid_plane.py
Standard library only.
"""

import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GRID = "a_min_grid__mid-theta_slice_.csv"


def main():
    rows = list(csv.reader(open(os.path.join(ROOT, GRID))))
    cols = [float(v) for v in rows[0][1:]]
    rvals = [float(row[0]) for row in rows[1:]]
    grid = [[float(v) for v in row[1:]] for row in rows[1:]]

    print("grid: %d rows (r = %.2f .. %.2f) x %d cols (x = %.2f .. %.2f) = %d cells"
          % (len(rvals), rvals[0], rvals[-1], len(cols), cols[0], cols[-1],
             len(rvals) * len(cols)))

    # Determine the plane from finite differences on the first row/column.
    b1 = (grid[1][0] - grid[0][0]) / (rvals[1] - rvals[0])
    b2 = (grid[0][1] - grid[0][0]) / (cols[1] - cols[0])
    b0 = grid[0][0] - b1 * rvals[0] - b2 * cols[0]

    worst = 0.0
    for i, rv in enumerate(rvals):
        for j, xv in enumerate(cols):
            resid = abs(grid[i][j] - (b0 + b1 * rv + b2 * xv))
            worst = max(worst, resid)

    lo = min(min(row) for row in grid)
    hi = max(max(row) for row in grid)

    print()
    print("  affine fit : a_min = %.4f + (%.3f)*r + (%.3f)*x" % (b0, b1, b2))
    print("  max |residual| over all cells : %.3e" % worst)
    print("  value range : %.3f .. %.3f" % (lo, hi))
    print()
    if worst < 1e-12:
        print("  => EXACTLY a plane, to machine precision. Zero curvature.")
        print("     No metric is solved and no black-hole physics is present in this file;")
        print("     the contour plot visualises a linear constraint.")
    if lo < 0:
        print("  => a_min goes negative (min %.3f). If a is a non-negative alignment weight," % lo)
        print("     the plotted region extends past the model's own domain of validity.")


if __name__ == "__main__":
    main()
