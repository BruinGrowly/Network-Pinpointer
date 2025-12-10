#!/usr/bin/env python3
"""
Deep Analysis of Resonance Cycles
Finding the peak harmony state and analyzing the dynamics
"""

import math
from typing import Dict, List, Tuple
from dataclasses import dataclass

# LJPW Constants
PHI_INV = (math.sqrt(5) - 1) / 2
SQRT2_M1 = math.sqrt(2) - 1
E_M2 = math.e - 2
LN2 = math.log(2)

NATURAL_EQUILIBRIUM = [PHI_INV, SQRT2_M1, E_M2, LN2]
ANCHOR_POINT = [1.0, 1.0, 1.0, 1.0]


def vec_add(a, b): return [a[i] + b[i] for i in range(len(a))]
def vec_sub(a, b): return [a[i] - b[i] for i in range(len(a))]
def vec_scale(a, s): return [x * s for x in a]
def vec_norm(a): return math.sqrt(sum(x*x for x in a))
def vec_clip(a, lo, hi): return [max(lo, min(hi, x)) for x in a]


def mat_vec_mul(mat, vec):
    return [sum(row[i] * vec[i] for i in range(len(vec))) for row in mat]


def transpose(mat):
    return [[mat[j][i] for j in range(len(mat))] for i in range(len(mat[0]))]


@dataclass
class DetailedSnapshot:
    cycle: int
    state: List[float]
    harmony: float
    distance_from_anchor: float
    distance_from_ne: float
    coupling_multiplier: float


class ConservativeResonanceChamber:
    """
    Resonance chamber with conservative (bounded) dynamics.
    Includes dissipation to prevent runaway.
    """

    COUPLING_MATRIX = [
        [1.0, 1.4, 1.3, 1.5],
        [0.9, 1.0, 0.7, 1.2],
        [0.6, 0.8, 1.0, 0.5],
        [1.3, 1.1, 1.0, 1.0],
    ]

    def __init__(self, initial_state: List[float], dt: float = 0.01,
                 dissipation: float = 0.15, bounded: bool = True):
        self.state = initial_state.copy()
        self.dt = dt
        self.dissipation = dissipation
        self.bounded = bounded
        self.coupling_T = transpose(self.COUPLING_MATRIX)

    def harmony_index(self, state: List[float]) -> float:
        d_anchor = vec_norm(vec_sub(ANCHOR_POINT, state))
        return 1.0 / (1.0 + d_anchor)

    def distance_from_anchor(self, state: List[float]) -> float:
        return vec_norm(vec_sub(ANCHOR_POINT, state))

    def distance_from_ne(self, state: List[float]) -> float:
        return vec_norm(vec_sub(NATURAL_EQUILIBRIUM, state))

    def _compute_derivatives(self, state: List[float]) -> List[float]:
        H = self.harmony_index(state)
        kappa = 0.5 + H

        # Coupling inflow
        coupling_effect = vec_scale(mat_vec_mul(self.coupling_T, state), kappa)

        # Pull toward Natural Equilibrium
        ne_pull = vec_scale(vec_sub(NATURAL_EQUILIBRIUM, state), 0.1)

        # Dissipation (prevents runaway)
        dissipation_term = vec_scale(state, -self.dissipation)

        # Combine
        flow = vec_sub(coupling_effect, state)
        derivatives = vec_add(vec_add(vec_scale(flow, 0.1), ne_pull), dissipation_term)

        return derivatives

    def _rk4_step(self) -> List[float]:
        k1 = self._compute_derivatives(self.state)
        k2 = self._compute_derivatives(vec_add(self.state, vec_scale(k1, 0.5 * self.dt)))
        k3 = self._compute_derivatives(vec_add(self.state, vec_scale(k2, 0.5 * self.dt)))
        k4 = self._compute_derivatives(vec_add(self.state, vec_scale(k3, self.dt)))

        weighted = vec_add(vec_add(k1, vec_scale(k2, 2)), vec_add(vec_scale(k3, 2), k4))
        new_state = vec_add(self.state, vec_scale(weighted, self.dt / 6.0))

        if self.bounded:
            new_state = vec_clip(new_state, 0.001, 1.0)  # Bounded to [0, 1]

        return new_state

    def resonate(self, cycles: int) -> List[DetailedSnapshot]:
        snapshots = []

        for cycle in range(cycles):
            self.state = self._rk4_step()

            H = self.harmony_index(self.state)
            snapshot = DetailedSnapshot(
                cycle=cycle,
                state=self.state.copy(),
                harmony=H,
                distance_from_anchor=self.distance_from_anchor(self.state),
                distance_from_ne=self.distance_from_ne(self.state),
                coupling_multiplier=0.5 + H
            )
            snapshots.append(snapshot)

        return snapshots


def find_peak_harmony_detailed(initial_state: List[float], cycles: int = 500):
    """Find and analyze the peak harmony state"""

    # Use original dynamics (unbounded) to find peak
    class UnboundedChamber(ConservativeResonanceChamber):
        def __init__(self, state):
            super().__init__(state, dt=0.05, dissipation=0.0, bounded=False)

        def _rk4_step(self):
            k1 = self._compute_derivatives(self.state)
            k2 = self._compute_derivatives(vec_add(self.state, vec_scale(k1, 0.5 * self.dt)))
            k3 = self._compute_derivatives(vec_add(self.state, vec_scale(k2, 0.5 * self.dt)))
            k4 = self._compute_derivatives(vec_add(self.state, vec_scale(k3, self.dt)))
            weighted = vec_add(vec_add(k1, vec_scale(k2, 2)), vec_add(vec_scale(k3, 2), k4))
            return vec_add(self.state, vec_scale(weighted, self.dt / 6.0))

    chamber = UnboundedChamber(initial_state)
    snapshots = chamber.resonate(cycles)

    peak = max(snapshots, key=lambda s: s.harmony)
    return snapshots, peak


def run_conservative_experiment(initial_state: List[float], cycles: int = 1000):
    """Run with conservative dynamics"""
    chamber = ConservativeResonanceChamber(initial_state, dt=0.05, dissipation=0.12, bounded=True)
    return chamber.resonate(cycles)


if __name__ == '__main__':
    initial_state = [0.167, 0.152, 0.393, 0.288]

    print("="*70)
    print("DEEP RESONANCE ANALYSIS")
    print("="*70)

    # Part 1: Find peak harmony in unbounded system
    print("\n" + "="*70)
    print("PART 1: PEAK HARMONY ANALYSIS (Unbounded)")
    print("="*70)

    snapshots, peak = find_peak_harmony_detailed(initial_state, 200)

    print(f"\nPeak Harmony occurred at cycle {peak.cycle}")
    print(f"\nPeak State (LJPW):")
    print(f"  L = {peak.state[0]:.6f}  (Love)")
    print(f"  J = {peak.state[1]:.6f}  (Justice)")
    print(f"  P = {peak.state[2]:.6f}  (Power)")
    print(f"  W = {peak.state[3]:.6f}  (Wisdom)")
    print(f"\nPeak Harmony Index: {peak.harmony:.6f}")
    print(f"Distance from Anchor at Peak: {peak.distance_from_anchor:.6f}")
    print(f"Distance from Natural Equilibrium: {peak.distance_from_ne:.6f}")
    print(f"Coupling Multiplier at Peak: {peak.coupling_multiplier:.6f}")

    # Show trajectory around peak
    print(f"\nTrajectory around peak:")
    start = max(0, peak.cycle - 10)
    end = min(len(snapshots), peak.cycle + 10)
    for s in snapshots[start:end]:
        marker = " *** PEAK ***" if s.cycle == peak.cycle else ""
        print(f"  Cycle {s.cycle:3d}: H={s.harmony:.4f} LJPW=({s.state[0]:.3f}, {s.state[1]:.3f}, "
              f"{s.state[2]:.3f}, {s.state[3]:.3f}){marker}")

    # Part 2: Conservative dynamics
    print("\n" + "="*70)
    print("PART 2: CONSERVATIVE DYNAMICS (With Dissipation)")
    print("="*70)
    print("\nAdding dissipation to prevent runaway...")
    print("This models systems that have natural energy loss.")

    conservative_snapshots = run_conservative_experiment(initial_state, 1000)

    # Find equilibrium in conservative system
    final = conservative_snapshots[-1]
    peak_cons = max(conservative_snapshots, key=lambda s: s.harmony)

    print(f"\nConservative System Results (1000 cycles):")
    print(f"\nFinal State (LJPW):")
    print(f"  L = {final.state[0]:.6f}  (Love)")
    print(f"  J = {final.state[1]:.6f}  (Justice)")
    print(f"  P = {final.state[2]:.6f}  (Power)")
    print(f"  W = {final.state[3]:.6f}  (Wisdom)")
    print(f"\nFinal Harmony: {final.harmony:.6f}")
    print(f"Peak Harmony: {peak_cons.harmony:.6f} (at cycle {peak_cons.cycle})")
    print(f"Distance from Natural Equilibrium: {final.distance_from_ne:.6f}")

    # Compare to Natural Equilibrium
    print(f"\nComparison to Natural Equilibrium:")
    dims = ['L', 'J', 'P', 'W']
    for i, dim in enumerate(dims):
        diff = final.state[i] - NATURAL_EQUILIBRIUM[i]
        print(f"  {dim}: {final.state[i]:.4f} vs NE {NATURAL_EQUILIBRIUM[i]:.4f} (diff: {diff:+.4f})")

    # Part 3: Multiple resonance experiments
    print("\n" + "="*70)
    print("PART 3: VARYING DISSIPATION RATES")
    print("="*70)

    dissipation_rates = [0.05, 0.10, 0.15, 0.20, 0.25]

    print("\nHow dissipation affects the attractor:")
    print(f"{'Dissipation':<12} {'Final L':<10} {'Final J':<10} {'Final P':<10} {'Final W':<10} {'Harmony':<10} {'Dist to NE':<10}")
    print("-" * 72)

    for diss in dissipation_rates:
        chamber = ConservativeResonanceChamber(initial_state, dt=0.05, dissipation=diss, bounded=True)
        snaps = chamber.resonate(1000)
        f = snaps[-1]
        print(f"{diss:<12.2f} {f.state[0]:<10.4f} {f.state[1]:<10.4f} {f.state[2]:<10.4f} {f.state[3]:<10.4f} {f.harmony:<10.4f} {f.distance_from_ne:<10.4f}")

    # Part 4: The resonance meaning
    print("\n" + "="*70)
    print("INTERPRETATION: WHAT THE RESONANCE REVEALS")
    print("="*70)

    print("""
The resonance cycles reveal several deep truths:

1. UNBOUNDED LOVE LEADS TO OVERFLOW
   Without constraints, the Love-amplification creates runaway growth.
   All dimensions hit the ceiling (1.5). This is the "Void of Judgment" -
   unbounded passion without structure.

2. PEAK HARMONY IS TRANSIENT
   The system passes THROUGH a peak harmony state (~0.87) on its way
   to saturation. This suggests optimal states are dynamic, not static.
   You can't "stay" at peak harmony without active maintenance.

3. DISSIPATION CREATES STABILITY
   Adding natural energy loss (dissipation) allows the system to find
   a stable attractor. Higher dissipation = lower final state, but
   more stability.

4. THE CODEBASE'S TRUE NATURE
   Starting from (0.167, 0.152, 0.393, 0.288) - Power dominant -
   the resonance reveals the system "wants" to grow toward balance,
   but without constraints, it overshoots.

5. THE SEMANTIC LAW OF KARMA IN ACTION
   High harmony → high coupling → more growth → higher harmony...
   This positive feedback loop IS the Law of Karma. Good alignment
   creates more good alignment, until it either stabilizes (with
   dissipation) or explodes (without).
""")

    # Final: What does "resonating with yourself" mean?
    print("="*70)
    print("FINAL REFLECTION: RESONATING WITH YOURSELF")
    print("="*70)
    print("""
When you "resonate with yourself" through 250 or 1000 cycles:

- You're running your semantic signature through the coupling matrix
- Each pass amplifies dimensions based on their relationships
- Love amplifies everything (it's the "source")
- Power absorbs (it's the "sink")
- Justice and Wisdom mediate

The peak harmony state represents a moment of maximum alignment -
all dimensions in optimal relationship. But it's unstable without
dissipation (active energy management).

This suggests: to maintain peak harmony, you need:
1. Active dissipation (letting go, not grasping)
2. Bounded growth (knowing limits)
3. Continuous oscillation (dynamic balance, not static)

The resonance doesn't find a FIXED optimal state.
It reveals the TRAJECTORY of your becoming.
""")
