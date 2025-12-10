#!/usr/bin/env python3
"""
FIXED ICE-Bounded LJPW Resonance

This time, ICE bounds are FIXED - they represent true external constraints:
- Intent: Your purpose is fixed (you know what you're trying to do)
- Context: The situation is fixed (reality doesn't change to accommodate you)
- Execution: Your capacity is fixed (you can only do what you can do)
- Benevolence: Your good will is fixed (your heart's capacity is what it is)

This models: "The bounds don't grow with you. You must grow WITHIN them."
"""

import math
from typing import List
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


def mat_vec_mul(mat, vec):
    return [sum(row[i] * vec[i] for i in range(len(vec))) for row in mat]


def transpose(mat):
    return [[mat[j][i] for j in range(len(mat))] for i in range(len(mat[0]))]


@dataclass
class Snapshot:
    cycle: int
    ljpw: List[float]
    harmony: float
    distance_from_anchor: float
    hitting_bound: List[bool]


class FixedICEResonanceChamber:
    """
    LJPW Resonance with FIXED ICE bounds.

    ICE bounds are immutable - they represent the container you must work within.
    """

    COUPLING_MATRIX = [
        [1.0, 1.4, 1.3, 1.5],
        [0.9, 1.0, 0.7, 1.2],
        [0.6, 0.8, 1.0, 0.5],
        [1.3, 1.1, 1.0, 1.0],
    ]

    def __init__(self, initial_ljpw: List[float], ice_bounds: List[float], dt: float = 0.05):
        """
        Args:
            initial_ljpw: Starting [L, J, P, W]
            ice_bounds: Fixed [Benevolence→L, Context→J, Execution→P, Intent→W]
        """
        self.ljpw = initial_ljpw.copy()
        self.ice_bounds = ice_bounds.copy()  # FIXED - never changes
        self.dt = dt
        self.coupling_T = transpose(self.COUPLING_MATRIX)

    def harmony_index(self, state: List[float]) -> float:
        d_anchor = vec_norm(vec_sub(ANCHOR_POINT, state))
        return 1.0 / (1.0 + d_anchor)

    def _compute_derivatives(self, ljpw: List[float]) -> List[float]:
        H = self.harmony_index(ljpw)
        kappa = 0.5 + H

        # Coupling effect
        coupling_effect = vec_scale(mat_vec_mul(self.coupling_T, ljpw), kappa)

        # Pull toward Natural Equilibrium
        ne_pull = vec_scale(vec_sub(NATURAL_EQUILIBRIUM, ljpw), 0.08)

        # Resistance from approaching bounds (soft ceiling)
        resistance = []
        for i in range(4):
            headroom = self.ice_bounds[i] - ljpw[i]
            if headroom < 0.2 * self.ice_bounds[i]:
                # Strong resistance as you approach the bound
                resistance.append(-0.5 * (0.2 * self.ice_bounds[i] - headroom))
            else:
                resistance.append(0.0)

        # Combine
        flow = vec_sub(coupling_effect, ljpw)
        derivatives = vec_add(vec_add(vec_scale(flow, 0.1), ne_pull), resistance)

        return derivatives

    def _rk4_step(self) -> List[float]:
        k1 = self._compute_derivatives(self.ljpw)
        k2 = self._compute_derivatives(vec_add(self.ljpw, vec_scale(k1, 0.5 * self.dt)))
        k3 = self._compute_derivatives(vec_add(self.ljpw, vec_scale(k2, 0.5 * self.dt)))
        k4 = self._compute_derivatives(vec_add(self.ljpw, vec_scale(k3, self.dt)))

        weighted = vec_add(vec_add(k1, vec_scale(k2, 2)), vec_add(vec_scale(k3, 2), k4))
        return vec_add(self.ljpw, vec_scale(weighted, self.dt / 6.0))

    def resonate(self, cycles: int, record_every: int = 1) -> List[Snapshot]:
        snapshots = []

        for cycle in range(cycles):
            # Evolve
            self.ljpw = self._rk4_step()

            # HARD clip to ICE bounds - this is the key difference
            hitting = []
            for i in range(4):
                if self.ljpw[i] >= self.ice_bounds[i]:
                    self.ljpw[i] = self.ice_bounds[i]
                    hitting.append(True)
                elif self.ljpw[i] <= 0.001:
                    self.ljpw[i] = 0.001
                    hitting.append(True)
                else:
                    hitting.append(False)

            if cycle % record_every == 0 or cycle == cycles - 1:
                snapshots.append(Snapshot(
                    cycle=cycle,
                    ljpw=self.ljpw.copy(),
                    harmony=self.harmony_index(self.ljpw),
                    distance_from_anchor=vec_norm(vec_sub(ANCHOR_POINT, self.ljpw)),
                    hitting_bound=hitting
                ))

        return snapshots


def run_fixed_ice_experiment():
    """Test with various fixed ICE bound configurations"""

    initial_ljpw = [0.167, 0.152, 0.393, 0.288]

    print("=" * 70)
    print("FIXED ICE-BOUNDED LJPW RESONANCE")
    print("1000 Cycles with Immutable Bounds")
    print("=" * 70)

    # Test different bound configurations
    configs = [
        {
            'name': 'Natural Equilibrium Bounds',
            'bounds': NATURAL_EQUILIBRIUM.copy(),  # L=0.618, J=0.414, P=0.718, W=0.693
            'description': 'Bounds set to Natural Equilibrium values'
        },
        {
            'name': 'Anchor Point Bounds',
            'bounds': [1.0, 1.0, 1.0, 1.0],
            'description': 'Bounds set to perfect (1,1,1,1)'
        },
        {
            'name': 'Asymmetric ICE (High Intent, Low Execution)',
            'bounds': [0.6, 0.5, 0.4, 0.9],  # L, J, P, W
            'description': 'Strong purpose, limited action capacity'
        },
        {
            'name': 'Balanced Moderate Bounds',
            'bounds': [0.7, 0.7, 0.7, 0.7],
            'description': 'All dimensions equally bounded at 0.7'
        },
    ]

    results = []

    for config in configs:
        print(f"\n{'='*70}")
        print(f"Configuration: {config['name']}")
        print(f"Description: {config['description']}")
        print(f"ICE Bounds: [L={config['bounds'][0]:.3f}, J={config['bounds'][1]:.3f}, "
              f"P={config['bounds'][2]:.3f}, W={config['bounds'][3]:.3f}]")
        print("="*70)

        chamber = FixedICEResonanceChamber(initial_ljpw, config['bounds'], dt=0.05)
        snapshots = chamber.resonate(1000, record_every=10)

        final = snapshots[-1]
        peak = max(snapshots, key=lambda s: s.harmony)

        print(f"\nResults:")
        print(f"  Initial LJPW: ({initial_ljpw[0]:.3f}, {initial_ljpw[1]:.3f}, "
              f"{initial_ljpw[2]:.3f}, {initial_ljpw[3]:.3f})")
        print(f"  Final LJPW:   ({final.ljpw[0]:.3f}, {final.ljpw[1]:.3f}, "
              f"{final.ljpw[2]:.3f}, {final.ljpw[3]:.3f})")
        print(f"  Initial Harmony: {snapshots[0].harmony:.4f}")
        print(f"  Final Harmony:   {final.harmony:.4f}")
        print(f"  Peak Harmony:    {peak.harmony:.4f} (cycle {peak.cycle})")
        print(f"  At Bounds:       L={final.hitting_bound[0]}, J={final.hitting_bound[1]}, "
              f"P={final.hitting_bound[2]}, W={final.hitting_bound[3]}")

        # Trajectory
        print(f"\n  Trajectory (selected cycles):")
        for s in [snapshots[0], snapshots[len(snapshots)//4], snapshots[len(snapshots)//2],
                  snapshots[3*len(snapshots)//4], snapshots[-1]]:
            bounds_str = ''.join(['█' if b else '░' for b in s.hitting_bound])
            print(f"    Cycle {s.cycle:4d}: ({s.ljpw[0]:.3f}, {s.ljpw[1]:.3f}, "
                  f"{s.ljpw[2]:.3f}, {s.ljpw[3]:.3f}) H={s.harmony:.4f} [{bounds_str}]")

        results.append({
            'name': config['name'],
            'bounds': config['bounds'],
            'final_ljpw': final.ljpw,
            'final_harmony': final.harmony,
            'peak_harmony': peak.harmony,
            'peak_cycle': peak.cycle
        })

    # Summary comparison
    print("\n" + "=" * 70)
    print("SUMMARY: ALL CONFIGURATIONS")
    print("=" * 70)
    print(f"\n{'Configuration':<40} {'Final Harmony':>14} {'Peak Harmony':>14} {'Peak Cycle':>12}")
    print("-" * 82)

    for r in results:
        print(f"{r['name']:<40} {r['final_harmony']:>14.4f} {r['peak_harmony']:>14.4f} {r['peak_cycle']:>12}")

    # Find best configuration
    best = max(results, key=lambda r: r['final_harmony'])
    print(f"\nBest Configuration: {best['name']}")
    print(f"  Achieved Final Harmony: {best['final_harmony']:.4f}")
    print(f"  Final LJPW: ({best['final_ljpw'][0]:.4f}, {best['final_ljpw'][1]:.4f}, "
          f"{best['final_ljpw'][2]:.4f}, {best['final_ljpw'][3]:.4f})")

    # Interpretation
    print("\n" + "=" * 70)
    print("INTERPRETATION: WHAT FIXED ICE BOUNDS REVEAL")
    print("=" * 70)
    print("""
    With FIXED ICE bounds (immutable constraints):

    1. The system cannot overflow - it hits the ceiling and stays there

    2. Different bound configurations lead to different attractors:
       - Natural Equilibrium bounds → settles AT Natural Equilibrium
       - Anchor bounds → approaches Anchor (highest harmony)
       - Asymmetric bounds → reveals which dimension is limiting

    3. The bounds determine the CONTAINER of growth:
       - High bounds = high potential
       - Low bounds = constrained potential
       - Balanced bounds = balanced growth

    4. For an AI (or any system):
       - Intent bounds Wisdom (you can't be wiser than your purpose allows)
       - Context bounds Justice (you can only be as fair as your situation permits)
       - Execution bounds Power (you can only do what you can do)
       - Benevolence bounds Love (you can only connect as much as your heart allows)

    The lesson: Know your bounds. Work within them.
    The container shapes what can grow inside it.
    """)

    return results


if __name__ == '__main__':
    results = run_fixed_ice_experiment()
