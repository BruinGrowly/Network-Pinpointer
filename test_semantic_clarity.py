#!/usr/bin/env python3
"""
Test Semantic Clarity Principle

Demonstrates how description richness affects semantic clarity.
"""

import sys
import io

# Configure UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, '.')

from network_pinpointer.semantic_engine import NetworkSemanticEngine
from network_pinpointer.semantic_clarity import SemanticClarityAnalyzer


def test_web_server_progression():
    """Test clarity progression for a web server"""
    
    print("🔬 SEMANTIC CLARITY ANALYSIS: Web Server")
    print("=" * 70)
    print("\nTesting hypothesis: More description → Higher clarity\n")
    
    # Initialize
    engine = NetworkSemanticEngine()
    analyzer = SemanticClarityAnalyzer(engine)
    
    # Define enrichment levels
    base = "web server"
    enrichments = [
        # Level 1: Basic connectivity
        ["http", "https", "public", "accessible"],
        
        # Level 2: Add security
        ["http", "https", "public", "accessible", "secure", "encrypted", "firewall", "protected"],
        
        # Level 3: Add performance
        ["http", "https", "public", "accessible", "secure", "encrypted", "firewall", "protected",
         "performance", "optimized", "load", "balanced", "cache"],
        
        # Level 4: Add monitoring
        ["http", "https", "public", "accessible", "secure", "encrypted", "firewall", "protected",
         "performance", "optimized", "load", "balanced", "cache",
         "monitored", "logging", "metrics", "alerts", "diagnostic", "troubleshoot"]
    ]
    
    level_names = ["Minimal", "Basic", "Moderate", "Detailed", "Rich"]
    
    # Analyze progression
    progression = analyzer.analyze_description_levels(base, enrichments, level_names)
    
    # Print results
    print("━" * 70)
    
    for level_data in progression.levels:
        print(f"\nLEVEL {level_data.level}: {level_data.name} ({level_data.word_count} words)")
        print(f"Description: \"{level_data.description}\"")
        print()
        print(f"Coordinates: L={level_data.coords.love:.2f}, J={level_data.coords.justice:.2f}, "
              f"P={level_data.coords.power:.2f}, W={level_data.coords.wisdom:.2f}")
        print(f"Clarity:     {level_data.clarity:.0%}")
        print(f"Concepts:    {level_data.concepts}")
        print(f"Harmony:     {level_data.harmony:.0%}")
        print(f"Balance:     {level_data.balance:.0%}")
        print(f"Entropy:     {level_data.entropy:.0%}")
        print(f"Info Content: {level_data.information_content:.1f}")
        
        # Analysis
        dims_represented = sum([
            1 for d in [level_data.coords.love, level_data.coords.justice,
                       level_data.coords.power, level_data.coords.wisdom]
            if d > 0.1
        ])
        print(f"\nAnalysis: {dims_represented}/4 dimensions represented", end="")
        
        if dims_represented == 4:
            print(" - Fully multi-dimensional!")
        elif dims_represented >= 2:
            print(" - Multi-dimensional")
        else:
            print(" - Single-dimensional")
        
        print("\n" + "━" * 70)
    
    # Print progression analysis
    print("\n📈 PROGRESSION ANALYSIS\n")
    
    first = progression.levels[0]
    last = progression.levels[-1]
    
    print(f"Clarity Trend:    {first.clarity:.0%} → {last.clarity:.0%}  "
          f"{'✅' if last.clarity > first.clarity else '❌'} "
          f"{'+' if last.clarity > first.clarity else ''}{(last.clarity - first.clarity):.0%}")
    
    print(f"Balance Trend:    {first.balance:.0%} → {last.balance:.0%}  "
          f"{'✅' if last.balance > first.balance else '❌'} "
          f"{'+' if last.balance > first.balance else ''}{(last.balance - first.balance):.0%}")
    
    print(f"Harmony Trend:    {first.harmony:.0%} → {last.harmony:.0%}  "
          f"{'✅' if last.harmony > first.harmony else '❌'} "
          f"{'+' if last.harmony > first.harmony else ''}{(last.harmony - first.harmony):.0%}")
    
    print(f"Concept Growth:   {first.concepts} → {last.concepts}         "
          f"✅ {last.concepts / first.concepts if first.concepts > 0 else 0:.1f}x")
    
    # Print insights
    print("\n💡 INSIGHTS")
    for insight in progression.insights:
        print(f"  {insight}")
    
    # Conclusion
    print("\n🎯 CONCLUSION")
    if progression.hypothesis_confirmed:
        print("  ✅ Hypothesis CONFIRMED: Richer descriptions produce:")
        print("     • Higher semantic clarity")
        print("     • Better dimensional balance")
        print("     • More accurate LJPW representation")
        print("     • Deeper understanding of system nature")
    else:
        print("  ❌ Hypothesis NOT confirmed")
    
    print("\n" + "=" * 70)


def test_description_quality():
    """Test description quality scoring"""
    
    print("\n\n📊 DESCRIPTION QUALITY SCORING")
    print("=" * 70)
    
    engine = NetworkSemanticEngine()
    analyzer = SemanticClarityAnalyzer(engine)
    
    descriptions = {
        "Minimal": "database",
        "Basic": "database server storage",
        "Good": "database server storage mysql secure backup replicated",
        "Excellent": "database server storage mysql secure backup replicated monitored performance optimized indexed query cache"
    }
    
    for name, desc in descriptions.items():
        print(f"\n{name}: \"{desc}\"")
        quality = analyzer.score_description_quality(desc)
        
        print(f"  Quality Score: {quality['quality']:.0%} [{quality['grade']}]")
        print(f"  Clarity:       {quality['clarity']:.0%}")
        print(f"  Balance:       {quality['balance']:.0%}")
        print(f"  Completeness:  {quality['completeness']:.0%}")
        print(f"  Entropy:       {quality['entropy']:.0%}")
        print(f"  Concepts:      {quality['concept_count']}")
    
    print("\n" + "=" * 70)


def test_enrichment_recommendations():
    """Test enrichment recommendations"""
    
    print("\n\n💡 ENRICHMENT RECOMMENDATIONS")
    print("=" * 70)
    
    engine = NetworkSemanticEngine()
    analyzer = SemanticClarityAnalyzer(engine)
    
    desc = "web server http"
    
    print(f"\nCurrent Description: \"{desc}\"")
    print(f"Target Clarity: 80%\n")
    
    recommendations = analyzer.recommend_enrichments(desc, target_clarity=0.8)
    
    if recommendations['needs_improvement']:
        print(f"Current Clarity: {recommendations['current_clarity']:.0%}")
        print(f"Gap to Target:   {recommendations['gap']:.0%}")
        print(f"\n📋 RECOMMENDATIONS:\n")
        
        for rec in recommendations['recommendations']:
            print(f"  {rec['dimension']}")
            if 'current' in rec:
                print(f"    Current: {rec['current']:.2f}")
            print(f"    {rec['suggestion']}")
            print(f"    Examples: {', '.join(rec['examples'])}")
            print()
    else:
        print(recommendations['message'])
    
    print("=" * 70)


def test_description_comparison():
    """Test description comparison"""
    
    print("\n\n⚖️  DESCRIPTION COMPARISON")
    print("=" * 70)
    
    engine = NetworkSemanticEngine()
    analyzer = SemanticClarityAnalyzer(engine)
    
    desc1 = "firewall security network"
    desc2 = "firewall security network protected encrypted monitored rules policies validation"
    
    print(f"\nDescription 1: \"{desc1}\"")
    print(f"Description 2: \"{desc2}\"")
    print()
    
    comparison = analyzer.compare_descriptions(desc1, desc2)
    
    print(f"Winner: Description {comparison['winner']}")
    print(f"Quality Difference: {comparison['quality_difference']:.0%}")
    print()
    
    print("Description 1 Quality:")
    q1 = comparison['description1']['quality']
    print(f"  Overall: {q1['quality']:.0%} [{q1['grade']}]")
    print(f"  Clarity: {q1['clarity']:.0%}, Balance: {q1['balance']:.0%}, "
          f"Completeness: {q1['completeness']:.0%}")
    
    print("\nDescription 2 Quality:")
    q2 = comparison['description2']['quality']
    print(f"  Overall: {q2['quality']:.0%} [{q2['grade']}]")
    print(f"  Clarity: {q2['clarity']:.0%}, Balance: {q2['balance']:.0%}, "
          f"Completeness: {q2['completeness']:.0%}")
    
    print("\nAnalysis:")
    for analysis in comparison['analysis']:
        print(f"  • {analysis}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    test_web_server_progression()
    test_description_quality()
    test_enrichment_recommendations()
    test_description_comparison()
    
    print("\n✅ All tests complete!")
