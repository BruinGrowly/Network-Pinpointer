#!/usr/bin/env python3
"""
Demonstration: Deep Metadata Extraction

Shows how LJPW extracts nuanced semantic meaning from protocol metadata.
Uses simulated data to demonstrate the analysis capabilities.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from network_pinpointer.metadata_extractor import MetadataExtractor


def demo_ttl_analysis():
    """Demonstrate TTL pattern analysis"""
    print("\n" + "="*70)
    print("DEMO 1: TTL Pattern Analysis")
    print("="*70)

    extractor = MetadataExtractor()

    scenarios = [
        {
            "name": "Stable Direct Path",
            "ttls": [60, 60, 60, 60, 60, 60, 60, 60],
            "description": "Consistent TTL = stable route, few hops"
        },
        {
            "name": "Route Changing (Load Balancing)",
            "ttls": [60, 60, 57, 60, 57, 60, 57, 60],
            "description": "TTL alternates = traffic using two different paths"
        },
        {
            "name": "Complex Distant Path",
            "ttls": [40, 40, 40, 40, 40, 40, 40, 40],
            "description": "Low TTL = many hops taken (distant or complex routing)"
        },
        {
            "name": "Unstable Routing",
            "ttls": [60, 57, 52, 58, 54, 60, 49, 55],
            "description": "Highly variable TTL = routing instability"
        },
    ]

    for scenario in scenarios:
        print(f"\n{'─'*70}")
        print(f"Scenario: {scenario['name']}")
        print(f"{'─'*70}")
        print(f"Description: {scenario['description']}")
        print(f"TTL Values: {scenario['ttls']}")

        result = extractor.extract_ttl_semantics(scenario['ttls'])

        print(f"\n📊 SEMANTIC ANALYSIS:")
        print(f"   Average Hops: {result.avg_hops:.1f}")
        print(f"   Hop Variance: {result.hop_variance:.2f}")
        print(f"   Path Complexity: {result.path_complexity}")
        print(f"   Path Stability: {result.path_stability:.0%}")
        print(f"   Route Changing: {'YES ⚠️' if result.route_changing else 'NO ✓'}")

        print(f"\n🎯 LJPW SCORES:")
        print(f"   Love (Connectivity): {result.love_score:.2f}")
        print(f"   Wisdom (Visibility): {result.wisdom_score:.2f}")

        print(f"\n💡 CONTEXT:")
        print(f"   {result.context}")


def demo_sequence_analysis():
    """Demonstrate sequence pattern analysis"""
    print("\n\n" + "="*70)
    print("DEMO 2: Sequence Pattern Analysis (Loss Detection)")
    print("="*70)

    extractor = MetadataExtractor()

    scenarios = [
        {
            "name": "No Loss (Perfect Delivery)",
            "sent": list(range(1, 11)),
            "received": list(range(1, 11)),
            "description": "All packets arrive"
        },
        {
            "name": "Random Loss (Noisy Link)",
            "sent": list(range(1, 11)),
            "received": [1, 2, 4, 5, 6, 8, 9, 10],  # 3, 7 missing randomly
            "description": "Random packet drops"
        },
        {
            "name": "Burst Loss (Congestion)",
            "sent": list(range(1, 11)),
            "received": [1, 2, 7, 8, 9, 10],  # 3,4,5,6 missing consecutively
            "description": "Consecutive packets lost = congestion/overload"
        },
        {
            "name": "Periodic Loss (QoS Policy)",
            "sent": list(range(1, 21)),
            "received": [1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20],  # Every 3rd missing
            "description": "Every 3rd packet filtered = rate limiting policy"
        },
    ]

    for scenario in scenarios:
        print(f"\n{'─'*70}")
        print(f"Scenario: {scenario['name']}")
        print(f"{'─'*70}")
        print(f"Description: {scenario['description']}")
        print(f"Sent: {scenario['sent']}")
        print(f"Received: {scenario['received']}")

        lost = set(scenario['sent']) - set(scenario['received'])
        if lost:
            print(f"Lost: {sorted(list(lost))}")

        result = extractor.extract_sequence_semantics(
            scenario['sent'],
            scenario['received']
        )

        print(f"\n📊 SEMANTIC ANALYSIS:")
        print(f"   Loss Rate: {result.loss_rate*100:.1f}%")
        print(f"   Pattern: {result.loss_pattern}")
        print(f"   Selective Filtering: {'YES - QoS DETECTED ⚠️' if result.selective_filtering else 'NO'}")

        print(f"\n🎯 LJPW SCORES:")
        print(f"   Love (Delivery): {result.love_score:.2f}")
        print(f"   Justice (Policy): {result.justice_score:.2f}")
        print(f"   Power (Link Quality): {result.power_score:.2f}")

        print(f"\n💡 CONTEXT:")
        print(f"   {result.context}")

        # KEY INSIGHT
        if result.selective_filtering:
            print(f"\n   🔍 KEY INSIGHT: This is NOT random network issues!")
            print(f"      A QoS policy is deliberately filtering traffic.")
            print(f"      This is a JUSTICE dimension issue (policy enforcement),")
            print(f"      not a POWER dimension issue (congestion/failure).")


def demo_timing_analysis():
    """Demonstrate timing pattern analysis"""
    print("\n\n" + "="*70)
    print("DEMO 3: Timing Pattern Analysis")
    print("="*70)

    extractor = MetadataExtractor()

    scenarios = [
        {
            "name": "Stable Performance",
            "latencies": [10.2, 10.5, 10.1, 10.3, 10.4, 10.2, 10.6, 10.1],
            "description": "Consistent low latency"
        },
        {
            "name": "Variable Performance (Some Congestion)",
            "latencies": [10, 15, 12, 25, 11, 18, 13, 22],
            "description": "Fluctuating latency"
        },
        {
            "name": "Bimodal Routing (Load Balancing)",
            "latencies": [10, 10, 50, 10, 50, 10, 50, 10, 50, 10],
            "description": "Two distinct latency modes = two different paths"
        },
        {
            "name": "Degrading Performance",
            "latencies": [10, 12, 15, 20, 30, 45, 65, 90],
            "description": "Latency increasing over time = congestion building"
        },
        {
            "name": "Improving Performance",
            "latencies": [90, 75, 60, 45, 30, 20, 15, 12],
            "description": "Latency decreasing over time = congestion clearing"
        },
    ]

    for scenario in scenarios:
        print(f"\n{'─'*70}")
        print(f"Scenario: {scenario['name']}")
        print(f"{'─'*70}")
        print(f"Description: {scenario['description']}")
        print(f"Latencies (ms): {[f'{l:.1f}' for l in scenario['latencies']]}")

        result = extractor.extract_timing_semantics(scenario['latencies'])

        print(f"\n📊 SEMANTIC ANALYSIS:")
        print(f"   Average Latency: {result.avg_latency:.1f}ms")
        print(f"   Variance: {result.latency_variance:.2f}")
        print(f"   Stability: {result.stability_coefficient:.0%}")
        print(f"   Pattern: {result.pattern}")
        if result.trend:
            trend_icon = "📈" if result.trend == "improving" else "📉" if result.trend == "worsening" else "➡️"
            print(f"   Trend: {trend_icon} {result.trend}")

        print(f"\n🎯 LJPW SCORES:")
        print(f"   Power (Performance): {result.power_score:.2f}")
        print(f"   Love (Stability): {result.love_score:.2f}")

        print(f"\n💡 CONTEXT:")
        print(f"   {result.context}")

        # KEY INSIGHTS
        if result.pattern == "bimodal":
            print(f"\n   🔍 KEY INSIGHT: Traffic is using TWO different paths!")
            print(f"      This indicates load balancing or failover in action.")
            print(f"      Not a problem - actually a HIGH LOVE feature (redundancy).")

        elif result.trend == "worsening":
            print(f"\n   🔍 KEY INSIGHT: Performance is actively degrading!")
            print(f"      This is a POWER dimension issue getting worse.")
            print(f"      Action needed: Identify and address congestion source.")


def demo_combined_analysis():
    """Demonstrate combining all metadata analyses"""
    print("\n\n" + "="*70)
    print("DEMO 4: Combined Metadata Analysis (Holistic)")
    print("="*70)

    extractor = MetadataExtractor()

    print("\nScenario: Real-world problematic connection")
    print("─"*70)

    # Simulate a problematic connection
    ttls = [52, 49, 52, 52, 49, 52, 49, 52]  # Route changing
    sent_seqs = list(range(1, 21))
    recv_seqs = [1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20]  # Every 3rd missing
    latencies = [15, 20, 18, 35, 22, 40, 25, 45, 30, 50]  # Degrading

    print(f"TTL pattern: {ttls} (varies between 52 and 49)")
    print(f"Packet loss: {len(sent_seqs) - len(recv_seqs)}/{len(sent_seqs)} packets lost")
    print(f"Latency: {latencies} (increasing trend)")

    # Analyze each dimension
    ttl_sem = extractor.extract_ttl_semantics(ttls)
    seq_sem = extractor.extract_sequence_semantics(sent_seqs, recv_seqs)
    time_sem = extractor.extract_timing_semantics(latencies)

    # Combine
    combined = extractor.combine_metadata_semantics(ttl_sem, seq_sem, time_sem)

    print(f"\n📊 INDIVIDUAL ANALYSES:")
    print(f"\n1. TTL Analysis:")
    print(f"   {ttl_sem.context}")
    print(f"   Love: {ttl_sem.love_score:.2f}, Wisdom: {ttl_sem.wisdom_score:.2f}")

    print(f"\n2. Sequence Analysis:")
    print(f"   {seq_sem.context}")
    print(f"   Love: {seq_sem.love_score:.2f}, Justice: {seq_sem.justice_score:.2f}, Power: {seq_sem.power_score:.2f}")

    print(f"\n3. Timing Analysis:")
    print(f"   {time_sem.context}")
    print(f"   Power: {time_sem.power_score:.2f}, Love: {time_sem.love_score:.2f}")

    print(f"\n🎯 COMBINED LJPW ANALYSIS:")
    coords = combined['coordinates']
    print(f"   Love:    {coords['love']:.2f}  {'█' * int(coords['love'] * 20)}")
    print(f"   Justice: {coords['justice']:.2f}  {'█' * int(coords['justice'] * 20)}")
    print(f"   Power:   {coords['power']:.2f}  {'█' * int(coords['power'] * 20)}")
    print(f"   Wisdom:  {coords['wisdom']:.2f}  {'█' * int(coords['wisdom'] * 20)}")

    print(f"\n🏥 OVERALL HEALTH: {combined['overall_health']:.0%}")

    print(f"\n💡 HOLISTIC DIAGNOSIS:")
    print(f"   Primary Issue: Multiple problems detected")
    print(f"   1. Route Instability (Love dimension low)")
    print(f"   2. QoS Policy Active (Justice dimension high)")
    print(f"   3. Performance Degrading (Power dimension low)")
    print(f"\n   Root Cause Hypothesis:")
    print(f"   Network is experiencing congestion AND has QoS policies active.")
    print(f"   The QoS is rate-limiting this traffic (periodic drops),")
    print(f"   while the network itself is also becoming congested (degrading latency),")
    print(f"   and routes are changing (possibly trying to avoid congestion).")


def main():
    """Run all demonstrations"""
    print("\n" + "="*70)
    print("DEEP METADATA EXTRACTION: Nuanced Semantic Insights")
    print("="*70)
    print("\nDemonstrating how LJPW extracts meaning from protocol metadata fields")

    demo_ttl_analysis()
    demo_sequence_analysis()
    demo_timing_analysis()
    demo_combined_analysis()

    print("\n\n" + "="*70)
    print("KEY TAKEAWAYS")
    print("="*70)
    print("""
1. Every metadata field tells a story:
   - TTL variance → Route changing (Love instability)
   - Periodic loss → QoS policy (Justice enforcement)
   - Latency trend → Performance degrading (Power declining)

2. Same symptom, different semantic causes:
   - Random loss (Power) vs Periodic loss (Justice)
   - Both are "packet loss" but MEAN different things!

3. Patterns reveal architecture:
   - Bimodal latency = Load balancing detected
   - TTL alternation = Multiple paths in use
   - Burst loss = Congestion points

4. Combined analysis provides holistic diagnosis:
   - Individual signals can be ambiguous
   - Combined metadata reveals true root cause
   - LJPW coordinates emerge from multiple signals

5. Metadata extraction enables unlimited depth:
   - The more fields you parse, the more context you get
   - Each field adds nuance to the semantic interpretation
   - Framework can go as deep as protocols allow

This is how Network-Pinpointer provides nuanced insights that
traditional tools cannot - by extracting semantic meaning from
metadata patterns that humans would analyze intuitively.
    """)


if __name__ == "__main__":
    main()
