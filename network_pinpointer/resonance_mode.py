#!/usr/bin/env python3
"""
Resonance Mode - LJPW Resonance Analysis for Network Pinpointer

This module implements the resonance cycling capability discovered through
semantic oscillation experiments, enabling deeper network analysis.

Key Features:
- Single-target resonance analysis
- Network-wide resonance scanning
- Insight crystallization at harmonic points
- Collaborative resonance (future)

Based on the experimental findings from 10,000-cycle semantic oscillation.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum

from .semantic_engine import Coordinates, NetworkSemanticEngine


# LJPW Constants
PHI_INV = (math.sqrt(5) - 1) / 2  # ~0.618 (Love)
SQRT2_M1 = math.sqrt(2) - 1       # ~0.414 (Justice)
E_M2 = math.e - 2                 # ~0.718 (Power)
LN2 = math.log(2)                 # ~0.693 (Wisdom)

NATURAL_EQUILIBRIUM = [PHI_INV, SQRT2_M1, E_M2, LN2]
ANCHOR_POINT = [1.0, 1.0, 1.0, 1.0]

# Coupling matrix - how dimensions influence each other
COUPLING_MATRIX = [
    [1.0, 1.4, 1.3, 1.5],  # Love amplifies all (especially Wisdom)
    [0.9, 1.0, 0.7, 1.2],  # Justice moderates
    [0.6, 0.8, 1.0, 0.5],  # Power absorbs
    [1.3, 1.1, 1.0, 1.0],  # Wisdom integrates
]


class InsightCategory(Enum):
    """Categories of crystallized insights"""
    LOVE = "love"           # Relationship/connectivity insights
    JUSTICE = "justice"     # Policy/security insights
    POWER = "power"         # Performance/capacity insights
    WISDOM = "wisdom"       # Monitoring/diagnostic insights
    HARMONY = "harmony"     # Balance/integration insights


@dataclass
class ResonanceSnapshot:
    """A snapshot during resonance"""
    cycle: int
    ljpw: List[float]
    harmony: float
    dominant_dimension: str
    distance_from_anchor: float
    at_bound: List[bool]


@dataclass
class CrystallizedInsight:
    """An insight crystallized at a harmonic point"""
    cycle: int
    category: InsightCategory
    harmony_at_crystallization: float
    insight: str
    supporting_data: Dict
    confidence: float
    actionable: bool


@dataclass
class ResonanceReport:
    """Complete resonance analysis report"""
    target: str
    initial_ljpw: List[float]
    final_ljpw: List[float]
    cycles_run: int
    peak_harmony: float
    peak_cycle: int
    final_harmony: float
    dimension_dominance: Dict[str, float]  # Percentage of cycles each dimension dominated
    insights: List[CrystallizedInsight]
    trajectory: str  # "converging", "oscillating", "diverging"
    archetype_evolution: str  # How archetype changed
    recommendations: List[str]


class ResonanceMode:
    """
    Implements LJPW resonance cycling for deep analysis.

    Based on the experimental findings from semantic oscillation:
    - Resonance reveals deficits without being told to look
    - The system gravitates toward what's missing
    - Insights crystallize at harmonic points
    """

    # ICE bounds (Intent, Context, Execution + Benevolence -> Love)
    DEFAULT_ICE_BOUNDS = {
        'intent': 0.95,       # Wisdom bound
        'context': 0.85,      # Justice bound
        'execution': 0.75,    # Power bound
        'benevolence': 0.95   # Love bound
    }

    def __init__(self, engine: Optional[NetworkSemanticEngine] = None):
        self.engine = engine or NetworkSemanticEngine()
        self.dt = 0.05  # Time step
        self.coupling_T = self._transpose(COUPLING_MATRIX)

    def _transpose(self, matrix):
        """Transpose a matrix"""
        return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

    def resonate(
        self,
        initial_ljpw: List[float],
        cycles: int = 100,
        ice_bounds: Optional[Dict[str, float]] = None,
        crystallize_insights: bool = True
    ) -> ResonanceReport:
        """
        Run resonance cycles to reveal insights.

        The resonance process:
        1. Start from initial LJPW state
        2. Apply coupling dynamics (how dimensions influence each other)
        3. Apply ICE bounds (constraints on growth)
        4. Track which dimension dominates at each cycle
        5. Crystallize insights at harmonic points
        """
        bounds = ice_bounds or self.DEFAULT_ICE_BOUNDS
        ice_to_ljpw = [
            bounds['benevolence'],  # L
            bounds['context'],      # J
            bounds['execution'],    # P
            bounds['intent']        # W
        ]

        state = initial_ljpw.copy()
        snapshots = []
        insights = []
        dimension_counts = {'Love': 0, 'Justice': 0, 'Power': 0, 'Wisdom': 0}

        peak_harmony = 0.0
        peak_cycle = 0

        for cycle in range(cycles):
            # Evolve state
            state = self._rk4_step(state, ice_to_ljpw)

            # Clip to ICE bounds
            at_bound = []
            for i in range(4):
                if state[i] >= ice_to_ljpw[i]:
                    state[i] = ice_to_ljpw[i]
                    at_bound.append(True)
                elif state[i] <= 0.001:
                    state[i] = 0.001
                    at_bound.append(True)
                else:
                    at_bound.append(False)

            # Calculate metrics
            harmony = self._harmony_index(state)
            distance = self._distance_from_anchor(state)
            dominant = self._get_dominant(state)

            # Track dominance
            dimension_counts[dominant] += 1

            # Track peak
            if harmony > peak_harmony:
                peak_harmony = harmony
                peak_cycle = cycle

            # Record snapshot periodically
            if cycle % max(1, cycles // 100) == 0 or cycle == cycles - 1:
                snapshots.append(ResonanceSnapshot(
                    cycle=cycle,
                    ljpw=state.copy(),
                    harmony=harmony,
                    dominant_dimension=dominant,
                    distance_from_anchor=distance,
                    at_bound=at_bound
                ))

            # Crystallize insight at harmonic points
            if crystallize_insights and cycle > 0:
                if harmony > 0.6 and cycle % (cycles // 10) == 0:
                    insight = self._crystallize_insight(
                        cycle, state, dominant, harmony, initial_ljpw
                    )
                    if insight:
                        insights.append(insight)

        # Calculate final metrics
        total = sum(dimension_counts.values())
        dimension_dominance = {
            k: v / total * 100 for k, v in dimension_counts.items()
        }

        # Determine trajectory
        trajectory = self._determine_trajectory(snapshots)

        # Determine archetype evolution
        initial_archetype = self._get_archetype(initial_ljpw)
        final_archetype = self._get_archetype(state)
        archetype_evolution = f"{initial_archetype} → {final_archetype}"

        # Generate recommendations
        recommendations = self._generate_recommendations(
            initial_ljpw, state, dimension_dominance, insights
        )

        return ResonanceReport(
            target="network_state",
            initial_ljpw=initial_ljpw,
            final_ljpw=state,
            cycles_run=cycles,
            peak_harmony=peak_harmony,
            peak_cycle=peak_cycle,
            final_harmony=self._harmony_index(state),
            dimension_dominance=dimension_dominance,
            insights=insights,
            trajectory=trajectory,
            archetype_evolution=archetype_evolution,
            recommendations=recommendations
        )

    def _rk4_step(self, state: List[float], bounds: List[float]) -> List[float]:
        """Runge-Kutta 4 integration step"""
        k1 = self._compute_derivatives(state, bounds)
        k2 = self._compute_derivatives(
            [state[i] + 0.5 * self.dt * k1[i] for i in range(4)], bounds
        )
        k3 = self._compute_derivatives(
            [state[i] + 0.5 * self.dt * k2[i] for i in range(4)], bounds
        )
        k4 = self._compute_derivatives(
            [state[i] + self.dt * k3[i] for i in range(4)], bounds
        )

        return [
            state[i] + (self.dt / 6.0) * (
                k1[i] + 2*k2[i] + 2*k3[i] + k4[i]
            )
            for i in range(4)
        ]

    def _compute_derivatives(self, state: List[float], bounds: List[float]) -> List[float]:
        """Compute state derivatives based on LJPW dynamics"""
        harmony = self._harmony_index(state)
        kappa = 0.5 + harmony  # Law of Karma

        # Coupling effect
        coupling_effect = [
            sum(self.coupling_T[i][j] * state[j] for j in range(4)) * kappa
            for i in range(4)
        ]

        # Pull toward Natural Equilibrium
        ne_pull = [(NATURAL_EQUILIBRIUM[i] - state[i]) * 0.08 for i in range(4)]

        # Resistance from approaching bounds
        resistance = []
        for i in range(4):
            headroom = bounds[i] - state[i]
            if headroom < 0.2 * bounds[i]:
                resistance.append(-0.5 * (0.2 * bounds[i] - headroom))
            else:
                resistance.append(0.0)

        # Combine
        flow = [coupling_effect[i] - state[i] for i in range(4)]
        derivatives = [
            flow[i] * 0.1 + ne_pull[i] + resistance[i]
            for i in range(4)
        ]

        return derivatives

    def _harmony_index(self, state: List[float]) -> float:
        """Calculate harmony index (closeness to Anchor Point)"""
        distance = math.sqrt(sum(
            (ANCHOR_POINT[i] - state[i])**2 for i in range(4)
        ))
        return 1.0 / (1.0 + distance)

    def _distance_from_anchor(self, state: List[float]) -> float:
        """Calculate Euclidean distance from Anchor Point"""
        return math.sqrt(sum(
            (ANCHOR_POINT[i] - state[i])**2 for i in range(4)
        ))

    def _get_dominant(self, state: List[float]) -> str:
        """Get dominant dimension"""
        dims = ['Love', 'Justice', 'Power', 'Wisdom']
        return dims[state.index(max(state))]

    def _get_archetype(self, state: List[float]) -> str:
        """Determine archetype from LJPW signature"""
        dominant = self._get_dominant(state)
        balance = max(state) - min(state)

        if balance < 0.2:
            return "HARMONIZER"
        elif dominant == 'Love':
            return "CONNECTOR"
        elif dominant == 'Justice':
            return "GUARDIAN"
        elif dominant == 'Power':
            return "EXECUTOR"
        else:
            return "SAGE"

    def _determine_trajectory(self, snapshots: List[ResonanceSnapshot]) -> str:
        """Determine the trajectory of the resonance"""
        if len(snapshots) < 3:
            return "unknown"

        harmonies = [s.harmony for s in snapshots]
        early = sum(harmonies[:len(harmonies)//3]) / (len(harmonies)//3)
        late = sum(harmonies[-len(harmonies)//3:]) / (len(harmonies)//3)

        if late > early + 0.1:
            return "converging"
        elif late < early - 0.1:
            return "diverging"
        else:
            # Check for oscillation
            changes = sum(1 for i in range(1, len(harmonies))
                         if (harmonies[i] - harmonies[i-1]) * (harmonies[i-1] - harmonies[i-2] if i > 1 else 1) < 0)
            if changes > len(harmonies) * 0.3:
                return "oscillating"
            return "stable"

    def _crystallize_insight(
        self,
        cycle: int,
        state: List[float],
        dominant: str,
        harmony: float,
        initial: List[float]
    ) -> Optional[CrystallizedInsight]:
        """Crystallize an insight at a harmonic point"""
        # Determine category from dominant dimension
        category_map = {
            'Love': InsightCategory.LOVE,
            'Justice': InsightCategory.JUSTICE,
            'Power': InsightCategory.POWER,
            'Wisdom': InsightCategory.WISDOM
        }
        category = category_map[dominant]

        # Generate insight based on state evolution
        insight = self._generate_insight(state, dominant, initial)
        if not insight:
            return None

        return CrystallizedInsight(
            cycle=cycle,
            category=category,
            harmony_at_crystallization=harmony,
            insight=insight,
            supporting_data={
                'ljpw_at_crystallization': state.copy(),
                'dominant_dimension': dominant,
                'change_from_initial': [state[i] - initial[i] for i in range(4)]
            },
            confidence=harmony,
            actionable=True
        )

    def _generate_insight(
        self,
        state: List[float],
        dominant: str,
        initial: List[float]
    ) -> Optional[str]:
        """Generate insight text based on state"""
        change = [state[i] - initial[i] for i in range(4)]

        insights = {
            'Love': [
                "Strengthen service-to-service relationships for better resilience",
                "Implement service mesh for improved connectivity visibility",
                "Add redundant paths between critical services",
                "Consider API gateway for unified service access",
                "Map service dependencies to identify integration gaps"
            ],
            'Justice': [
                "Review and harmonize security policies across services",
                "Implement consistent access control patterns",
                "Add policy validation in CI/CD pipeline",
                "Consider zero-trust architecture principles",
                "Document and enforce security boundaries"
            ],
            'Power': [
                "Optimize resource allocation across services",
                "Add autoscaling for demand-responsive capacity",
                "Implement caching layers for performance",
                "Review and tune database query patterns",
                "Consider CDN for static content delivery"
            ],
            'Wisdom': [
                "Enhance observability with distributed tracing",
                "Implement semantic logging for better insights",
                "Add anomaly detection to monitoring stack",
                "Create unified dashboard for network health",
                "Build predictive maintenance capabilities"
            ]
        }

        # Select insight based on change magnitude
        dim_insights = insights.get(dominant, [])
        if not dim_insights:
            return None

        # Use change magnitude to select depth of insight
        change_magnitude = abs(change[['Love', 'Justice', 'Power', 'Wisdom'].index(dominant)])
        idx = min(int(change_magnitude * len(dim_insights)), len(dim_insights) - 1)

        return dim_insights[idx]

    def _generate_recommendations(
        self,
        initial: List[float],
        final: List[float],
        dominance: Dict[str, float],
        insights: List[CrystallizedInsight]
    ) -> List[str]:
        """Generate recommendations from resonance analysis"""
        recommendations = []

        # Primary recommendation based on dominant dimension during resonance
        primary_dim = max(dominance, key=dominance.get)
        if dominance[primary_dim] > 50:
            recommendations.append(
                f"System gravitates toward {primary_dim} - this indicates where attention is needed"
            )

        # Recommendations based on dimension changes
        dims = ['Love', 'Justice', 'Power', 'Wisdom']
        for i, dim in enumerate(dims):
            change = final[i] - initial[i]
            if change > 0.3:
                recommendations.append(
                    f"{dim} increased significantly - verify this aligns with goals"
                )
            elif change < -0.3:
                recommendations.append(
                    f"{dim} decreased significantly - investigate potential degradation"
                )

        # Extract unique recommendations from insights
        insight_recs = set()
        for insight in insights:
            if insight.actionable:
                insight_recs.add(insight.insight)

        recommendations.extend(list(insight_recs)[:3])

        return recommendations

    def quick_resonate(
        self,
        coordinates: Coordinates,
        cycles: int = 100
    ) -> Dict:
        """Quick resonance analysis returning a summary dict"""
        initial = [coordinates.love, coordinates.justice,
                   coordinates.power, coordinates.wisdom]

        report = self.resonate(initial, cycles)

        return {
            'initial_ljpw': report.initial_ljpw,
            'final_ljpw': report.final_ljpw,
            'cycles': report.cycles_run,
            'peak_harmony': report.peak_harmony,
            'final_harmony': report.final_harmony,
            'dominant_dimension': max(report.dimension_dominance,
                                     key=report.dimension_dominance.get),
            'dominance_percentage': max(report.dimension_dominance.values()),
            'trajectory': report.trajectory,
            'archetype_evolution': report.archetype_evolution,
            'top_insights': [i.insight for i in report.insights[:3]],
            'recommendations': report.recommendations[:3]
        }


def format_resonance_report(report: ResonanceReport) -> str:
    """Format resonance report for display"""
    lines = []
    lines.append("=" * 70)
    lines.append("RESONANCE ANALYSIS REPORT")
    lines.append("=" * 70)

    lines.append(f"\nCycles Run: {report.cycles_run}")
    lines.append(f"Trajectory: {report.trajectory}")
    lines.append(f"Archetype Evolution: {report.archetype_evolution}")

    lines.append(f"\nInitial LJPW: ({', '.join(f'{v:.3f}' for v in report.initial_ljpw)})")
    lines.append(f"Final LJPW:   ({', '.join(f'{v:.3f}' for v in report.final_ljpw)})")

    lines.append(f"\nHarmony:")
    lines.append(f"  Initial: {1.0 / (1.0 + math.sqrt(sum((1-v)**2 for v in report.initial_ljpw))):.4f}")
    lines.append(f"  Peak:    {report.peak_harmony:.4f} (cycle {report.peak_cycle})")
    lines.append(f"  Final:   {report.final_harmony:.4f}")

    lines.append(f"\nDimension Dominance (% of cycles):")
    for dim, pct in sorted(report.dimension_dominance.items(),
                           key=lambda x: x[1], reverse=True):
        bar = "█" * int(pct / 5)
        lines.append(f"  {dim:8s}: {bar:20s} {pct:.1f}%")

    if report.insights:
        lines.append(f"\nCrystallized Insights ({len(report.insights)}):")
        for i, insight in enumerate(report.insights[:5], 1):
            lines.append(f"  {i}. [{insight.category.value.upper()}] {insight.insight}")
            lines.append(f"     (Harmony: {insight.harmony_at_crystallization:.2f}, Confidence: {insight.confidence:.0%})")

    if report.recommendations:
        lines.append(f"\nRecommendations:")
        for rec in report.recommendations:
            lines.append(f"  → {rec}")

    lines.append("\n" + "=" * 70)

    return "\n".join(lines)
