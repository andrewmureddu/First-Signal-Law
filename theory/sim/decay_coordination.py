"""
Coordination under a decaying status quo: numerical demonstration of t*.

Stag hunt with payoffs (own action vs opponent action):
    M[C][C] = R,  M[C][S] = L,  M[S][*] = s(t)
with R > s > L. The safe action S is payoff-independent of the opponent.

We show:
  (1) the trust threshold p*(t) = (s(t)-L)/(R-L) falls as s decays,
  (2) (C,C) becomes risk-dominant at t* where s(t*) = (R+L)/2,
  (3) a population stuck at all-S tips to all-C once t > t*, under
      replicator dynamics — confirming decay as an endogenous selection device.

No dependencies beyond numpy / matplotlib.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---- parameters ----------------------------------------------------------
R, L = 3.0, 0.0          # cooperate-vs-cooperate, cooperate-vs-safe (sucker)
s0 = 2.0                 # initial safe payoff
T = 200                  # horizon (periods)
x0 = 0.45                # initial cooperative mass, deliberately BELOW p*(0)
h = 0.25                 # replicator step size (erosion speed)

def s_lin(t, delta):     # linear decay, floored at L
    return np.maximum(s0 - delta * t, L)

# ---- analytic landmarks (reference decay rate) ---------------------------
delta_ref = 0.05
p_star = lambda t, d: (s_lin(t, d) - L) / (R - L)
t_star = (2 * s0 - R - L) / (2 * delta_ref)   # first time s(t) < (R+L)/2
print(f"reference delta          = {delta_ref}")
print(f"closed-form t*           = {t_star:.3f}")
print(f"p*(0) (trust needed now) = {p_star(0, delta_ref):.3f}  (x0={x0} starts below it)")
print(f"p*(t*) (should be 0.5)   = {p_star(t_star, delta_ref):.3f}")

# ---- replicator dynamics: the RACE between decay and erosion -------------
# x grows iff x > p*(t). The falling threshold sweeps the basin boundary down.
# A population starting BELOW p*(0) erodes at first; it is rescued only if the
# boundary drops past it before it collapses -- i.e. decay must outrun erosion.
def trajectory(x, delta):
    out = np.empty(T)
    for t in range(T):
        fC = x * R + (1 - x) * L
        x = min(max(x + h * x * (1 - x) * (fC - s_lin(t, delta)), 1e-9), 1 - 1e-9)
        out[t] = x
    return out

# (a) same starting mass, several decay rates -> a phase transition
rates = [0.02, 0.05, 0.12, 0.30]
trajs = {d: trajectory(x0, d) for d in rates}
for d, tr in trajs.items():
    print(f"delta={d:.2f}: final cooperation = {tr[-1]:.3f}  "
          f"-> {'RESCUED' if tr[-1] > 0.5 else 'eroded to S'}")

# (b) locate the critical decay rate for this x0 (smallest delta that rescues)
grid = np.linspace(0.0, 0.5, 251)
finals = np.array([trajectory(x0, d)[-1] for d in grid])
rescued = grid[finals > 0.5]
delta_crit = rescued.min() if rescued.size else float("nan")
print(f"critical decay rate for x0={x0}: delta_crit ~ {delta_crit:.3f}")

# Stochastic-stability note (Kandori-Mailath-Rob 1993; Young 1993): with
# persistent mutation the risk-dominant equilibrium is the unique long-run
# state in a 2x2 game. Since (C,C) turns risk-dominant at t*, a perturbed
# population selects cooperation for t > t* regardless of erosion speed --
# the race condition is specific to the unperturbed (deterministic) model.

# ---- figure --------------------------------------------------------------
tt = np.arange(T)
fig, ax = plt.subplots(3, 1, figsize=(7, 10))

ax[0].plot(tt, [p_star(t, delta_ref) for t in tt], lw=2, label="trust threshold p*(t)")
ax[0].axhline(0.5, ls=":", c="grey", label="risk-dominance switch (p*=1/2)")
ax[0].axvline(t_star, ls="--", c="crimson", label=f"t* = {t_star:.0f}")
ax[0].set_ylabel("confidence to cooperate")
ax[0].set_title(f"(1) Decay lowers the trust bar  (delta={delta_ref})")
ax[0].legend(fontsize=8); ax[0].set_ylim(0, 1); ax[0].set_xlabel("time t")

for d, tr in trajs.items():
    ax[1].plot(tt, tr, label=f"delta = {d:.2f}")
ax[1].axhline(x0, ls=":", c="grey", lw=1, label=f"start x0 = {x0}")
ax[1].set_ylabel("fraction playing C")
ax[1].set_title("(2) Same start, faster decay rescues cooperation")
ax[1].legend(fontsize=8); ax[1].set_ylim(0, 1); ax[1].set_xlabel("time t")

ax[2].plot(grid, finals, c="purple")
ax[2].axvline(delta_crit, ls="--", c="crimson", label=f"delta_crit ~ {delta_crit:.2f}")
ax[2].axhline(0.5, ls=":", c="grey")
ax[2].set_xlabel("decay rate delta"); ax[2].set_ylabel("final cooperation")
ax[2].set_title(f"(3) Phase transition in decay rate  (x0 = {x0})")
ax[2].legend(fontsize=8); ax[2].set_ylim(0, 1)

fig.tight_layout()
out = __file__.rsplit("/", 1)[0] + "/decay_coordination.png"
fig.savefig(out, dpi=130)
print(f"wrote {out}")
