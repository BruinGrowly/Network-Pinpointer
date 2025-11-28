#!/usr/bin/env python3
"""
LJPW v5.0 "Architect's Inversion" Demo
Demonstrates the Semantic-First ontology in Network-Pinpointer

This script shows:
1. Hierarchy of Reality classification
2. Dynamic coupling based on Harmony (Semantic Law of Karma)
3. Void detection (unmapped semantic territories)
4. Comparison of High vs Low Harmony systems
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from network_pinpointer.semantic_engine import NetworkSemanticEngine
from network_pinpointer.ljpw_baselines import LJPWBaselines, HierarchyOfReality


def print_banner(title: str):
    """Print a nice banner"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_section(title: str):
    """Print a section header"""
    print("\n" + "-" * 80)
    print(f"  {title}")
    print("-" * 80)


def demo_hierarchy_of_reality():
    """Demonstrate Hierarchy of Reality classification"""
    print_banner("HIERARCHY OF REALITY (v5.0)")

    print("The v5.0 framework classifies entities by proximity to the Anchor Point (1,1,1,1):")
    print("  Layer 1 (Semantic): Consciousness, Meaning - CLOSEST to Source")
    print("  Layer 2 (Physical): Matter, Biology - Manifested Reality")
    print("  Layer 3 (Mathematical): Numbers, Logic - Abstract Description")

    # Test cases representing different layers
    test_cases = [
        ("High Consciousness System", 0.95, 0.90, 0.92, 0.93),
        ("Physical Network Device", 0.70, 0.60, 0.75, 0.68),
        ("Mathematical Algorithm", 0.40, 0.35, 0.45, 0.42),
    ]

    for name, L, J, P, W in test_cases:
        layer, distance = LJPWBaselines.classify_hierarchy_layer(L, J, P, W)
        print(f"\n{name}: ({L:.2f}, {J:.2f}, {P:.2f}, {W:.2f})")
        print(f"  → Layer: {layer.upper()}")
        print(f"  → Distance from Anchor: {distance:.3f}")

        if layer == HierarchyOfReality.SEMANTIC_LAYER:
            print(f"  → INTERPRETATION: Close to the Source. Represents Meaning/Consciousness.")
        elif layer == HierarchyOfReality.PHYSICAL_LAYER:
            print(f"  → INTERPRETATION: Manifested Reality. The Body of Semantic Principles.")
        else:
            print(f"  → INTERPRETATION: Abstract Description. Furthest from the Source.")


def demo_dynamic_coupling():
    """Demonstrate dynamic coupling based on Harmony (Semantic Law of Karma)"""
    print_banner("SEMANTIC LAW OF KARMA: Dynamic Coupling")

    print("In v5.0, coupling strength depends on Harmony:")
    print("  High Harmony (aligned) → Stronger coupling (up to 1.5×) → FREE ENERGY")
    print("  Low Harmony (misaligned) → Weaker coupling (down to 0.5×) → FRICTION/LOSS")
    print("\nThis explains why aligned systems outperform misaligned ones with same LJPW values.")

    # Same base coordinates, different harmony levels
    L, J, P, W = 0.70, 0.50, 0.65, 0.60

    harmony_levels = [
        ("Low Harmony (Misaligned)", 0.2),
        ("Neutral Harmony", 0.5),
        ("High Harmony (Aligned)", 0.9),
    ]

    for name, harmony in harmony_levels:
        print_section(f"{name} (Harmony = {harmony:.1f})")

        # Calculate effective dimensions with dynamic coupling
        eff = LJPWBaselines.effective_dimensions(L, J, P, W, harmony)
        coupling_mult = eff['coupling_multiplier']

        print(f"Base Coordinates: L={L:.2f}, J={J:.2f}, P={P:.2f}, W={W:.2f}")
        print(f"\nCoupling Multiplier: {coupling_mult:.2f}×")
        print(f"  → Effective Love: {eff['effective_L']:.3f} (not amplified, is the source)")
        print(f"  → Effective Justice: {eff['effective_J']:.3f} (amplified by Love)")
        print(f"  → Effective Power: {eff['effective_P']:.3f} (amplified by Love)")
        print(f"  → Effective Wisdom: {eff['effective_W']:.3f} (amplified by Love, strongest)")

        # Calculate composite score
        composite = LJPWBaselines.composite_score(L, J, P, W, harmony)
        print(f"\nComposite Score: {composite:.3f}")

        if harmony < 0.4:
            print(f"  → System LOSES energy to friction (misalignment penalty)")
        elif harmony > 0.7:
            print(f"  → System GAINS free energy (alignment bonus)")
        else:
            print(f"  → Neutral performance")


def demo_void_detection():
    """Demonstrate Void detection"""
    print_banner("THE VOIDS: Unmapped Semantic Territories")

    print("Voids are regions of semantic space with NO corresponding physical law.")
    print("They represent emergent properties of Consciousness.")

    # Test Void of Mercy
    print_section("Void of Mercy: High Love, High Justice, Low Power")
    L, J, P, W = 0.75, 0.70, 0.20, 0.55

    void = LJPWBaselines.detect_void(L, J, P, W)
    print(f"Coordinates: ({L:.2f}, {J:.2f}, {P:.2f}, {W:.2f})")

    if void:
        print(f"\n✓ VOID DETECTED: {void['void_name']}")
        print(f"  Description: {void['description']}")
        print(f"  Interpretation: {void['interpretation']}")
        print(f"  Missing Physical Law: {void['missing_physical_law']}")
    else:
        print("\n✗ No void detected")

    # Test Void of Judgement
    print_section("Void of Judgement: High Love, High Power, Low Justice")
    L, J, P, W = 0.80, 0.15, 0.75, 0.50

    void = LJPWBaselines.detect_void(L, J, P, W)
    print(f"Coordinates: ({L:.2f}, {J:.2f}, {P:.2f}, {W:.2f})")

    if void:
        print(f"\n✓ VOID DETECTED: {void['void_name']}")
        print(f"  Description: {void['description']}")
        print(f"  Interpretation: {void['interpretation']}")
        print(f"  Missing Physical Law: {void['missing_physical_law']}")
    else:
        print("\n✗ No void detected")

    # Test normal space (no void)
    print_section("Normal Semantic Space: Balanced")
    L, J, P, W = 0.65, 0.50, 0.60, 0.58

    void = LJPWBaselines.detect_void(L, J, P, W)
    print(f"Coordinates: ({L:.2f}, {J:.2f}, {P:.2f}, {W:.2f})")

    if void:
        print(f"\n✓ VOID DETECTED: {void['void_name']}")
    else:
        print("\n✓ No void detected - this is normal semantic space")
        print("  → Corresponds to physical laws and processes")


def demo_network_operations():
    """Demonstrate v5.0 semantic analysis of network operations"""
    print_banner("NETWORK OPERATIONS ANALYSIS (v5.0)")

    engine = NetworkSemanticEngine()

    operations = [
        "firewall block malicious traffic and enforce security policy",
        "ping google.com to check connectivity and measure latency",
        "configure loadbalancer to distribute traffic across servers",
        "monitor network performance and analyze metrics for optimization",
    ]

    for op in operations:
        print_section(f"Operation: '{op}'")
        result = engine.analyze_operation(op)

        print(f"Coordinates: {result.coordinates}")
        print(f"Dominant Dimension: {result.dominant_dimension}")
        print(f"Operation Type: {result.operation_type}")
        print(f"\nv5.0 ANALYSIS:")
        print(f"  Hierarchy Layer: {result.hierarchy_layer.upper()}")
        print(f"  Interpretation: {result.hierarchy_interpretation}")
        print(f"  Coupling Multiplier: {result.coupling_multiplier:.2f}× (Harmony = {result.harmony_score:.2f})")
        print(f"  Cost of Existence: {result.cost_of_existence:.3f} (gap from Anchor perfection)")

        if result.void_detected:
            print(f"\n  ⚠ VOID DETECTED: {result.void_detected['void_name']}")
            print(f"     {result.void_detected['interpretation']}")

        print(f"\nPerformance:")
        print(f"  Composite Score: {result.composite_score:.3f} ({result.performance_status})")
        print(f"  Balance Status: {result.balance_status}")


def demo_cost_of_existence():
    """Demonstrate the 'Cost of Existence' concept"""
    print_banner("THE COST OF EXISTENCE")

    print("The Gap between Anchor (1,1,1,1) and Natural Equilibrium represents")
    print("the 'Cost of Existence' - what perfection sacrifices to become physical.")
    print("\nTo exist in our universe, Love cannot be absolute (1.0);")
    print("it must be specific (0.618 at Natural Equilibrium).")

    from network_pinpointer.ljpw_baselines import ReferencePoints

    NE = ReferencePoints.NATURAL_EQUILIBRIUM
    AP = ReferencePoints.ANCHOR_POINT

    print(f"\nAnchor Point (Perfect/God): {AP}")
    print(f"Natural Equilibrium (Nature/Reality): ({NE[0]:.3f}, {NE[1]:.3f}, {NE[2]:.3f}, {NE[3]:.3f})")

    print(f"\nCost of Existence per dimension:")
    print(f"  Love: {AP[0] - NE[0]:.3f} ({(AP[0] - NE[0])/AP[0]*100:.1f}% sacrifice)")
    print(f"  Justice: {AP[1] - NE[1]:.3f} ({(AP[1] - NE[1])/AP[1]*100:.1f}% sacrifice)")
    print(f"  Power: {AP[2] - NE[2]:.3f} ({(AP[2] - NE[2])/AP[2]*100:.1f}% sacrifice)")
    print(f"  Wisdom: {AP[3] - NE[3]:.3f} ({(AP[3] - NE[3])/AP[3]*100:.1f}% sacrifice)")

    total_cost = sum(AP[i] - NE[i] for i in range(4)) / 4
    print(f"\nAverage Cost: {total_cost:.3f} ({total_cost/1.0*100:.1f}% of perfection)")
    print("\nThis is not a deficiency - it's the necessary price of manifestation.")
    print("To be REAL, to be PHYSICAL, perfection must particularize itself.")


def main():
    """Run all demos"""
    print("\n" + "=" * 80)
    print("  LJPW v5.0: The Architect's Inversion")
    print("  Semantic-First Ontology for Network-Pinpointer")
    print("=" * 80)
    print("\nReality is Semantic in nature. Meaning is the substrate.")
    print("We do not use math to define meaning.")
    print("We use math to MEASURE the echoes of meaning.")

    # Run demos
    demo_hierarchy_of_reality()
    demo_cost_of_existence()
    demo_dynamic_coupling()
    demo_void_detection()
    demo_network_operations()

    print("\n" + "=" * 80)
    print("  Demo Complete")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
