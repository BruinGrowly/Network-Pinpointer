#!/usr/bin/env python3
"""
Demonstration: How LJPW Semantic Interpretation Adds Context

Shows real examples of tool output → semantic interpretation → actionable diagnosis
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from network_pinpointer.semantic_engine import NetworkSemanticEngine
from network_pinpointer.semantic_interpreter import SemanticToolInterpreter


def demo_ping_interpretation():
    """Demo: How ping results get semantic context"""
    print("\n" + "=" * 70)
    print("DEMO 1: Ping Semantic Interpretation")
    print("=" * 70)

    engine = NetworkSemanticEngine()
    interpreter = SemanticToolInterpreter(engine)

    scenarios = [
        {
            "name": "Healthy Connection",
            "host": "8.8.8.8",
            "sent": 10,
            "received": 10,
            "latency": 15.0,
            "loss": 0.0,
        },
        {
            "name": "Packet Loss",
            "host": "slow-server.com",
            "sent": 10,
            "received": 5,
            "latency": 100.0,
            "loss": 50.0,
        },
        {
            "name": "High Latency",
            "host": "distant-server.com",
            "sent": 10,
            "received": 10,
            "latency": 350.0,
            "loss": 0.0,
        },
        {
            "name": "Complete Failure",
            "host": "unreachable.com",
            "sent": 10,
            "received": 0,
            "latency": 0.0,
            "loss": 100.0,
        },
    ]

    for scenario in scenarios:
        print(f"\n{'─' * 70}")
        print(f"Scenario: {scenario['name']}")
        print(f"{'─' * 70}")

        # Raw tool output
        print(f"\nRAW TOOL OUTPUT:")
        print(f"  Host: {scenario['host']}")
        print(f"  Packets: {scenario['received']}/{scenario['sent']} received")
        print(f"  Loss: {scenario['loss']:.0f}%")
        print(f"  Latency: {scenario['latency']:.0f}ms")

        # Semantic interpretation
        result = interpreter.interpret_ping(
            host=scenario["host"],
            packets_sent=scenario["sent"],
            packets_received=scenario["received"],
            avg_latency=scenario["latency"],
            packet_loss=scenario["loss"],
        )

        print(f"\n📊 SEMANTIC INTERPRETATION:")
        print(f"  Coordinates: {result.coordinates}")
        print(f"  Context: {result.context}")
        print(f"  Diagnosis: {result.diagnosis}")
        print(f"  Confidence: {result.confidence:.0%}")

        if result.recommendations:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in result.recommendations:
                print(f"    → {rec}")

        # Show what LJPW reveals
        l, j, p, w = result.coordinates
        print(f"\n🔍 LJPW INSIGHT:")
        if l < 0.5:
            print(f"    ⚠️  Love={l:.2f} - Connectivity is compromised")
        if p < 0.5:
            print(f"    ⚠️  Power={p:.2f} - Performance is degraded")
        if w < 0.5:
            print(f"    ⚠️  Wisdom={w:.2f} - Limited visibility into issue")


def demo_port_scan_interpretation():
    """Demo: Different port states have different semantic meanings"""
    print("\n\n" + "=" * 70)
    print("DEMO 2: Port Scan Semantic Interpretation")
    print("=" * 70)

    engine = NetworkSemanticEngine()
    interpreter = SemanticToolInterpreter(engine)

    scenarios = [
        {
            "name": "Open Port (Service Running)",
            "port": 80,
            "state": "open",
            "response_time": 5.0,
        },
        {
            "name": "Closed Port (Connection Refused)",
            "port": 3306,
            "state": "closed",
            "response_time": 2.0,
        },
        {
            "name": "Filtered Port (Firewall Block)",
            "port": 22,
            "state": "filtered",
            "response_time": 1000.0,
        },
    ]

    for scenario in scenarios:
        print(f"\n{'─' * 70}")
        print(f"Scenario: {scenario['name']}")
        print(f"{'─' * 70}")

        print(f"\nRAW TOOL OUTPUT:")
        print(f"  Port: {scenario['port']}")
        print(f"  State: {scenario['state']}")
        print(f"  Response: {scenario['response_time']:.0f}ms")

        result = interpreter.interpret_port_scan(
            host="target-server",
            port=scenario["port"],
            state=scenario["state"],
            response_time=scenario["response_time"],
        )

        print(f"\n📊 SEMANTIC INTERPRETATION:")
        print(f"  Coordinates: {result.coordinates}")
        print(f"  Context: {result.context}")

        # Key insight: same "can't connect" but different SEMANTIC MEANING
        l, j, p, w = result.coordinates
        print(f"\n🔍 SEMANTIC DIFFERENCE:")

        if scenario["state"] == "closed":
            print("    This is a POWER issue (active rejection)")
            print("    → Service explicitly refusing connections")
            print(
                "    → NOT a firewall (that would be Justice-dominant with no response)"
            )

        elif scenario["state"] == "filtered":
            print("    This is a JUSTICE issue (policy enforcement)")
            print("    → Firewall silently dropping packets")
            print(
                "    → NOT a service issue (that would send RST and be Power-dominant)"
            )

        elif scenario["state"] == "open":
            print("    This is healthy LOVE (connectivity working)")
            print("    → Service available and accepting connections")


def demo_correlation():
    """Demo: Correlating multiple tools for holistic diagnosis"""
    print("\n\n" + "=" * 70)
    print("DEMO 3: Multi-Tool Correlation - Finding Root Cause")
    print("=" * 70)

    engine = NetworkSemanticEngine()
    interpreter = SemanticToolInterpreter(engine)

    print("\nScenario: Website not loading")
    print("Running diagnostics...\n")

    # Test 1: Ping (network layer)
    print("Step 1: Test network connectivity")
    ping_result = interpreter.interpret_ping(
        host="webserver.com",
        packets_sent=10,
        packets_received=10,
        avg_latency=12.0,
        packet_loss=0.0,
    )
    print(f"  Ping: {ping_result.context}")
    print(f"  LJPW: {ping_result.coordinates}")

    # Test 2: Port 80 (transport layer)
    print("\nStep 2: Test HTTP port accessibility")
    port_result = interpreter.interpret_port_scan(
        host="webserver.com", port=80, state="open", response_time=5.0
    )
    print(f"  Port 80: {port_result.context}")
    print(f"  LJPW: {port_result.coordinates}")

    # Test 3: HTTP request fails (application layer)
    # Simulating with port timeout for demo
    print("\nStep 3: Test HTTP application response")
    app_result = interpreter.interpret_port_scan(
        host="webserver.com", port=80, state="timeout", response_time=5000.0
    )
    print(f"  HTTP: Application not responding")
    print(f"  LJPW: {app_result.coordinates}")

    # Correlate all results
    print("\n" + "─" * 70)
    print("CORRELATION ANALYSIS")
    print("─" * 70)

    correlated = interpreter.correlate_multi_tool(
        [ping_result, port_result, app_result]
    )

    print(f"\n🎯 HOLISTIC DIAGNOSIS:")
    print(f"  Aggregate LJPW: {correlated.coordinates}")
    print(f"  Context: {correlated.context}")
    print(f"  Diagnosis: {correlated.diagnosis}")
    print(f"  Confidence: {correlated.confidence:.0%}")

    print(f"\n🔍 SEMANTIC ANALYSIS:")
    print("  Layer 1 (Network): Love=0.9 ✓ HEALTHY")
    print("  Layer 2 (Transport): Love=0.8 ✓ HEALTHY")
    print("  Layer 3 (Application): Love=0.0 ✗ FAILED")
    print("\n  Conclusion: Problem is APPLICATION-LEVEL, not network")
    print("  Network and port are fine, but web server isn't responding")

    print(f"\n💡 ACTIONABLE RECOMMENDATIONS:")
    for rec in correlated.recommendations:
        print(f"    → {rec}")


def demo_traceroute_patterns():
    """Demo: Different traceroute patterns reveal different issues"""
    print("\n\n" + "=" * 70)
    print("DEMO 4: Traceroute Pattern Recognition")
    print("=" * 70)

    engine = NetworkSemanticEngine()
    interpreter = SemanticToolInterpreter(engine)

    patterns = [
        {
            "name": "Healthy Path",
            "hops": [
                {"hop_number": 1, "host": "router1", "latency": 2},
                {"hop_number": 2, "host": "router2", "latency": 5},
                {"hop_number": 3, "host": "router3", "latency": 8},
                {"hop_number": 4, "host": "target", "latency": 12},
            ],
        },
        {
            "name": "Bottleneck at Hop 3",
            "hops": [
                {"hop_number": 1, "host": "router1", "latency": 2},
                {"hop_number": 2, "host": "router2", "latency": 5},
                {"hop_number": 3, "host": "slow-router", "latency": 250},
                {"hop_number": 4, "host": "target", "latency": 255},
            ],
        },
        {
            "name": "Firewall Obscuring Path",
            "hops": [
                {"hop_number": 1, "host": "router1", "latency": 2},
                {"hop_number": 2, "host": "router2", "latency": 5},
                {"hop_number": 3, "host": "*", "latency": 0, "timeout": True},
                {"hop_number": 4, "host": "*", "latency": 0, "timeout": True},
                {"hop_number": 5, "host": "*", "latency": 0, "timeout": True},
            ],
        },
    ]

    for pattern in patterns:
        print(f"\n{'─' * 70}")
        print(f"Pattern: {pattern['name']}")
        print(f"{'─' * 70}")

        print(f"\nRAW TRACEROUTE:")
        for hop in pattern["hops"]:
            if hop.get("timeout"):
                print(f"  {hop['hop_number']:2d}. * * * (timeout)")
            else:
                print(
                    f"  {hop['hop_number']:2d}. {hop['host']:20s} {hop['latency']:3.0f}ms"
                )

        result = interpreter.interpret_traceroute(
            target="destination", hops=pattern["hops"], success=True
        )

        print(f"\n📊 SEMANTIC INTERPRETATION:")
        print(f"  LJPW: {result.coordinates}")
        print(f"  Context: {result.context}")
        print(f"  Diagnosis: {result.diagnosis}")

        # Explain what pattern means
        l, j, p, w = result.coordinates
        print(f"\n🔍 PATTERN MEANING:")

        if j > 0.6:
            print("    High Justice = Firewalls blocking ICMP visibility")
            print("    This is NORMAL for security-conscious networks")
            print("    Try TCP-based traceroute to see full path")

        elif p < 0.3:
            print("    Low Power = Performance bottleneck detected")
            print("    One hop is causing significant delay")
            print("    This is a CONGESTION/BANDWIDTH issue")

        elif l > 0.8 and p > 0.8:
            print("    High Love + High Power = Optimal path")
            print("    Clean route with good performance")


def main():
    """Run all demonstrations"""
    print("\n" + "=" * 70)
    print("SEMANTIC INTERPRETATION: Tool Output → LJPW Context → Understanding")
    print("=" * 70)

    demo_ping_interpretation()
    demo_port_scan_interpretation()
    demo_correlation()
    demo_traceroute_patterns()

    print("\n\n" + "=" * 70)
    print("KEY TAKEAWAYS")
    print("=" * 70)
    print("""
1. LJPW adds MEANING to raw numbers
   - Not just "packet loss" but "Love dimension collapsed"
   - Not just "timeout" but "Justice blocking visibility"

2. Same symptom, different semantic causes
   - Connection refused (Power) vs Firewall drop (Justice)
   - Both are "can't connect" but MEAN different things

3. Multi-tool correlation finds root cause
   - Ping good + Port bad = Application layer issue
   - All layers bad = Network infrastructure issue

4. Patterns have semantic signatures
   - High Justice + Low Wisdom = Firewall obscuring path
   - Low Power + High Wisdom = Visible bottleneck

5. Context emerges from coordinates
   - The LJPW values ARE the context
   - They tell you WHAT TYPE of problem
   - They guide you to the root cause

This is not just relabeling - it's adding a semantic reasoning layer
that enables diagnosis like a human network engineer would think.
    """)


if __name__ == "__main__":
    main()
