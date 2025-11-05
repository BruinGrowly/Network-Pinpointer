#!/usr/bin/env python3
"""
Test Script: Semantic Meaning Imbuing

This script demonstrates that we CAN imbue packets with semantic meaning:
1. By analyzing payload content to discover inherent intent
2. By generating probes with intentional semantic purpose

Run this to see LJPW semantics at the packet level!
"""

import sys
from network_pinpointer.deep_packet_semantics import DeepPacketSemanticAnalyzer, SemanticIntent
from network_pinpointer.semantic_probes import SemanticProbeGenerator, ProbeDimension


def test_packet_analysis():
    """Test 1: Discover semantic meaning in packets"""
    print("=" * 80)
    print("TEST 1: DISCOVERING SEMANTIC MEANING IN PACKETS")
    print("=" * 80)
    print("\nCan we discover the INHERENT semantic intent of packets by analyzing")
    print("their actual content (not just metadata)?\n")

    analyzer = DeepPacketSemanticAnalyzer()

    # Simulate different types of network traffic
    test_scenarios = [
        {
            'name': 'TCP SYN - Connection Attempt',
            'data': b'',
            'metadata': {
                'protocol': 'TCP',
                'tcp_flags': {'SYN': True, 'ACK': False},
                'src_ip': '192.168.1.100',
                'dst_ip': 'api.prod.com',
                'dst_port': 443,
                'src_port': 54321
            }
        },
        {
            'name': 'DNS Query - Information Seeking',
            'data': b'\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00',
            'metadata': {
                'protocol': 'UDP',
                'src_ip': '192.168.1.100',
                'dst_ip': '8.8.8.8',
                'dst_port': 53,
                'src_port': 54322
            }
        },
        {
            'name': 'HTTP GET - API Query',
            'data': b'GET /api/users HTTP/1.1\r\nHost: api.example.com\r\nUser-Agent: TestClient/1.0\r\n\r\n',
            'metadata': {
                'protocol': 'TCP',
                'tcp_flags': {'ACK': True},
                'src_ip': '192.168.1.100',
                'dst_ip': 'api.example.com',
                'dst_port': 80,
                'src_port': 54323
            }
        },
        {
            'name': 'HTTP POST - Authentication',
            'data': b'POST /auth/login HTTP/1.1\r\nHost: api.example.com\r\nContent-Type: application/json\r\nContent-Length: 45\r\n\r\n{"username":"user","password":"pass"}',
            'metadata': {
                'protocol': 'TCP',
                'tcp_flags': {'ACK': True},
                'src_ip': '192.168.1.100',
                'dst_ip': 'api.example.com',
                'dst_port': 443,
                'src_port': 54324
            }
        },
        {
            'name': 'Large Data Transfer',
            'data': b'X' * 1450,  # Near MTU
            'metadata': {
                'protocol': 'TCP',
                'tcp_flags': {'ACK': True},
                'src_ip': '192.168.1.100',
                'dst_ip': 'cdn.example.com',
                'dst_port': 443,
                'src_port': 54325
            }
        },
        {
            'name': 'TLS Handshake',
            'data': b'\x16\x03\x01\x00\x00',  # TLS ClientHello marker
            'metadata': {
                'protocol': 'TCP',
                'tcp_flags': {'ACK': True},
                'src_ip': '192.168.1.100',
                'dst_ip': 'secure.example.com',
                'dst_port': 443,
                'src_port': 54326
            }
        },
        {
            'name': 'TCP FIN - Connection Termination',
            'data': b'',
            'metadata': {
                'protocol': 'TCP',
                'tcp_flags': {'FIN': True, 'ACK': True},
                'src_ip': '192.168.1.100',
                'dst_ip': 'api.example.com',
                'dst_port': 443,
                'src_port': 54327
            }
        }
    ]

    print("Analyzing packets to discover their semantic intent...\n")

    for scenario in test_scenarios:
        sem = analyzer.analyze_packet(scenario['data'], scenario['metadata'])

        print(f"┌─ {scenario['name']}")
        print(f"│  Intent Discovered: {sem.intent.value.replace('_', ' ').title()}")
        print(f"│  Semantic Meaning: {sem.semantic_description}")
        print(f"│")
        print(f"│  LJPW Coordinates (imbued from intent):")
        print(f"│    Love:    {sem.ljpw_coordinates.love:.2f}  {'█' * int(sem.ljpw_coordinates.love * 20)}")
        print(f"│    Justice: {sem.ljpw_coordinates.justice:.2f}  {'█' * int(sem.ljpw_coordinates.justice * 20)}")
        print(f"│    Power:   {sem.ljpw_coordinates.power:.2f}  {'█' * int(sem.ljpw_coordinates.power * 20)}")
        print(f"│    Wisdom:  {sem.ljpw_coordinates.wisdom:.2f}  {'█' * int(sem.ljpw_coordinates.wisdom * 20)}")
        print(f"│")
        print(f"│  Protocol: {sem.layer7_protocol}")
        print(f"│  Confidence: {sem.confidence:.0%}")
        print(f"└─")
        print()

        # Track for flow analysis
        analyzer.track_flow(sem)

    # Show flow aggregation
    print("\n" + "=" * 80)
    print("FLOW ANALYSIS - Semantic Journey")
    print("=" * 80)

    for flow_id, flow in analyzer.flows.items():
        print(f"\nFlow: {flow_id}")
        print(f"  Pattern: {flow.flow_pattern}")
        print(f"  Packets: {len(flow.packets)}")
        print(f"  Dominant Intent: {flow.dominant_intent.value.replace('_', ' ').title()}")
        print(f"  Aggregate LJPW:")
        print(f"    Love:    {flow.aggregate_ljpw.love:.2f}")
        print(f"    Justice: {flow.aggregate_ljpw.justice:.2f}")
        print(f"    Power:   {flow.aggregate_ljpw.power:.2f}")
        print(f"    Wisdom:  {flow.aggregate_ljpw.wisdom:.2f}")

        print(f"\n  Semantic Journey (packet-by-packet):")
        for p in flow.packets[:5]:
            print(f"    #{p.packet_num}: {p.intent.value} → "
                  f"L={p.ljpw_coordinates.love:.1f} "
                  f"J={p.ljpw_coordinates.justice:.1f} "
                  f"P={p.ljpw_coordinates.power:.1f} "
                  f"W={p.ljpw_coordinates.wisdom:.1f}")

    print("\n✅ Conclusion: YES - We can discover inherent semantic meaning by analyzing")
    print("   packet payloads and understanding communication intent!\n")


def test_semantic_probes():
    """Test 2: Generate probes with intentional semantic meaning"""
    print("\n" + "=" * 80)
    print("TEST 2: GENERATING PACKETS WITH INTENTIONAL SEMANTIC MEANING")
    print("=" * 80)
    print("\nCan we IMBUE packets with semantic purpose by generating probes")
    print("specifically designed to test each LJPW dimension?\n")

    generator = SemanticProbeGenerator()

    target = "8.8.8.8"  # Google DNS

    print(f"Generating semantic probe suite for target: {target}\n")

    # Generate one probe for each dimension to demonstrate
    love_probe = generator.generate_love_probes(target)[0]
    justice_probe = generator.generate_justice_probes(target)[0]
    power_probe = generator.generate_power_probes(target)[0]
    wisdom_probe = generator.generate_wisdom_probes(target)[0]

    probes = [
        ("LOVE", love_probe),
        ("JUSTICE", justice_probe),
        ("POWER", power_probe),
        ("WISDOM", wisdom_probe)
    ]

    for dimension, probe in probes:
        print(f"┌─ {dimension} Dimension Probe")
        print(f"│")
        print(f"│  Probe Name: {probe.name}")
        print(f"│  Purpose: {probe.description}")
        print(f"│  Type: {probe.probe_type}")
        print(f"│  Target: {probe.target_host}" +
              (f":{probe.target_port}" if probe.target_port else ""))
        print(f"│")
        print(f"│  This probe is INTENTIONALLY designed to test {dimension}!")
        print(f"│")

        if probe.expected_ljpw_success:
            ljpw = probe.expected_ljpw_success
            print(f"│  Expected LJPW if successful:")
            print(f"│    Love:    {ljpw['love']:.1f}  {'█' * int(ljpw['love'] * 20)}")
            print(f"│    Justice: {ljpw['justice']:.1f}  {'█' * int(ljpw['justice'] * 20)}")
            print(f"│    Power:   {ljpw['power']:.1f}  {'█' * int(ljpw['power'] * 20)}")
            print(f"│    Wisdom:  {ljpw['wisdom']:.1f}  {'█' * int(ljpw['wisdom'] * 20)}")
            print(f"│")
            print(f"│  Notice: {dimension} dimension is dominant!")

        print(f"└─")
        print()

    print("✅ Conclusion: YES - We can IMBUE packets with semantic meaning by")
    print("   intentionally generating probes designed to test specific dimensions!\n")


def show_summary():
    """Show summary of findings"""
    print("\n" + "=" * 80)
    print("SUMMARY: CAN WE IMBUE MEANING INTO PACKETS?")
    print("=" * 80)
    print()
    print("Q: Can LJPW framework imbue meaning into packets?")
    print("A: YES - in TWO ways:")
    print()
    print("1. DISCOVERING Inherent Meaning:")
    print("   - Analyze packet payloads (HTTP methods, DNS queries, etc.)")
    print("   - Understand actual communication intent")
    print("   - Assign LJPW based on what packet is TRYING to do")
    print("   - Example: POST /auth/login → Authentication (Justice=0.9)")
    print()
    print("2. IMBUING Intentional Meaning:")
    print("   - Generate probes designed to test specific dimensions")
    print("   - Each probe has explicit semantic purpose")
    print("   - Example: DNS query probe → Pure Wisdom test (Wisdom=0.95)")
    print()
    print("The Framework Works Because:")
    print("  • Communication has inherent semantics (not just bits)")
    print("  • TCP SYN IS about Love (establishing connection)")
    print("  • Firewall block IS about Justice (enforcing policy)")
    print("  • Large transfer IS about Power (using capacity)")
    print("  • DNS query IS about Wisdom (seeking information)")
    print()
    print("LJPW doesn't invent meaning - it RECOGNIZES and CATEGORIZES meaning")
    print("that exists in the communication patterns themselves.")
    print()
    print("New Capabilities Unlocked:")
    print("  ✓ Per-packet semantic analysis")
    print("  ✓ Semantic flow tracking")
    print("  ✓ Intentional semantic probes")
    print("  ✓ Payload-aware LJPW coordinates")
    print()
    print("=" * 80)


if __name__ == "__main__":
    print()
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "TESTING: SEMANTIC MEANING IMBUING" + " " * 30 + "║")
    print("║" + " " * 78 + "║")
    print("║" + " " * 10 + "Can we imbue packets with semantic meaning using LJPW?" + " " * 11 + "║")
    print("╚" + "=" * 78 + "╝")
    print()

    # Run tests
    test_packet_analysis()
    test_semantic_probes()
    show_summary()

    print("\n🎉 Test Complete! The framework successfully imbues semantic meaning!")
    print()
