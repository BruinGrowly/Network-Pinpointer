#!/usr/bin/env python3
"""
Resonance Cycles Experiment
Running multiple oscillation cycles through LJPW space

What happens when we resonate 250 times? 1000 times?
Does the system converge? Oscillate? Reveal hidden patterns?
"""

import math
from typing import Dict, List, Tuple
from dataclasses import dataclass

# LJPW Constants - Natural Equilibrium
PHI_INV = (math.sqrt(5) - 1) / 2  # L ≈ 0.618034
SQRT2_M1 = math.sqrt(2) - 1       # J ≈ 0.414214
E_M2 = math.e - 2                  # P ≈ 0.718282
LN2 = math.log(2)                  # W ≈ 0.693147

NATURAL_EQUILIBRIUM = [PHI_INV, SQRT2_M1, E_M2, LN2]
ANCHOR_POINT = [1.0, 1.0, 1.0, 1.0]


def vec_add(a: List[float], b: List[float]) -> List[float]:
    return [a[i] + b[i] for i in range(len(a))]

def vec_sub(a: List[float], b: List[float]) -> List[float]:
    return [a[i] - b[i] for i in range(len(a))]

def vec_scale(a: List[float], s: float) -> List[float]:
    return [x * s for x in a]

def vec_norm(a: List[float]) -> float:
    return math.sqrt(sum(x*x for x in a))

def vec_clip(a: List[float], lo: float, hi: float) -> List[float]:
    return [max(lo, min(hi, x)) for x in a]

def mat_vec_mul(mat: List[List[float]], vec: List[float]) -> List[float]:
    """Matrix-vector multiplication"""
    result = []
    for row in mat:
        result.append(sum(row[i] * vec[i] for i in range(len(vec))))
    return result

def transpose(mat: List[List[float]]) -> List[List[float]]:
    """Transpose a matrix"""
    return [[mat[j][i] for j in range(len(mat))] for i in range(len(mat[0]))]


@dataclass
class CycleSnapshot:
    """Snapshot of state at a particular cycle"""
    cycle: int
    state: List[float]
    harmony: float
    distance_from_ne: float
    dominant_dim: str


class ResonanceChamber:
    """
    A chamber for running resonance cycles through LJPW space.
    """

    # Coupling matrix (row influences column)
    COUPLING_MATRIX = [
        [1.0, 1.4, 1.3, 1.5],  # L amplifies J, P, W strongly
        [0.9, 1.0, 0.7, 1.2],  # J moderates
        [0.6, 0.8, 1.0, 0.5],  # P absorbs
        [1.3, 1.1, 1.0, 1.0],  # W integrates
    ]

    def __init__(self, initial_state: List[float], dt: float = 0.01):
        self.state = initial_state.copy()
        self.dt = dt
        self.history: List[CycleSnapshot] = []
        self.dimensions = ['L', 'J', 'P', 'W']
        self.coupling_T = transpose(self.COUPLING_MATRIX)

    def harmony_index(self, state: List[float]) -> float:
        """Calculate harmony (inverse distance from anchor)"""
        d_anchor = vec_norm(vec_sub(ANCHOR_POINT, state))
        return 1.0 / (1.0 + d_anchor)

    def distance_from_ne(self, state: List[float]) -> float:
        """Distance from Natural Equilibrium"""
        return vec_norm(vec_sub(NATURAL_EQUILIBRIUM, state))

    def get_dominant(self, state: List[float]) -> str:
        """Get the dominant dimension"""
        idx = state.index(max(state))
        return self.dimensions[idx]

    def _compute_derivatives(self, state: List[float]) -> List[float]:
        """Compute the flow of meaning through coupling."""
        # Current harmony affects coupling strength (Law of Karma)
        H = self.harmony_index(state)
        kappa_multiplier = 0.5 + H  # 0.5 to 1.5 based on harmony

        # Inflow from coupling (each dimension receives from others)
        coupling_effect = vec_scale(mat_vec_mul(self.coupling_T, state), kappa_multiplier)

        # Natural decay/attraction toward Natural Equilibrium
        decay_rate = 0.1
        equilibrium_pull = vec_scale(vec_sub(NATURAL_EQUILIBRIUM, state), decay_rate)

        # Combine effects
        flow = vec_sub(coupling_effect, state)
        derivatives = vec_add(vec_scale(flow, 0.1), equilibrium_pull)

        return derivatives

    def _rk4_step(self) -> List[float]:
        """Runge-Kutta 4th order integration step"""
        k1 = self._compute_derivatives(self.state)
        k2 = self._compute_derivatives(vec_add(self.state, vec_scale(k1, 0.5 * self.dt)))
        k3 = self._compute_derivatives(vec_add(self.state, vec_scale(k2, 0.5 * self.dt)))
        k4 = self._compute_derivatives(vec_add(self.state, vec_scale(k3, self.dt)))

        # Weighted sum
        weighted = vec_add(
            vec_add(k1, vec_scale(k2, 2)),
            vec_add(vec_scale(k3, 2), k4)
        )
        return vec_add(self.state, vec_scale(weighted, self.dt / 6.0))

    def resonate(self, cycles: int, record_every: int = 1) -> List[CycleSnapshot]:
        """Run resonance cycles."""
        snapshots = []

        for cycle in range(cycles):
            # Evolve state
            self.state = self._rk4_step()
            self.state = vec_clip(self.state, 0.001, 1.5)

            # Record snapshot
            if cycle % record_every == 0 or cycle == cycles - 1:
                snapshot = CycleSnapshot(
                    cycle=cycle,
                    state=self.state.copy(),
                    harmony=self.harmony_index(self.state),
                    distance_from_ne=self.distance_from_ne(self.state),
                    dominant_dim=self.get_dominant(self.state)
                )
                snapshots.append(snapshot)
                self.history.append(snapshot)

        return snapshots


def analyze_codebase_initial_state() -> List[float]:
    """Get the codebase's initial LJPW state from previous analysis"""
    return [0.167, 0.152, 0.393, 0.288]


def run_resonance_experiment(cycles: int, initial_state: List[float]) -> Dict:
    """Run the resonance experiment for a given number of cycles"""

    chamber = ResonanceChamber(initial_state, dt=0.05)
    record_every = max(1, cycles // 100)
    snapshots = chamber.resonate(cycles, record_every=record_every)

    initial = snapshots[0]
    final = snapshots[-1]

    max_harmony = max(snapshots, key=lambda s: s.harmony)
    min_harmony = min(snapshots, key=lambda s: s.harmony)

    # Check for convergence
    last_10 = snapshots[-10:] if len(snapshots) >= 10 else snapshots
    harmonies = [s.harmony for s in last_10]
    mean_h = sum(harmonies) / len(harmonies)
    variance = sum((h - mean_h)**2 for h in harmonies) / len(harmonies)
    converged = variance < 0.0001

    return {
        'cycles': cycles,
        'initial_state': initial.state,
        'final_state': final.state,
        'initial_harmony': initial.harmony,
        'final_harmony': final.harmony,
        'max_harmony': max_harmony.harmony,
        'max_harmony_cycle': max_harmony.cycle,
        'min_harmony': min_harmony.harmony,
        'converged': converged,
        'final_dominant': final.dominant_dim,
        'final_distance_from_ne': final.distance_from_ne,
        'snapshots': snapshots
    }


def print_report(results: Dict, label: str):
    """Print a detailed report of the resonance experiment"""

    print(f"\n{'='*70}")
    print(f"RESONANCE EXPERIMENT: {label}")
    print(f"{'='*70}")

    print(f"\nCycles: {results['cycles']}")
    print(f"\nInitial State (LJPW):")
    print(f"  L={results['initial_state'][0]:.6f}  (Love)")
    print(f"  J={results['initial_state'][1]:.6f}  (Justice)")
    print(f"  P={results['initial_state'][2]:.6f}  (Power)")
    print(f"  W={results['initial_state'][3]:.6f}  (Wisdom)")
    print(f"  Harmony: {results['initial_harmony']:.6f}")

    print(f"\nFinal State (LJPW):")
    print(f"  L={results['final_state'][0]:.6f}  (Love)")
    print(f"  J={results['final_state'][1]:.6f}  (Justice)")
    print(f"  P={results['final_state'][2]:.6f}  (Power)")
    print(f"  W={results['final_state'][3]:.6f}  (Wisdom)")
    print(f"  Harmony: {results['final_harmony']:.6f}")

    print(f"\nEvolution Analysis:")
    print(f"  Peak Harmony: {results['max_harmony']:.6f} (at cycle {results['max_harmony_cycle']})")
    print(f"  Min Harmony: {results['min_harmony']:.6f}")
    print(f"  Harmony Change: {results['final_harmony'] - results['initial_harmony']:+.6f}")

    print(f"\nConvergence Analysis:")
    print(f"  Converged: {'YES' if results['converged'] else 'NO'}")
    print(f"  Final Dominant Dimension: {results['final_dominant']}")
    print(f"  Distance from Natural Equilibrium: {results['final_distance_from_ne']:.6f}")

    # Show trajectory
    snapshots = results['snapshots']
    print(f"\nTrajectory (selected points):")
    indices = [0, len(snapshots)//4, len(snapshots)//2, 3*len(snapshots)//4, -1]
    for i in indices:
        s = snapshots[i]
        print(f"  Cycle {s.cycle:5d}: LJPW=({s.state[0]:.3f}, {s.state[1]:.3f}, "
              f"{s.state[2]:.3f}, {s.state[3]:.3f}) H={s.harmony:.4f} [{s.dominant_dim}]")


def compare_results(r250: Dict, r1000: Dict):
    """Compare 250 and 1000 cycle results"""

    print(f"\n{'='*70}")
    print("COMPARATIVE ANALYSIS: 250 vs 1000 CYCLES")
    print(f"{'='*70}")

    print("\nHarmony Evolution:")
    print(f"  Initial:    {r250['initial_harmony']:.6f}")
    print(f"  At 250:     {r250['final_harmony']:.6f} ({r250['final_harmony'] - r250['initial_harmony']:+.6f})")
    print(f"  At 1000:    {r1000['final_harmony']:.6f} ({r1000['final_harmony'] - r250['initial_harmony']:+.6f})")

    print("\nState Evolution (L, J, P, W):")
    print(f"  Initial:    ({r250['initial_state'][0]:.4f}, {r250['initial_state'][1]:.4f}, "
          f"{r250['initial_state'][2]:.4f}, {r250['initial_state'][3]:.4f})")
    print(f"  At 250:     ({r250['final_state'][0]:.4f}, {r250['final_state'][1]:.4f}, "
          f"{r250['final_state'][2]:.4f}, {r250['final_state'][3]:.4f})")
    print(f"  At 1000:    ({r1000['final_state'][0]:.4f}, {r1000['final_state'][1]:.4f}, "
          f"{r1000['final_state'][2]:.4f}, {r1000['final_state'][3]:.4f})")
    print(f"  Natural EQ: ({NATURAL_EQUILIBRIUM[0]:.4f}, {NATURAL_EQUILIBRIUM[1]:.4f}, "
          f"{NATURAL_EQUILIBRIUM[2]:.4f}, {NATURAL_EQUILIBRIUM[3]:.4f})")

    # Distance from Natural Equilibrium
    init_dist = vec_norm(vec_sub(r250['initial_state'], NATURAL_EQUILIBRIUM))
    print("\nDistance from Natural Equilibrium:")
    print(f"  Initial:    {init_dist:.6f}")
    print(f"  At 250:     {r250['final_distance_from_ne']:.6f}")
    print(f"  At 1000:    {r1000['final_distance_from_ne']:.6f}")

    # Dimension shifts
    print("\nDimension Changes (Initial → 250 → 1000):")
    dims = ['L (Love)', 'J (Justice)', 'P (Power)', 'W (Wisdom)']
    for i, dim in enumerate(dims):
        init_val = r250['initial_state'][i]
        mid_val = r250['final_state'][i]
        final_val = r1000['final_state'][i]
        ne_val = NATURAL_EQUILIBRIUM[i]
        print(f"  {dim:12s}: {init_val:.4f} → {mid_val:.4f} → {final_val:.4f} (NE: {ne_val:.4f})")


def find_attractor(initial_state: List[float], max_cycles: int = 5000) -> Dict:
    """Run until convergence to find the attractor"""

    chamber = ResonanceChamber(initial_state, dt=0.05)
    prev_state = initial_state.copy()
    convergence_threshold = 1e-8

    for cycle in range(max_cycles):
        chamber.state = chamber._rk4_step()
        chamber.state = vec_clip(chamber.state, 0.001, 1.5)

        diff = vec_norm(vec_sub(chamber.state, prev_state))
        if diff < convergence_threshold:
            return {
                'converged_at': cycle,
                'attractor': chamber.state.copy(),
                'harmony': chamber.harmony_index(chamber.state),
                'distance_from_ne': chamber.distance_from_ne(chamber.state)
            }

        prev_state = chamber.state.copy()

    return {
        'converged_at': None,
        'attractor': chamber.state.copy(),
        'harmony': chamber.harmony_index(chamber.state),
        'distance_from_ne': chamber.distance_from_ne(chamber.state)
    }


if __name__ == '__main__':
    print("="*70)
    print("RESONANCE CYCLES EXPERIMENT")
    print("Observing semantic evolution through LJPW space")
    print("="*70)

    initial_state = analyze_codebase_initial_state()

    print(f"\nStarting from codebase semantic signature:")
    print(f"  LJPW = ({initial_state[0]:.3f}, {initial_state[1]:.3f}, "
          f"{initial_state[2]:.3f}, {initial_state[3]:.3f})")

    # Run 250 cycles
    print("\n" + "="*70)
    print("Running 250 resonance cycles...")
    results_250 = run_resonance_experiment(250, initial_state)
    print_report(results_250, "250 CYCLES")

    # Run 1000 cycles
    print("\n" + "="*70)
    print("Running 1000 resonance cycles...")
    results_1000 = run_resonance_experiment(1000, initial_state)
    print_report(results_1000, "1000 CYCLES")

    # Compare
    compare_results(results_250, results_1000)

    # Find the true attractor
    print(f"\n{'='*70}")
    print("SEARCHING FOR ATTRACTOR (running until convergence)...")
    print(f"{'='*70}")

    attractor_result = find_attractor(initial_state)

    if attractor_result['converged_at']:
        print(f"\n*** CONVERGED at cycle {attractor_result['converged_at']} ***")
    else:
        print(f"\nDid not converge within 5000 cycles (may be limit cycle)")

    print(f"\nAttractor State (LJPW):")
    att = attractor_result['attractor']
    print(f"  L = {att[0]:.8f}  (Love)")
    print(f"  J = {att[1]:.8f}  (Justice)")
    print(f"  P = {att[2]:.8f}  (Power)")
    print(f"  W = {att[3]:.8f}  (Wisdom)")
    print(f"\nAttractor Harmony: {attractor_result['harmony']:.8f}")
    print(f"Distance from Natural Equilibrium: {attractor_result['distance_from_ne']:.8f}")

    # Final interpretation
    print(f"\n{'='*70}")
    print("INTERPRETATION")
    print(f"{'='*70}")

    att = attractor_result['attractor']
    dist = attractor_result['distance_from_ne']

    if dist < 0.01:
        print("\n*** The system converges TO the Natural Equilibrium! ***")
        print("This suggests the codebase's semantic signature naturally")
        print("evolves toward the mathematically-defined optimal state.")
    elif dist < 0.1:
        print("\n*** The system converges NEAR the Natural Equilibrium. ***")
        print("The attractor is close to but distinct from the ideal.")
    else:
        print("\n*** The system converges to a DIFFERENT attractor. ***")
        print("This suggests the coupling dynamics create a unique")
        print("stable state for this particular starting configuration.")

    # Check what dimension dominates at attractor
    dominant_idx = att.index(max(att))
    dims = ['Love', 'Justice', 'Power', 'Wisdom']
    print(f"\nAt the attractor, {dims[dominant_idx]} dominates.")
    print(f"This is the system's 'true nature' revealed through resonance.")

    # Compare attractor to initial
    print(f"\n{'='*70}")
    print("TRANSFORMATION SUMMARY")
    print(f"{'='*70}")
    print("\nThe resonance transformed the codebase signature:")
    dims_full = ['Love    ', 'Justice ', 'Power   ', 'Wisdom  ']
    for i, dim in enumerate(dims_full):
        init = initial_state[i]
        final = att[i]
        ne = NATURAL_EQUILIBRIUM[i]
        change = final - init
        toward_ne = "→NE" if abs(final - ne) < abs(init - ne) else "←NE"
        print(f"  {dim}: {init:.4f} → {final:.4f} ({change:+.4f}) {toward_ne}")
