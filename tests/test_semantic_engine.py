#!/usr/bin/env python3
"""
Basic tests for Network-Pinpointer Semantic Engine
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from network_pinpointer.semantic_engine import (
    NetworkSemanticEngine,
    NetworkVocabularyManager,
    Coordinates,
)


def test_vocabulary_initialization():
    """Test that vocabulary manager initializes correctly"""
    vocab = NetworkVocabularyManager()
    assert len(vocab.all_keywords) > 200, "Should have 200+ network keywords"
    print(f"✓ Vocabulary initialized with {len(vocab.all_keywords)} keywords")


def test_network_operation_analysis():
    """Test analyzing network operations"""
    engine = NetworkSemanticEngine()

    # Test 1: Monitoring (should be Wisdom-dominant)
    result = engine.analyze_operation("monitor diagnose analyze information")
    assert result.coordinates.wisdom > 0.3, "Monitoring should have high Wisdom"
    assert result.dominant_dimension == "Wisdom", "Monitoring should be Wisdom-dominant"
    print(f"✓ Monitoring analysis: {result.coordinates} - {result.dominant_dimension}")

    # Test 2: Firewall (should be Justice-dominant)
    result = engine.analyze_operation("firewall rules security policy enforce")
    assert result.coordinates.justice > 0.3, "Firewall should have high Justice"
    assert result.dominant_dimension == "Justice", "Firewall should be Justice-dominant"
    print(f"✓ Firewall analysis: {result.coordinates} - {result.dominant_dimension}")

    # Test 3: Service (should be Love-dominant)
    result = engine.analyze_operation("service connect communicate integrate share")
    assert result.coordinates.love > 0.3, "Service should have high Love"
    assert result.dominant_dimension == "Love", "Service should be Love-dominant"
    print(f"✓ Service analysis: {result.coordinates} - {result.dominant_dimension}")

    # Test 4: Performance (should be Power-dominant)
    result = engine.analyze_operation("bandwidth performance execute control manage")
    assert result.coordinates.power > 0.3, "Performance should have high Power"
    assert result.dominant_dimension == "Power", "Performance should be Power-dominant"
    print(f"✓ Performance analysis: {result.coordinates} - {result.dominant_dimension}")


def test_ice_analysis():
    """Test ICE framework analysis"""
    engine = NetworkSemanticEngine()

    result = engine.analyze_ice(
        intent="establish secure fast connection",
        context="network with firewall limited bandwidth",
        execution="open port configure connection"
    )

    assert "ice_coherence" in result, "Should have ICE coherence metric"
    assert "ice_balance" in result, "Should have ICE balance metric"
    assert "overall_harmony" in result, "Should have overall harmony"
    assert 0 <= result["overall_harmony"] <= 1, "Harmony should be 0-1"

    print(f"✓ ICE analysis complete: {result['harmony_level']}")
    print(f"  Coherence: {result['ice_coherence']:.0%}")
    print(f"  Balance: {result['ice_balance']:.0%}")
    print(f"  Harmony: {result['overall_harmony']:.0%}")


def test_coordinate_distance():
    """Test distance calculations"""
    vocab = NetworkVocabularyManager()

    c1 = Coordinates(1.0, 0.0, 0.0, 0.0)
    c2 = Coordinates(0.0, 1.0, 0.0, 0.0)

    distance = vocab.get_distance(c1, c2)
    expected = (2 ** 0.5)  # sqrt(2)

    assert abs(distance - expected) < 0.01, f"Distance should be ~{expected}"
    print(f"✓ Distance calculation: {distance:.3f}")


def test_semantic_clarity():
    """Test semantic clarity calculation"""
    vocab = NetworkVocabularyManager()

    # Pure/specialized coordinate (low balance/clarity = highly focused)
    pure = Coordinates(1.0, 0.0, 0.0, 0.0)
    clarity_pure = vocab.get_semantic_clarity(pure)
    assert clarity_pure < 0.5, "Specialized coordinate should have low balance"

    # Balanced coordinate (high balance/clarity = well-distributed)
    balanced = Coordinates(0.25, 0.25, 0.25, 0.25)
    clarity_balanced = vocab.get_semantic_clarity(balanced)
    assert clarity_balanced > 0.8, "Balanced coordinate should have high balance"

    print(f"✓ Semantic balance - Specialized: {clarity_pure:.0%}, Balanced: {clarity_balanced:.0%}")


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("NETWORK-PINPOINTER SEMANTIC ENGINE TESTS")
    print("=" * 70)
    print()

    tests = [
        ("Vocabulary Initialization", test_vocabulary_initialization),
        ("Network Operation Analysis", test_network_operation_analysis),
        ("ICE Framework Analysis", test_ice_analysis),
        ("Coordinate Distance", test_coordinate_distance),
        ("Semantic Clarity", test_semantic_clarity),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        print(f"\nTesting: {test_name}")
        print("-" * 70)
        try:
            test_func()
            passed += 1
            print(f"✅ {test_name} PASSED\n")
        except AssertionError as e:
            failed += 1
            print(f"❌ {test_name} FAILED: {e}\n")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name} ERROR: {e}\n")

    print("=" * 70)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 70)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
