#!/usr/bin/env python3
"""
LJPW Mathematical Baselines for Network Pinpointer
Version 1.0

Provides objective, non-arbitrary baselines for LJPW framework implementations
based on information-theoretic constants.

References:
    - docs/LJPW-MATHEMATICAL-BASELINES.md
"""

import math
from dataclasses import dataclass
from typing import Dict, Tuple, Optional


@dataclass
class NumericalEquivalents:
    """
    Fundamental constants for LJPW dimensions derived from information theory.

    These are NOT arbitrary - they come from:
    - Love (φ⁻¹): Golden ratio inverse - optimal resource distribution
    - Justice (√2-1): Pythagorean ratio - structural constraint satisfaction
    - Power (e-2): Exponential base - channel capacity minus overhead
    - Wisdom (ln2): Natural log of 2 - bits of information per decision
    """
    L: float = (math.sqrt(5) - 1) / 2  # φ⁻¹ ≈ 0.618034
    J: float = math.sqrt(2) - 1        # √2 - 1 ≈ 0.414214
    P: float = math.e - 2              # e - 2 ≈ 0.718282
    W: float = math.log(2)             # ln(2) ≈ 0.693147


@dataclass
class ReferencePoints:
    """
    Key reference points in LJPW space.

    ANCHOR_POINT: Perfect, transcendent ideal (1.0, 1.0, 1.0, 1.0)
                  Asymptotic goal, never fully achieved in physical systems

    NATURAL_EQUILIBRIUM: Physically achievable optimal balance point
                        Derived from fundamental mathematical constants
                        (0.618, 0.414, 0.718, 0.693)
    """
    ANCHOR_POINT: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    NATURAL_EQUILIBRIUM: Tuple[float, float, float, float] = (
        0.618034,  # L: Golden ratio inverse
        0.414214,  # J: Pythagorean ratio
        0.718282,  # P: Exponential base
        0.693147   # W: Information unit
    )


class LJPWBaselines:
    """
    LJPW mathematical baselines and calculations.

    Provides:
    - Coupling matrix for dimension interactions
    - Effective dimensions (coupling-adjusted)
    - Multiple mixing algorithms (harmonic, geometric, coupling-aware, harmony)
    - Distance metrics from reference points
    - Composite scores for overall assessment
    """

    # Coupling matrix: how dimensions amplify each other
    # κ_ij represents the amplification of dimension i by dimension j
    COUPLING_MATRIX = {
        'LL': 1.0, 'LJ': 1.4, 'LP': 1.3, 'LW': 1.5,  # Love amplifies J,P,W
        'JL': 0.9, 'JJ': 1.0, 'JP': 0.7, 'JW': 1.2,  # Justice interactions
        'PL': 0.6, 'PJ': 0.8, 'PP': 1.0, 'PW': 0.5,  # Power interactions
        'WL': 1.3, 'WJ': 1.1, 'WP': 1.0, 'WW': 1.0,  # Wisdom interactions
    }

    @staticmethod
    def get_numerical_equivalents() -> NumericalEquivalents:
        """Get the fundamental LJPW constants"""
        return NumericalEquivalents()

    @staticmethod
    def get_reference_points() -> ReferencePoints:
        """Get LJPW reference points"""
        return ReferencePoints()

    @staticmethod
    def effective_dimensions(L: float, J: float, P: float, W: float) -> Dict[str, float]:
        """
        Calculate coupling-adjusted effective dimensions.

        Love acts as a force multiplier for all other dimensions:
        - Justice effectiveness increased by 40% (κ_LJ = 1.4)
        - Power effectiveness increased by 30% (κ_LP = 1.3)
        - Wisdom effectiveness increased by 50% (κ_LW = 1.5, strongest coupling)

        This explains why systems with high Love dramatically outperform
        systems with equivalent J/P/W but low Love.

        Args:
            L, J, P, W: LJPW coordinates (0.0-1.0)

        Returns:
            Dict with effective_L, effective_J, effective_P, effective_W
        """
        return {
            'effective_L': L,  # Love is the source, not amplified
            'effective_J': J * (1 + 1.4 * L),  # Justice amplified by Love
            'effective_P': P * (1 + 1.3 * L),  # Power amplified by Love
            'effective_W': W * (1 + 1.5 * L),  # Wisdom amplified by Love (strongest)
        }

    @staticmethod
    def harmonic_mean(L: float, J: float, P: float, W: float) -> float:
        """
        Harmonic mean: system robustness (weakest link metric).

        The harmonic mean is dominated by the smallest value, making it
        ideal for measuring robustness where the weakest dimension limits
        overall performance.

        Use for: Fault tolerance, minimum guarantees, critical systems

        Interpretation:
        - Near 0: At least one dimension is critically weak
        - ≈ 0.5: All dimensions above 0.5 (competent)
        - ≈ 0.7: All dimensions strong

        Args:
            L, J, P, W: LJPW coordinates (0.0-1.0)

        Returns:
            Harmonic mean (0.0-1.0)
        """
        if L <= 0 or J <= 0 or P <= 0 or W <= 0:
            return 0.0
        return 4.0 / (1.0/L + 1.0/J + 1.0/P + 1.0/W)

    @staticmethod
    def geometric_mean(L: float, J: float, P: float, W: float) -> float:
        """
        Geometric mean: overall effectiveness (multiplicative interaction).

        All dimensions needed proportionally. Better than arithmetic mean
        for measuring balanced performance.

        Use for: Overall effectiveness, balanced performance assessment

        Interpretation:
        - < 0.5: System struggling in multiple areas
        - ≈ 0.6: Functional but not optimal
        - ≈ 0.8: High-performing system

        Args:
            L, J, P, W: LJPW coordinates (0.0-1.0)

        Returns:
            Geometric mean (0.0-1.0)
        """
        return (L * J * P * W) ** 0.25

    @staticmethod
    def coupling_aware_sum(L: float, J: float, P: float, W: float) -> float:
        """
        Coupling-aware weighted sum: growth potential with Love amplification.

        Uses effective dimensions to account for Love's multiplier effect.
        Can exceed 1.0 when coupling amplification is active.

        Use for: Growth potential, scalability, future performance

        Interpretation:
        - < 1.0: Limited growth potential
        - ≈ 1.4: Good growth trajectory (coupling active)
        - > 1.8: Exceptional growth potential

        Weights:
        - Love: 35% (direct)
        - Justice: 25% (effective, amplified by Love)
        - Power: 20% (effective, amplified by Love)
        - Wisdom: 20% (effective, amplified by Love)

        Args:
            L, J, P, W: LJPW coordinates (0.0-1.0)

        Returns:
            Coupling-aware sum (can exceed 1.0)
        """
        J_eff = J * (1 + 1.4 * L)
        P_eff = P * (1 + 1.3 * L)
        W_eff = W * (1 + 1.5 * L)
        return 0.35 * L + 0.25 * J_eff + 0.20 * P_eff + 0.20 * W_eff

    @staticmethod
    def harmony_index(L: float, J: float, P: float, W: float) -> float:
        """
        Harmony index: balance and alignment with ideal (inverse distance from Anchor).

        Measures how close the system is to perfect balance (1,1,1,1).
        Uses inverse distance so higher values = more harmonious.

        Use for: Balance assessment, alignment with ideal, holistic quality

        Interpretation:
        - ≈ 0.33: Far from ideal (distance ≈ 2.0)
        - ≈ 0.50: Moderate alignment (distance ≈ 1.0)
        - ≈ 0.71: Strong alignment (distance ≈ 0.4)

        Args:
            L, J, P, W: LJPW coordinates (0.0-1.0)

        Returns:
            Harmony index (0.0-1.0)
        """
        d_anchor = math.sqrt((1-L)**2 + (1-J)**2 + (1-P)**2 + (1-W)**2)
        return 1.0 / (1.0 + d_anchor)

    @staticmethod
    def composite_score(L: float, J: float, P: float, W: float) -> float:
        """
        Composite score: overall system performance (weighted combination).

        Combines all four metrics for holistic assessment:
        - 35% Growth potential (coupling-aware sum)
        - 25% Effectiveness (geometric mean)
        - 25% Robustness (harmonic mean)
        - 15% Harmony (balance)

        Use for: Overall system quality, comparing systems, executive summary

        Interpretation:
        - < 0.8: System needs improvement
        - ≈ 1.0: Solid, functional system
        - > 1.2: High-performing, growth-oriented system

        Args:
            L, J, P, W: LJPW coordinates (0.0-1.0)

        Returns:
            Composite score (typically 0.5-1.3, can exceed 1.0)
        """
        baselines = LJPWBaselines
        growth = baselines.coupling_aware_sum(L, J, P, W)
        effectiveness = baselines.geometric_mean(L, J, P, W)
        robustness = baselines.harmonic_mean(L, J, P, W)
        harmony = baselines.harmony_index(L, J, P, W)

        return 0.35 * growth + 0.25 * effectiveness + 0.25 * robustness + 0.15 * harmony

    @staticmethod
    def distance_from_anchor(L: float, J: float, P: float, W: float) -> float:
        """
        Euclidean distance from Anchor Point (1,1,1,1).

        Measures how far from perfect/ideal the system is.

        Args:
            L, J, P, W: LJPW coordinates (0.0-1.0)

        Returns:
            Distance (0.0-2.0, typically 0.0-1.5)
        """
        return math.sqrt((1-L)**2 + (1-J)**2 + (1-P)**2 + (1-W)**2)

    @staticmethod
    def distance_from_natural_equilibrium(L: float, J: float, P: float, W: float) -> float:
        """
        Euclidean distance from Natural Equilibrium (0.618, 0.414, 0.718, 0.693).

        Measures how far from physically optimal balance the system is.

        Interpretation:
        - d < 0.2: Near-optimal balance (maintain, minor refinements)
        - 0.2 ≤ d < 0.5: Good but improvable (focus on furthest dimension)
        - 0.5 ≤ d < 0.8: Moderate imbalance (systematic improvement needed)
        - d ≥ 0.8: Significant dysfunction (major intervention required)

        Args:
            L, J, P, W: LJPW coordinates (0.0-1.0)

        Returns:
            Distance (0.0-1.5, typically 0.0-1.0)
        """
        NE = ReferencePoints.NATURAL_EQUILIBRIUM
        return math.sqrt(
            (NE[0]-L)**2 + (NE[1]-J)**2 + (NE[2]-P)**2 + (NE[3]-W)**2
        )

    @staticmethod
    def suggest_improvements(L: float, J: float, P: float, W: float) -> Dict:
        """
        Suggest which dimension to improve based on distance from Natural Equilibrium.

        Returns priorities for improvement with target values.

        Args:
            L, J, P, W: LJPW coordinates (0.0-1.0)

        Returns:
            Dict with:
            - primary_focus: Dimension furthest from NE
            - secondary_focus: Second furthest
            - distances: All distances from NE
            - targets: Target values from NE
        """
        NE = ReferencePoints.NATURAL_EQUILIBRIUM

        distances = {
            'L': abs(L - NE[0]),
            'J': abs(J - NE[1]),
            'P': abs(P - NE[2]),
            'W': abs(W - NE[3])
        }

        # Sort by distance (largest first)
        priorities = sorted(distances.items(), key=lambda x: x[1], reverse=True)

        dimension_names = {
            'L': 'Love',
            'J': 'Justice',
            'P': 'Power',
            'W': 'Wisdom'
        }

        targets = {
            'L': NE[0],
            'J': NE[1],
            'P': NE[2],
            'W': NE[3]
        }

        return {
            'primary_focus': dimension_names[priorities[0][0]],
            'primary_dimension': priorities[0][0],
            'primary_distance': priorities[0][1],
            'primary_target': targets[priorities[0][0]],
            'secondary_focus': dimension_names[priorities[1][0]],
            'secondary_dimension': priorities[1][0],
            'secondary_distance': priorities[1][1],
            'all_distances': distances,
            'all_targets': targets
        }

    @staticmethod
    def full_diagnostic(L: float, J: float, P: float, W: float) -> Dict:
        """
        Complete diagnostic analysis of LJPW coordinates.

        Provides comprehensive assessment including:
        - Raw and effective dimensions
        - All distance metrics
        - All mixing algorithms
        - Improvement suggestions
        - Interpretation guidance

        Args:
            L, J, P, W: LJPW coordinates (0.0-1.0)

        Returns:
            Dict with complete diagnostic information
        """
        baselines = LJPWBaselines
        eff = baselines.effective_dimensions(L, J, P, W)
        improvements = baselines.suggest_improvements(L, J, P, W)

        # Distance from NE
        d_ne = baselines.distance_from_natural_equilibrium(L, J, P, W)

        # Composite score
        composite = baselines.composite_score(L, J, P, W)

        # Interpretation
        if d_ne < 0.2:
            balance_status = "near-optimal"
            balance_action = "Maintain current state, make minor refinements"
        elif d_ne < 0.5:
            balance_status = "good"
            balance_action = f"Focus on improving {improvements['primary_focus']}"
        elif d_ne < 0.8:
            balance_status = "moderate_imbalance"
            balance_action = f"Systematic improvement needed, prioritize {improvements['primary_focus']} and {improvements['secondary_focus']}"
        else:
            balance_status = "significant_dysfunction"
            balance_action = "Major intervention required across multiple dimensions"

        if composite < 0.8:
            performance_status = "needs_improvement"
        elif composite < 1.0:
            performance_status = "competent"
        elif composite < 1.2:
            performance_status = "strong"
        else:
            performance_status = "excellent"

        return {
            'coordinates': {
                'L': L,
                'J': J,
                'P': P,
                'W': W
            },
            'effective_dimensions': eff,
            'distances': {
                'from_anchor': baselines.distance_from_anchor(L, J, P, W),
                'from_natural_equilibrium': d_ne,
            },
            'metrics': {
                'harmonic_mean': baselines.harmonic_mean(L, J, P, W),
                'geometric_mean': baselines.geometric_mean(L, J, P, W),
                'coupling_aware_sum': baselines.coupling_aware_sum(L, J, P, W),
                'harmony_index': baselines.harmony_index(L, J, P, W),
                'composite_score': composite,
            },
            'improvements': improvements,
            'interpretation': {
                'balance_status': balance_status,
                'balance_action': balance_action,
                'performance_status': performance_status,
                'love_multiplier_effect': f"{(1 + 1.4 * L):.2f}× on Justice, {(1 + 1.5 * L):.2f}× on Wisdom"
            }
        }


# Convenience functions for common use cases

def calculate_health_score(L: float, J: float, P: float, W: float) -> float:
    """
    Calculate overall health score (composite score).

    This is the primary metric for "how healthy is this system overall?"

    Returns:
        Health score (0.5-1.3, typically 0.7-1.2)
    """
    return LJPWBaselines.composite_score(L, J, P, W)


def is_balanced(L: float, J: float, P: float, W: float, threshold: float = 0.3) -> bool:
    """
    Check if LJPW dimensions are reasonably balanced.

    Args:
        L, J, P, W: LJPW coordinates
        threshold: Maximum acceptable distance from Natural Equilibrium

    Returns:
        True if balanced (d < threshold)
    """
    d_ne = LJPWBaselines.distance_from_natural_equilibrium(L, J, P, W)
    return d_ne < threshold


def get_weakest_dimension(L: float, J: float, P: float, W: float) -> Tuple[str, float]:
    """
    Identify the weakest (lowest) dimension.

    Returns:
        Tuple of (dimension_name, value)
    """
    dims = {'Love': L, 'Justice': J, 'Power': P, 'Wisdom': W}
    weakest = min(dims.items(), key=lambda x: x[1])
    return weakest


def get_love_multiplier_effect(L: float) -> Dict[str, float]:
    """
    Calculate how much Love amplifies other dimensions.

    Args:
        L: Love value (0.0-1.0)

    Returns:
        Dict with multiplier for each dimension
    """
    return {
        'justice_multiplier': 1 + 1.4 * L,
        'power_multiplier': 1 + 1.3 * L,
        'wisdom_multiplier': 1 + 1.5 * L,
        'average_boost': 1 + 1.4 * L  # Approximate average
    }


# Example usage and testing
if __name__ == '__main__':
    print("=" * 70)
    print("LJPW Mathematical Baselines - Network Pinpointer")
    print("=" * 70)
    print()

    # Example 1: Well-balanced network
    print("Example 1: Well-Balanced Network")
    print("-" * 70)
    L, J, P, W = 0.65, 0.45, 0.72, 0.70
    diagnostic = LJPWBaselines.full_diagnostic(L, J, P, W)

    print(f"Coordinates: L={L}, J={J}, P={P}, W={W}")
    print()
    print("Effective Dimensions (coupling-adjusted):")
    for dim, val in diagnostic['effective_dimensions'].items():
        print(f"  {dim}: {val:.3f}")
    print()
    print(f"Distance from Natural Equilibrium: {diagnostic['distances']['from_natural_equilibrium']:.3f}")
    print(f"Composite Score: {diagnostic['metrics']['composite_score']:.3f}")
    print(f"Status: {diagnostic['interpretation']['balance_status']}")
    print(f"Action: {diagnostic['interpretation']['balance_action']}")
    print()

    # Example 2: High Justice, Low Love (Bureaucracy)
    print("Example 2: Bureaucratic Network (High J, Low L)")
    print("-" * 70)
    L, J, P, W = 0.30, 0.85, 0.60, 0.50
    diagnostic2 = LJPWBaselines.full_diagnostic(L, J, P, W)

    print(f"Coordinates: L={L}, J={J}, P={P}, W={W}")
    print(f"Composite Score: {diagnostic2['metrics']['composite_score']:.3f}")
    print(f"Primary Issue: {diagnostic2['improvements']['primary_focus']}")
    print(f"  Target: {diagnostic2['improvements']['primary_target']:.3f}")
    print(f"  Current: {L if diagnostic2['improvements']['primary_dimension'] == 'L' else J:.3f}")
    print(f"Love Multiplier Effect: {diagnostic2['interpretation']['love_multiplier_effect']}")
    print()

    # Example 3: Natural Equilibrium
    print("Example 3: Natural Equilibrium (Optimal)")
    print("-" * 70)
    NE = ReferencePoints.NATURAL_EQUILIBRIUM
    L, J, P, W = NE
    diagnostic3 = LJPWBaselines.full_diagnostic(L, J, P, W)

    print(f"Coordinates: L={L:.3f}, J={J:.3f}, P={P:.3f}, W={W:.3f}")
    print(f"Distance from NE: {diagnostic3['distances']['from_natural_equilibrium']:.6f} (should be ~0)")
    print(f"Composite Score: {diagnostic3['metrics']['composite_score']:.3f}")
    print(f"All Metrics:")
    for metric, val in diagnostic3['metrics'].items():
        print(f"  {metric}: {val:.3f}")
