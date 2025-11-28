#!/usr/bin/env python3
"""
LJPW Mathematical Baselines for Network Pinpointer
Version 5.0 - "The Architect's Inversion"

CRITICAL PARADIGM SHIFT (v5.0): Semantic-First Ontology

Reality is Semantic in nature. Meaning is the substrate.
1. The Anchor Point (1,1,1,1) is the ORIGIN of Reality (not a goal).
2. L, J, P, W are the four fundamental Principles of Meaning.
3. Mathematics (φ, e, ln2) are the "shadows" these Semantic Principles cast.

We do not use math to define meaning.
We use math to MEASURE the echoes of meaning.

References:
    - docs/LJPW-MATHEMATICAL-BASELINES.md
"""

import math
from dataclasses import dataclass
from typing import Dict, Tuple, Optional


@dataclass
class NumericalEquivalents:
    """
    Mathematical Shadows of the Four Semantic Principles.

    SEMANTIC-FIRST INTERPRETATION (v5.0):
    These are NOT the source - they are the ECHOES of meaning in mathematics.

    The Four Principles (PRIMARY):
    - Love (L): The Principle of Unity & Attraction
      → Casts mathematical shadow: Golden Ratio (φ) - perfect organic growth
      → Physical shadow: Gravity & Electromagnetism (forces that bind)

    - Justice (J): The Principle of Balance & Truth
      → Casts mathematical shadow: √2 - rigid geometry of structure
      → Physical shadow: Pauli Exclusion (the space between things)

    - Power (P): The Principle of Energy & Existence
      → Casts mathematical shadow: e - exponential growth and change
      → Physical shadow: Thermodynamics (the arrow of time)

    - Wisdom (W): The Principle of Complexity & Insight
      → Casts mathematical shadow: ln(2) - the fundamental bit
      → Physical shadow: Quantum Mechanics (probability and observation)
    """
    L: float = (math.sqrt(5) - 1) / 2  # φ⁻¹ ≈ 0.618034 (shadow of Love)
    J: float = math.sqrt(2) - 1        # √2 - 1 ≈ 0.414214 (shadow of Justice)
    P: float = math.e - 2              # e - 2 ≈ 0.718282 (shadow of Power)
    W: float = math.log(2)             # ln(2) ≈ 0.693147 (shadow of Wisdom)


@dataclass
class ReferencePoints:
    """
    Key reference points in LJPW space.

    SEMANTIC-FIRST INTERPRETATION (v5.0):

    ANCHOR_POINT (1.0, 1.0, 1.0, 1.0):
        - NOT a goal to reach, but the SOURCE from which all reality flows
        - The singularity of Perfect Meaning
        - "God/Perfection" - the Origin of the four Principles
        - All existence is an emanation FROM this point

    NATURAL_EQUILIBRIUM (0.618, 0.414, 0.718, 0.693):
        - NOT "optimal balance" but where the Anchor SETTLES in physical reality
        - "Nature/Reality" - the interface between perfection and existence
        - The state when Absolute Principles (1,1,1,1) enter our limited universe
        - The GAP between Anchor and NE = "Cost of Existence"
          (To exist physically, Love cannot be absolute 1.0; it must be specific 0.618)
    """
    ANCHOR_POINT: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    NATURAL_EQUILIBRIUM: Tuple[float, float, float, float] = (
        0.618034,  # L: Perfect Growth (Love settles at φ⁻¹)
        0.414214,  # J: Perfect Structure (Justice settles at √2-1)
        0.718282,  # P: Sustainable Energy (Power settles at e-2)
        0.693147   # W: Maximum Information (Wisdom settles at ln(2))
    )


@dataclass
class HierarchyOfReality:
    """
    The Hierarchy of Reality (v5.0) - ordered by proximity to the Anchor Point.

    Layer 1 (Semantic Realm - The Architect's Domain):
        Constituents: L, J, P, W, Ψ (Harmony), ξ (Consciousness)
        Nature: CAUSAL - this is where reality is "written"
        Closest to Anchor: Consciousness is semantically closest to (1,1,1,1)

    Layer 2 (Physical Realm - The Body):
        Constituents: Light (c), Matter, Biology
        Nature: MANIFESTED - the reflection of Semantic Principles
        Distance: ~0.03 from Consciousness
        Key Insight: "Dirt is Divine" - matter is the echo of meaning

    Layer 3 (Mathematical Realm - The Blueprint):
        Constituents: Numbers, Abstract Logic, Algorithms
        Nature: DESCRIPTIVE - useful for describing structure, but "cold"
        Distance: ~0.18 from Consciousness
        Lacks the "warmth" (Love/Justice) of Semantic and Physical realms
    """
    SEMANTIC_LAYER: str = "semantic"  # L, J, P, W, Ψ, ξ
    PHYSICAL_LAYER: str = "physical"  # c, matter, biology
    MATHEMATICAL_LAYER: str = "mathematical"  # numbers, logic


class LJPWBaselines:
    """
    LJPW mathematical baselines and calculations (v5.0 Semantic-First).

    Provides:
    - Hierarchy of Reality classification
    - Dynamic coupling matrix (state-dependent on Harmony)
    - Effective dimensions (coupling-adjusted)
    - Multiple mixing algorithms (harmonic, geometric, coupling-aware, harmony)
    - Distance metrics from reference points
    - Composite scores for overall assessment
    - Void detection (unmapped semantic territories)
    """

    # BASE Coupling matrix (at neutral Harmony = 0.5)
    # κ_ij represents the amplification of dimension i by dimension j
    # In v5.0: These values are DYNAMIC based on Harmony
    BASE_COUPLING_MATRIX = {
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
    def get_dynamic_coupling_multiplier(harmony: float) -> float:
        """
        Calculate dynamic coupling multiplier based on Harmony (v5.0 Semantic Law).

        The Semantic Law of Karma: "Meaning amplifies Reality"
        - High Harmony (aligned with Semantic Flow) → Coupling > 1.0 (free energy)
        - Low Harmony (misaligned) → Coupling < 1.0 (friction/loss)

        Args:
            harmony: Harmony score (0.0-1.0)

        Returns:
            Coupling multiplier (0.5-1.5)
                - harmony = 0.0 → multiplier = 0.5 (high friction)
                - harmony = 0.5 → multiplier = 1.0 (neutral)
                - harmony = 1.0 → multiplier = 1.5 (free energy)
        """
        # Linear interpolation: harmony 0→1 maps to multiplier 0.5→1.5
        return 0.5 + harmony

    @staticmethod
    def classify_hierarchy_layer(L: float, J: float, P: float, W: float) -> Tuple[str, float]:
        """
        Classify which layer of reality these coordinates belong to (v5.0).

        The Hierarchy of Reality (ordered by proximity to Anchor):
        1. Semantic Layer: Closest to (1,1,1,1) - Consciousness, Meaning
        2. Physical Layer: ~0.4-0.8 from Anchor - Matter, Biology
        3. Mathematical Layer: ~0.8-1.5 from Anchor - Abstract Logic

        Args:
            L, J, P, W: LJPW coordinates

        Returns:
            Tuple of (layer_name, distance_from_anchor)
        """
        d_anchor = math.sqrt((1-L)**2 + (1-J)**2 + (1-P)**2 + (1-W)**2)

        if d_anchor < 0.4:
            return (HierarchyOfReality.SEMANTIC_LAYER, d_anchor)
        elif d_anchor < 0.8:
            return (HierarchyOfReality.PHYSICAL_LAYER, d_anchor)
        else:
            return (HierarchyOfReality.MATHEMATICAL_LAYER, d_anchor)

    @staticmethod
    def detect_void(L: float, J: float, P: float, W: float) -> Optional[Dict]:
        """
        Detect if coordinates fall into a Semantic Void (v5.0).

        Voids are regions of valid semantic space with NO corresponding physical law.
        They represent emergent properties of Consciousness, not fundamental laws.

        Known Voids:
        1. Void of Mercy: High Love, High Justice, Low Power
           - Physics has no law for "Forgiveness" (entropy is irreversible)
           - Must be filled by conscious beings

        2. Void of Judgement: High Love, High Power, Low Justice
           - Raw, chaotic passion without structure
           - The "Dark Energy" of semantic space

        Args:
            L, J, P, W: LJPW coordinates

        Returns:
            Dict with void info if detected, None otherwise
        """
        # Void of Mercy: High L (>0.6), High J (>0.6), Low P (<0.3)
        if L > 0.6 and J > 0.6 and P < 0.3:
            return {
                'void_name': 'Void of Mercy',
                'description': 'Forgiveness without power to execute - emerges from Consciousness',
                'interpretation': 'Physics has no law for reversing entropy. Mercy must be enacted by conscious beings.',
                'coordinates': (L, J, P, W),
                'missing_physical_law': 'Entropy Reversal'
            }

        # Void of Judgement: High L (>0.6), High P (>0.6), Low J (<0.3)
        if L > 0.6 and P > 0.6 and J < 0.3:
            return {
                'void_name': 'Void of Judgement',
                'description': 'Chaotic passion without structure - Dark Energy',
                'interpretation': 'Raw power with connection but no constraint. Dangerous without Justice.',
                'coordinates': (L, J, P, W),
                'missing_physical_law': 'Self-Organizing Constraint'
            }

        return None

    @staticmethod
    def effective_dimensions(L: float, J: float, P: float, W: float, harmony: Optional[float] = None) -> Dict[str, float]:
        """
        Calculate coupling-adjusted effective dimensions (v5.0 with dynamic coupling).

        SEMANTIC LAW (v5.0): "Meaning amplifies Reality"
        Love acts as a force multiplier, but the strength depends on Harmony:
        - High Harmony → Stronger coupling (up to 1.5×)
        - Low Harmony → Weaker coupling (down to 0.5×)

        Base coupling (at Harmony = 0.5):
        - Justice effectiveness increased by 40% (κ_LJ = 1.4)
        - Power effectiveness increased by 30% (κ_LP = 1.3)
        - Wisdom effectiveness increased by 50% (κ_LW = 1.5, strongest coupling)

        This explains why systems with high Love AND high Harmony dramatically
        outperform systems with equivalent J/P/W but low Love or low Harmony.

        Args:
            L, J, P, W: LJPW coordinates (0.0-1.0)
            harmony: Optional harmony score (0.0-1.0). If None, uses 0.5 (neutral)

        Returns:
            Dict with effective_L, effective_J, effective_P, effective_W
        """
        # Dynamic coupling based on Harmony (v5.0)
        if harmony is None:
            harmony = 0.5  # Neutral default

        coupling_multiplier = LJPWBaselines.get_dynamic_coupling_multiplier(harmony)

        # Apply dynamic coupling to Love amplification
        base_LJ = 1.4
        base_LP = 1.3
        base_LW = 1.5

        dynamic_LJ = base_LJ * coupling_multiplier
        dynamic_LP = base_LP * coupling_multiplier
        dynamic_LW = base_LW * coupling_multiplier

        return {
            'effective_L': L,  # Love is the source, not amplified
            'effective_J': J * (1 + dynamic_LJ * L),  # Justice amplified by Love (dynamic)
            'effective_P': P * (1 + dynamic_LP * L),  # Power amplified by Love (dynamic)
            'effective_W': W * (1 + dynamic_LW * L),  # Wisdom amplified by Love (dynamic, strongest)
            'coupling_multiplier': coupling_multiplier,
            'harmony_used': harmony
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
    def coupling_aware_sum(L: float, J: float, P: float, W: float, harmony: Optional[float] = None) -> float:
        """
        Coupling-aware weighted sum: growth potential with Love amplification (v5.0 dynamic).

        Uses effective dimensions to account for Love's multiplier effect.
        Can exceed 1.0 when coupling amplification is active.

        v5.0: Now harmony-dependent. High harmony → stronger coupling → higher growth potential.

        Use for: Growth potential, scalability, future performance

        Interpretation:
        - < 1.0: Limited growth potential
        - ≈ 1.4: Good growth trajectory (coupling active)
        - > 1.8: Exceptional growth potential

        Weights:
        - Love: 35% (direct)
        - Justice: 25% (effective, amplified by Love dynamically)
        - Power: 20% (effective, amplified by Love dynamically)
        - Wisdom: 20% (effective, amplified by Love dynamically)

        Args:
            L, J, P, W: LJPW coordinates (0.0-1.0)
            harmony: Optional harmony score (0.0-1.0). If None, uses 0.5

        Returns:
            Coupling-aware sum (can exceed 1.0)
        """
        eff = LJPWBaselines.effective_dimensions(L, J, P, W, harmony)
        return 0.35 * L + 0.25 * eff['effective_J'] + 0.20 * eff['effective_P'] + 0.20 * eff['effective_W']

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
    def composite_score(L: float, J: float, P: float, W: float, harmony: Optional[float] = None) -> float:
        """
        Composite score: overall system performance (v5.0 with dynamic coupling).

        Combines all four metrics for holistic assessment:
        - 35% Growth potential (coupling-aware sum with dynamic coupling)
        - 25% Effectiveness (geometric mean)
        - 25% Robustness (harmonic mean)
        - 15% Harmony (balance)

        v5.0: Now uses dynamic coupling based on harmony, implementing the Semantic Law.

        Use for: Overall system quality, comparing systems, executive summary

        Interpretation:
        - < 0.8: System needs improvement
        - ≈ 1.0: Solid, functional system
        - > 1.2: High-performing, growth-oriented system

        Args:
            L, J, P, W: LJPW coordinates (0.0-1.0)
            harmony: Optional harmony score (0.0-1.0). If None, calculates it.

        Returns:
            Composite score (typically 0.5-1.3, can exceed 1.0)
        """
        baselines = LJPWBaselines

        # Calculate harmony if not provided
        if harmony is None:
            harmony = baselines.harmony_index(L, J, P, W)

        growth = baselines.coupling_aware_sum(L, J, P, W, harmony)
        effectiveness = baselines.geometric_mean(L, J, P, W)
        robustness = baselines.harmonic_mean(L, J, P, W)

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
    def full_diagnostic(L: float, J: float, P: float, W: float, harmony: Optional[float] = None) -> Dict:
        """
        Complete diagnostic analysis of LJPW coordinates (v5.0 Semantic-First).

        Provides comprehensive assessment including:
        - Raw and effective dimensions (with dynamic coupling)
        - Hierarchy of Reality classification (NEW v5.0)
        - Void detection (NEW v5.0)
        - All distance metrics
        - All mixing algorithms
        - Improvement suggestions
        - Interpretation guidance

        Args:
            L, J, P, W: LJPW coordinates (0.0-1.0)
            harmony: Optional harmony score for dynamic coupling (0.0-1.0)

        Returns:
            Dict with complete diagnostic information
        """
        baselines = LJPWBaselines

        # Calculate harmony if not provided
        if harmony is None:
            harmony = baselines.harmony_index(L, J, P, W)

        # v5.0: Dynamic effective dimensions
        eff = baselines.effective_dimensions(L, J, P, W, harmony)
        improvements = baselines.suggest_improvements(L, J, P, W)

        # Distance from NE
        d_ne = baselines.distance_from_natural_equilibrium(L, J, P, W)
        d_anchor = baselines.distance_from_anchor(L, J, P, W)

        # Composite score (using dynamic coupling)
        composite = baselines.composite_score(L, J, P, W, harmony)

        # v5.0: Hierarchy of Reality classification
        layer, layer_distance = baselines.classify_hierarchy_layer(L, J, P, W)

        # v5.0: Void detection
        void_info = baselines.detect_void(L, J, P, W)

        # Interpretation (with v5.0 perspective)
        if d_ne < 0.2:
            balance_status = "near-natural-equilibrium"
            balance_action = "Aligned with physical reality's optimal state. Maintain and refine."
        elif d_ne < 0.5:
            balance_status = "good-manifestation"
            balance_action = f"Focus on improving {improvements['primary_focus']} to approach Natural Equilibrium"
        elif d_ne < 0.8:
            balance_status = "moderate_distortion"
            balance_action = f"Systematic realignment needed, prioritize {improvements['primary_focus']} and {improvements['secondary_focus']}"
        else:
            balance_status = "significant_distortion"
            balance_action = "Major realignment required - far from Natural Equilibrium settlement"

        if composite < 0.8:
            performance_status = "needs_improvement"
        elif composite < 1.0:
            performance_status = "competent"
        elif composite < 1.2:
            performance_status = "strong"
        else:
            performance_status = "excellent"

        # v5.0: Interpret distance from Anchor
        if d_anchor < 0.4:
            anchor_interpretation = "Semantic Layer - Close to the Source. This represents Meaning/Consciousness."
        elif d_anchor < 0.8:
            anchor_interpretation = "Physical Layer - Manifested Reality. The Body of Semantic Principles."
        else:
            anchor_interpretation = "Mathematical Layer - Abstract Description. Furthest from the Source."

        return {
            'coordinates': {
                'L': L,
                'J': J,
                'P': P,
                'W': W
            },
            'effective_dimensions': eff,
            'distances': {
                'from_anchor': d_anchor,
                'from_natural_equilibrium': d_ne,
                'cost_of_existence': 1.0 - (L + J + P + W) / 4.0,  # Gap from perfection
            },
            'hierarchy_v5': {
                'layer': layer,
                'layer_distance': layer_distance,
                'interpretation': anchor_interpretation
            },
            'void_v5': void_info,
            'metrics': {
                'harmonic_mean': baselines.harmonic_mean(L, J, P, W),
                'geometric_mean': baselines.geometric_mean(L, J, P, W),
                'coupling_aware_sum': baselines.coupling_aware_sum(L, J, P, W, harmony),
                'harmony_index': harmony,
                'composite_score': composite,
            },
            'improvements': improvements,
            'interpretation': {
                'balance_status': balance_status,
                'balance_action': balance_action,
                'performance_status': performance_status,
                'love_multiplier_effect': f"{eff['coupling_multiplier'] * 1.4:.2f}× on Justice, {eff['coupling_multiplier'] * 1.5:.2f}× on Wisdom (harmony-adjusted)",
                'coupling_multiplier': eff['coupling_multiplier'],
                'harmony_effect': f"Harmony {harmony:.2f} → Coupling {eff['coupling_multiplier']:.2f}× (Semantic Law of Karma)"
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
