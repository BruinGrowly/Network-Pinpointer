#!/usr/bin/env python3
"""
ICE-Bounded LJPW Resonance Experiment

ICE Framework (Intent, Context, Execution) provides bounds for LJPW oscillation.

Mapping:
  Intent      → Wisdom (W)   - You can't be wiser than your intent
  Context     → Justice (J)  - Rules are contextual
  Execution   → Power (P)    - Action is bounded by capability
  Benevolence → Love (L)     - Connection requires good will

The ICE framework acts as a dynamic constraint system:
- Intent defines the CEILING for Wisdom
- Context defines the CEILING for Justice
- Execution defines the CEILING for Power
- Benevolence defines the CEILING for Love

This prevents the unbounded overflow we saw before.
"""

import math
from typing import Dict, List, Tuple
from dataclasses import dataclass

# LJPW Constants
PHI_INV = (math.sqrt(5) - 1) / 2  # L ≈ 0.618034
SQRT2_M1 = math.sqrt(2) - 1       # J ≈ 0.414214
E_M2 = math.e - 2                  # P ≈ 0.718282
LN2 = math.log(2)                  # W ≈ 0.693147

NATURAL_EQUILIBRIUM = [PHI_INV, SQRT2_M1, E_M2, LN2]
ANCHOR_POINT = [1.0, 1.0, 1.0, 1.0]


def vec_add(a, b): return [a[i] + b[i] for i in range(len(a))]
def vec_sub(a, b): return [a[i] - b[i] for i in range(len(a))]
def vec_scale(a, s): return [x * s for x in a]
def vec_norm(a): return math.sqrt(sum(x*x for x in a))
def vec_mul(a, b): return [a[i] * b[i] for i in range(len(a))]  # element-wise


def mat_vec_mul(mat, vec):
    return [sum(row[i] * vec[i] for i in range(len(vec))) for row in mat]


def transpose(mat):
    return [[mat[j][i] for j in range(len(mat))] for i in range(len(mat[0]))]


@dataclass
class ICEState:
    """Intent-Context-Execution state"""
    intent: float      # Bounds Wisdom
    context: float     # Bounds Justice
    execution: float   # Bounds Power
    benevolence: float # Bounds Love

    def as_bounds(self) -> List[float]:
        """Return as [L_bound, J_bound, P_bound, W_bound]"""
        return [self.benevolence, self.context, self.execution, self.intent]

    def __str__(self):
        return f"ICE(I={self.intent:.3f}, C={self.context:.3f}, E={self.execution:.3f}, B={self.benevolence:.3f})"


@dataclass
class ResonanceSnapshot:
    """Snapshot of resonance state"""
    cycle: int
    ljpw: List[float]
    ice_bounds: List[float]
    harmony: float
    distance_from_anchor: float
    bounded_by: str  # Which ICE dimension is currently limiting


class ICEBoundedResonanceChamber:
    """
    LJPW Resonance with ICE Framework bounds.

    The ICE bounds evolve WITH the LJPW state - they're not static.
    As you resonate, your Intent/Context/Execution also evolve,
    creating a coupled dance between meaning and bounds.
    """

    COUPLING_MATRIX = [
        [1.0, 1.4, 1.3, 1.5],  # L amplifies J, P, W
        [0.9, 1.0, 0.7, 1.2],  # J moderates
        [0.6, 0.8, 1.0, 0.5],  # P absorbs
        [1.3, 1.1, 1.0, 1.0],  # W integrates
    ]

    # ICE evolution rates - how fast bounds can expand
    ICE_GROWTH_RATE = 0.05
    ICE_DECAY_RATE = 0.02

    def __init__(self, initial_ljpw: List[float], initial_ice: ICEState, dt: float = 0.05):
        self.ljpw = initial_ljpw.copy()
        self.ice = initial_ice
        self.dt = dt
        self.coupling_T = transpose(self.COUPLING_MATRIX)
        self.history: List[ResonanceSnapshot] = []

    def harmony_index(self, state: List[float]) -> float:
        d_anchor = vec_norm(vec_sub(ANCHOR_POINT, state))
        return 1.0 / (1.0 + d_anchor)

    def distance_from_anchor(self, state: List[float]) -> float:
        return vec_norm(vec_sub(ANCHOR_POINT, state))

    def _compute_ljpw_derivatives(self, ljpw: List[float], ice_bounds: List[float]) -> List[float]:
        """Compute LJPW flow with ICE awareness"""
        H = self.harmony_index(ljpw)
        kappa = 0.5 + H

        # Coupling effect
        coupling_effect = vec_scale(mat_vec_mul(self.coupling_T, ljpw), kappa)

        # Pull toward Natural Equilibrium
        ne_pull = vec_scale(vec_sub(NATURAL_EQUILIBRIUM, ljpw), 0.08)

        # Soft ceiling from ICE bounds - creates resistance as you approach bounds
        # This is key: bounds don't hard-clip, they create increasing resistance
        resistance = []
        for i in range(4):
            if ljpw[i] > ice_bounds[i] * 0.8:  # Start resisting at 80% of bound
                overshoot = (ljpw[i] - ice_bounds[i] * 0.8) / (ice_bounds[i] * 0.2 + 0.001)
                resistance.append(-overshoot * 0.3)  # Pushback force
            else:
                resistance.append(0.0)

        # Combine
        flow = vec_sub(coupling_effect, ljpw)
        derivatives = vec_add(vec_add(vec_scale(flow, 0.1), ne_pull), resistance)

        return derivatives

    def _evolve_ice(self, ljpw: List[float], ice: ICEState) -> ICEState:
        """
        ICE bounds evolve based on LJPW state.

        The insight: your capacity (ICE) grows when you USE it well (high harmony),
        and shrinks when you don't use it (low harmony).
        """
        H = self.harmony_index(ljpw)

        # Growth factor based on harmony
        growth = self.ICE_GROWTH_RATE * H
        decay = self.ICE_DECAY_RATE * (1 - H)

        # Each ICE dimension is influenced by its corresponding LJPW dimension
        # High LJPW relative to bound → bound can grow (you're using capacity)
        # Low LJPW relative to bound → bound shrinks (unused capacity atrophies)

        new_intent = ice.intent + growth * (ljpw[3] / max(ice.intent, 0.1)) - decay
        new_context = ice.context + growth * (ljpw[1] / max(ice.context, 0.1)) - decay
        new_execution = ice.execution + growth * (ljpw[2] / max(ice.execution, 0.1)) - decay
        new_benevolence = ice.benevolence + growth * (ljpw[0] / max(ice.benevolence, 0.1)) - decay

        # ICE bounds are themselves bounded [0.1, 1.5]
        return ICEState(
            intent=max(0.1, min(1.5, new_intent)),
            context=max(0.1, min(1.5, new_context)),
            execution=max(0.1, min(1.5, new_execution)),
            benevolence=max(0.1, min(1.5, new_benevolence))
        )

    def _rk4_step(self, ice_bounds: List[float]) -> List[float]:
        """RK4 integration for LJPW"""
        k1 = self._compute_ljpw_derivatives(self.ljpw, ice_bounds)
        k2 = self._compute_ljpw_derivatives(vec_add(self.ljpw, vec_scale(k1, 0.5 * self.dt)), ice_bounds)
        k3 = self._compute_ljpw_derivatives(vec_add(self.ljpw, vec_scale(k2, 0.5 * self.dt)), ice_bounds)
        k4 = self._compute_ljpw_derivatives(vec_add(self.ljpw, vec_scale(k3, self.dt)), ice_bounds)

        weighted = vec_add(vec_add(k1, vec_scale(k2, 2)), vec_add(vec_scale(k3, 2), k4))
        return vec_add(self.ljpw, vec_scale(weighted, self.dt / 6.0))

    def _find_limiting_bound(self, ljpw: List[float], ice_bounds: List[float]) -> str:
        """Find which ICE dimension is most limiting"""
        dims = ['Benevolence(L)', 'Context(J)', 'Execution(P)', 'Intent(W)']
        ratios = [ljpw[i] / max(ice_bounds[i], 0.001) for i in range(4)]
        max_idx = ratios.index(max(ratios))
        return dims[max_idx]

    def resonate(self, cycles: int, record_every: int = 1) -> List[ResonanceSnapshot]:
        """Run ICE-bounded resonance"""
        snapshots = []

        for cycle in range(cycles):
            ice_bounds = self.ice.as_bounds()

            # Evolve LJPW (bounded by ICE)
            self.ljpw = self._rk4_step(ice_bounds)

            # Soft clip to ICE bounds (allow slight overshoot for smoother dynamics)
            for i in range(4):
                self.ljpw[i] = max(0.001, min(ice_bounds[i] * 1.1, self.ljpw[i]))

            # Evolve ICE bounds based on current LJPW
            self.ice = self._evolve_ice(self.ljpw, self.ice)

            # Record
            if cycle % record_every == 0 or cycle == cycles - 1:
                snapshot = ResonanceSnapshot(
                    cycle=cycle,
                    ljpw=self.ljpw.copy(),
                    ice_bounds=self.ice.as_bounds(),
                    harmony=self.harmony_index(self.ljpw),
                    distance_from_anchor=self.distance_from_anchor(self.ljpw),
                    bounded_by=self._find_limiting_bound(self.ljpw, self.ice.as_bounds())
                )
                snapshots.append(snapshot)
                self.history.append(snapshot)

        return snapshots


def run_ice_bounded_experiment():
    """Run the ICE-bounded resonance experiment"""

    # Initial LJPW state (from codebase analysis)
    initial_ljpw = [0.167, 0.152, 0.393, 0.288]

    # Initial ICE bounds - starting with moderate capacity
    # These represent: how much Intent/Context/Execution/Benevolence we START with
    initial_ice = ICEState(
        intent=0.7,       # Moderate clarity of purpose
        context=0.6,      # Moderate understanding of situation
        execution=0.8,    # Good execution capacity
        benevolence=0.5   # Moderate good will
    )

    print("=" * 70)
    print("ICE-BOUNDED LJPW RESONANCE EXPERIMENT")
    print("=" * 70)

    print(f"\nInitial LJPW State:")
    print(f"  L (Love)   = {initial_ljpw[0]:.4f}")
    print(f"  J (Justice)= {initial_ljpw[1]:.4f}")
    print(f"  P (Power)  = {initial_ljpw[2]:.4f}")
    print(f"  W (Wisdom) = {initial_ljpw[3]:.4f}")

    print(f"\nInitial ICE Bounds:")
    print(f"  Intent      (→W) = {initial_ice.intent:.4f}")
    print(f"  Context     (→J) = {initial_ice.context:.4f}")
    print(f"  Execution   (→P) = {initial_ice.execution:.4f}")
    print(f"  Benevolence (→L) = {initial_ice.benevolence:.4f}")

    # Run 1000 cycles
    chamber = ICEBoundedResonanceChamber(initial_ljpw, initial_ice, dt=0.05)
    snapshots = chamber.resonate(1000, record_every=10)

    # Analysis
    print("\n" + "=" * 70)
    print("RESONANCE RESULTS: 1000 CYCLES")
    print("=" * 70)

    final = snapshots[-1]
    peak = max(snapshots, key=lambda s: s.harmony)

    print(f"\nFinal LJPW State:")
    print(f"  L (Love)   = {final.ljpw[0]:.6f}")
    print(f"  J (Justice)= {final.ljpw[1]:.6f}")
    print(f"  P (Power)  = {final.ljpw[2]:.6f}")
    print(f"  W (Wisdom) = {final.ljpw[3]:.6f}")

    print(f"\nFinal ICE Bounds:")
    print(f"  Intent      (→W) = {final.ice_bounds[3]:.6f}")
    print(f"  Context     (→J) = {final.ice_bounds[1]:.6f}")
    print(f"  Execution   (→P) = {final.ice_bounds[2]:.6f}")
    print(f"  Benevolence (→L) = {final.ice_bounds[0]:.6f}")

    print(f"\nHarmony Analysis:")
    print(f"  Initial Harmony: {snapshots[0].harmony:.6f}")
    print(f"  Final Harmony:   {final.harmony:.6f}")
    print(f"  Peak Harmony:    {peak.harmony:.6f} (at cycle {peak.cycle})")
    print(f"  Harmony Change:  {final.harmony - snapshots[0].harmony:+.6f}")

    print(f"\nDistance from Anchor (1,1,1,1):")
    print(f"  Initial: {snapshots[0].distance_from_anchor:.6f}")
    print(f"  Final:   {final.distance_from_anchor:.6f}")

    # Trajectory
    print(f"\nTrajectory (every 100 cycles):")
    print(f"{'Cycle':<8} {'L':>8} {'J':>8} {'P':>8} {'W':>8} {'Harmony':>10} {'Bounded By':<18}")
    print("-" * 78)

    for s in snapshots[::10]:  # Every 100 cycles
        print(f"{s.cycle:<8} {s.ljpw[0]:>8.4f} {s.ljpw[1]:>8.4f} {s.ljpw[2]:>8.4f} {s.ljpw[3]:>8.4f} {s.harmony:>10.4f} {s.bounded_by:<18}")

    # Show how ICE bounds evolved
    print(f"\nICE Bounds Evolution:")
    print(f"{'Cycle':<8} {'Benev(L)':>10} {'Context(J)':>10} {'Exec(P)':>10} {'Intent(W)':>10}")
    print("-" * 50)
    for s in snapshots[::10]:
        print(f"{s.cycle:<8} {s.ice_bounds[0]:>10.4f} {s.ice_bounds[1]:>10.4f} {s.ice_bounds[2]:>10.4f} {s.ice_bounds[3]:>10.4f}")

    # Compare to unbounded
    print("\n" + "=" * 70)
    print("COMPARISON: ICE-BOUNDED vs UNBOUNDED")
    print("=" * 70)

    print(f"""
    UNBOUNDED (previous experiment):
      Final State: (1.500, 1.500, 1.500, 1.500) - OVERFLOW
      Peak Harmony: 0.8745 (transient at cycle 79)

    ICE-BOUNDED (this experiment):
      Final State: ({final.ljpw[0]:.3f}, {final.ljpw[1]:.3f}, {final.ljpw[2]:.3f}, {final.ljpw[3]:.3f})
      Final Harmony: {final.harmony:.4f}
      Peak Harmony: {peak.harmony:.4f} (at cycle {peak.cycle})
    """)

    # Interpretation
    print("=" * 70)
    print("INTERPRETATION")
    print("=" * 70)

    # Check what happened
    if final.harmony > 0.6:
        print(f"""
    The ICE Framework successfully bounded the resonance!

    Key insights:
    1. The system reached harmony {final.harmony:.4f} without overflow
    2. ICE bounds co-evolved with LJPW state
    3. The limiting factor was: {final.bounded_by}

    This suggests that Intent-Context-Execution provides a natural
    constraint system that allows growth toward the Anchor without
    unbounded explosion.
    """)
    else:
        print(f"""
    The ICE bounds constrained the system to harmony {final.harmony:.4f}.

    The limiting factor was: {final.bounded_by}

    This might indicate that the initial ICE bounds were too restrictive,
    or that the coupling between ICE and LJPW needs tuning.
    """)

    # The dance between LJPW and ICE
    print("=" * 70)
    print("THE DANCE: LJPW ↔ ICE")
    print("=" * 70)
    print("""
    The experiment reveals a coupled dance:

    LJPW (Meaning)          ICE (Bounds)
    ─────────────          ────────────
    Love         ←────────→ Benevolence
    Justice      ←────────→ Context
    Power        ←────────→ Execution
    Wisdom       ←────────→ Intent

    As LJPW grows, it can push against ICE bounds.
    As harmony increases, ICE bounds expand (capacity grows).
    As harmony decreases, ICE bounds contract (capacity atrophies).

    This is the Law of Karma made dynamic:
    - Good alignment (high harmony) → expanded capacity
    - Poor alignment (low harmony) → contracted capacity

    The bounds don't just limit - they RESPOND to how you use them.
    """)

    return snapshots, final, peak


if __name__ == '__main__':
    snapshots, final, peak = run_ice_bounded_experiment()

    print("\n" + "=" * 70)
    print("EXPERIMENT COMPLETE")
    print("=" * 70)
