#!/usr/bin/env python3
"""
Network-Pinpointer CLI

Command-line interface for semantic network diagnostics and analysis.
"""

import argparse
import sys
from typing import Optional

from .semantic_engine import NetworkSemanticEngine
from .diagnostics import NetworkDiagnostics
from .network_mapper import NetworkMapper


def print_banner():
    """Print application banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                    NETWORK-PINPOINTER                         ║
║           Semantic Network Diagnostic Tool (LJPW)             ║
╚═══════════════════════════════════════════════════════════════╝

Love, Justice, Power, Wisdom - The Four Dimensions of Network Operations
"""
    print(banner)


def cmd_ping(args, engine: NetworkSemanticEngine):
    """Handle ping command"""
    diagnostics = NetworkDiagnostics(engine)

    print(f"\n🔍 Pinging {args.host}...")
    print("=" * 70)

    result = diagnostics.ping(args.host, count=args.count, timeout=args.timeout)

    # Print results
    print(f"\nHost: {result.host}")
    print(f"Status: {'✓ Reachable' if result.success else '✗ Unreachable'}")

    if result.success:
        print(f"Packets: {result.packets_received}/{result.packets_sent} received")
        print(f"Packet Loss: {result.packet_loss:.1f}%")
        print(f"Average Latency: {result.avg_latency:.1f}ms")

    # Semantic analysis
    print(f"\n📊 SEMANTIC ANALYSIS")
    print(f"Coordinates: {result.semantic_coords}")
    print(f"Analysis: {result.semantic_analysis}")

    # Visual representation
    l, j, p, w = result.semantic_coords
    print(f"\nDimension Breakdown:")
    print(f"  Love (Connectivity):  {'█' * int(l * 20):20s} {l:.0%}")
    print(f"  Justice (Validation): {'█' * int(j * 20):20s} {j:.0%}")
    print(f"  Power (Execution):    {'█' * int(p * 20):20s} {p:.0%}")
    print(f"  Wisdom (Diagnostic):  {'█' * int(w * 20):20s} {w:.0%}")

    print("\n" + "=" * 70)


def cmd_traceroute(args, engine: NetworkSemanticEngine):
    """Handle traceroute command"""
    diagnostics = NetworkDiagnostics(engine)

    print(f"\n🔍 Tracing route to {args.target}...")
    print("=" * 70)

    result = diagnostics.traceroute(
        args.target, max_hops=args.max_hops, timeout=args.timeout
    )

    # Print results
    print(f"\nTarget: {result.target}")
    print(f"Total Hops: {result.total_hops}")

    if result.hops:
        print(f"\nRoute:")
        for hop in result.hops:
            print(
                f"  {hop.hop_number:2d}. {hop.host:20s} ({hop.ip:15s}) - {hop.latency:.1f}ms"
            )

    # Semantic analysis
    print(f"\n📊 SEMANTIC ANALYSIS")
    print(f"Coordinates: {result.semantic_coords}")
    print(f"Analysis: {result.semantic_analysis}")

    l, j, p, w = result.semantic_coords
    print(f"\nDimension Breakdown:")
    print(f"  Love (Path Discovery): {'█' * int(l * 20):20s} {l:.0%}")
    print(f"  Justice (Validation):  {'█' * int(j * 20):20s} {j:.0%}")
    print(f"  Power (Execution):     {'█' * int(p * 20):20s} {p:.0%}")
    print(f"  Wisdom (Analysis):     {'█' * int(w * 20):20s} {w:.0%}")

    print("\n" + "=" * 70)


def cmd_scan(args, engine: NetworkSemanticEngine):
    """Handle port scan command"""
    diagnostics = NetworkDiagnostics(engine)

    # Parse port range
    if "-" in args.ports:
        start, end = map(int, args.ports.split("-"))
        ports = list(range(start, end + 1))
    else:
        ports = [int(p) for p in args.ports.split(",")]

    print(f"\n🔍 Scanning {args.host} ports {args.ports}...")
    print("=" * 70)

    results = diagnostics.scan_ports(args.host, ports, timeout=args.timeout)

    # Print results
    open_ports = [r for r in results if r.is_open]
    closed_ports = [r for r in results if not r.is_open]

    print(f"\nHost: {args.host}")
    print(f"Open Ports: {len(open_ports)}/{len(results)}")

    if open_ports:
        print(f"\n✓ OPEN PORTS:")
        for result in open_ports:
            print(
                f"  {result.port:5d}/tcp - {result.service_name:15s} - {result.semantic_coords}"
            )

    if args.verbose and closed_ports:
        print(f"\n✗ CLOSED PORTS:")
        for result in closed_ports[:10]:  # Limit output
            print(f"  {result.port:5d}/tcp - closed")
        if len(closed_ports) > 10:
            print(f"  ... and {len(closed_ports) - 10} more closed ports")

    # Aggregate semantic analysis
    if open_ports:
        avg_l = sum(r.semantic_coords.love for r in open_ports) / len(open_ports)
        avg_j = sum(r.semantic_coords.justice for r in open_ports) / len(open_ports)
        avg_p = sum(r.semantic_coords.power for r in open_ports) / len(open_ports)
        avg_w = sum(r.semantic_coords.wisdom for r in open_ports) / len(open_ports)

        print(f"\n📊 AGGREGATE SEMANTIC ANALYSIS")
        print(f"  Love (Services):      {'█' * int(avg_l * 20):20s} {avg_l:.0%}")
        print(f"  Justice (Security):   {'█' * int(avg_j * 20):20s} {avg_j:.0%}")
        print(f"  Power (Capability):   {'█' * int(avg_p * 20):20s} {avg_p:.0%}")
        print(f"  Wisdom (Discovery):   {'█' * int(avg_w * 20):20s} {avg_w:.0%}")

    print("\n" + "=" * 70)


def cmd_map(args, engine: NetworkSemanticEngine):
    """Handle network mapping command"""
    mapper = NetworkMapper(engine, quiet=args.quiet)

    print_banner()

    report = mapper.scan_network(args.network, common_ports=None)

    if "error" in report:
        print(f"❌ Error: {report['error']}")
        sys.exit(1)

    mapper.print_report(report)

    # Export if requested
    if args.export_json:
        mapper.export_topology_json(args.export_json)


def cmd_analyze(args, engine: NetworkSemanticEngine):
    """Analyze a network operation description"""
    print(f"\n🔍 Analyzing operation: '{args.operation}'")
    print("=" * 70)

    result = engine.analyze_operation(args.operation)

    print(f"\nOperation Type: {result.operation_type}")
    print(f"Dominant Dimension: {result.dominant_dimension}")
    print(f"Semantic Clarity: {result.semantic_clarity:.0%}")
    print(f"Harmony Score: {result.harmony_score:.0%}")

    print(f"\n📊 LJPW COORDINATES")
    print(f"Coordinates: {result.coordinates}")

    l, j, p, w = result.coordinates
    print(f"\nDimension Breakdown:")
    print(f"  Love (Connectivity):  {'█' * int(l * 40):40s} {l:.0%}")
    print(f"  Justice (Policy):     {'█' * int(j * 40):40s} {j:.0%}")
    print(f"  Power (Execution):    {'█' * int(p * 40):40s} {p:.0%}")
    print(f"  Wisdom (Information): {'█' * int(w * 40):40s} {w:.0%}")

    print(f"\nDistance from Anchor: {result.distance_from_anchor:.3f}")
    print(f"Concept Count: {result.concept_count}")

    print("\n" + "=" * 70)


def cmd_ice(args, engine: NetworkSemanticEngine):
    """Analyze Intent-Context-Execution harmony"""
    print(f"\n🔍 ICE HARMONY ANALYSIS")
    print("=" * 70)

    print(f"\nIntent:    {args.intent}")
    print(f"Context:   {args.context}")
    print(f"Execution: {args.execution}")

    result = engine.analyze_ice(args.intent, args.context, args.execution)

    print(f"\n📊 HARMONY METRICS")
    print(f"ICE Coherence:     {result['ice_coherence']:.0%}")
    print(f"ICE Balance:       {result['ice_balance']:.0%}")
    print(f"Overall Harmony:   {result['overall_harmony']:.0%}")
    print(f"Harmony Level:     {result['harmony_level']}")
    print(f"Benevolence Score: {result['benevolence_score']:.0%}")
    print(
        f"Intent-Execution Disharmony: {result['intent_execution_disharmony']:.3f}"
    )

    # Show individual components
    print(f"\n📍 COMPONENT COORDINATES")
    intent_result = result["intent"]
    context_result = result["context"]
    execution_result = result["execution"]

    print(f"\nIntent:    {intent_result.coordinates}")
    print(f"  Type: {intent_result.operation_type} ({intent_result.dominant_dimension})")

    print(f"\nContext:   {context_result.coordinates}")
    print(
        f"  Type: {context_result.operation_type} ({context_result.dominant_dimension})"
    )

    print(f"\nExecution: {execution_result.coordinates}")
    print(
        f"  Type: {execution_result.operation_type} ({execution_result.dominant_dimension})"
    )

    # Recommendations
    print(f"\n💡 RECOMMENDATIONS")
    if result["overall_harmony"] < 0.5:
        print(
            "⚠️  Low harmony detected - intent and execution are misaligned"
        )
        if result["intent_execution_disharmony"] > 1.0:
            print(
                "  → Review if the executed action matches the intended goal"
            )
        if result["ice_balance"] < 0.5:
            print(
                "  → Check if current context supports the intended operation"
            )
    elif result["overall_harmony"] < 0.7:
        print(
            "✓ Moderate harmony - minor misalignment between components"
        )
    else:
        print(
            "✅ Excellent harmony - intent, context, and execution are well-aligned"
        )

    print("\n" + "=" * 70)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Network-Pinpointer: Semantic Network Diagnostic Tool (LJPW Framework)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Ping command
    ping_parser = subparsers.add_parser("ping", help="Ping a host with semantic analysis")
    ping_parser.add_argument("host", help="Target host (IP or hostname)")
    ping_parser.add_argument(
        "-c", "--count", type=int, default=4, help="Number of packets to send"
    )
    ping_parser.add_argument(
        "-t", "--timeout", type=int, default=5, help="Timeout in seconds"
    )

    # Traceroute command
    trace_parser = subparsers.add_parser(
        "traceroute", help="Trace route to target with semantic analysis"
    )
    trace_parser.add_argument("target", help="Target host (IP or hostname)")
    trace_parser.add_argument(
        "-m", "--max-hops", type=int, default=30, help="Maximum number of hops"
    )
    trace_parser.add_argument(
        "-t", "--timeout", type=int, default=5, help="Timeout per hop"
    )

    # Port scan command
    scan_parser = subparsers.add_parser("scan", help="Scan ports with semantic analysis")
    scan_parser.add_argument("host", help="Target host (IP or hostname)")
    scan_parser.add_argument(
        "-p",
        "--ports",
        default="22,80,443",
        help="Ports to scan (e.g., '80,443' or '1-1000')",
    )
    scan_parser.add_argument(
        "-t", "--timeout", type=float, default=1.0, help="Timeout per port"
    )
    scan_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show closed ports"
    )

    # Network map command
    map_parser = subparsers.add_parser(
        "map", help="Map entire network with semantic topology analysis"
    )
    map_parser.add_argument(
        "network", help="Network range in CIDR notation (e.g., 192.168.1.0/24)"
    )
    map_parser.add_argument(
        "--export-json", help="Export topology to JSON file"
    )
    map_parser.add_argument(
        "-q", "--quiet", action="store_true", help="Minimal output"
    )

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze", help="Analyze a network operation description"
    )
    analyze_parser.add_argument(
        "operation", help="Operation description (e.g., 'configure firewall rules')"
    )

    # ICE analysis command
    ice_parser = subparsers.add_parser(
        "ice", help="Analyze Intent-Context-Execution harmony"
    )
    ice_parser.add_argument("intent", help="Intended operation")
    ice_parser.add_argument("context", help="Current network context")
    ice_parser.add_argument("execution", help="Actual execution")

    args = parser.parse_args()

    if not args.command:
        print_banner()
        parser.print_help()
        sys.exit(1)

    # Initialize semantic engine
    engine = NetworkSemanticEngine()

    # Route to appropriate command handler
    if args.command == "ping":
        cmd_ping(args, engine)
    elif args.command == "traceroute":
        cmd_traceroute(args, engine)
    elif args.command == "scan":
        cmd_scan(args, engine)
    elif args.command == "map":
        cmd_map(args, engine)
    elif args.command == "analyze":
        cmd_analyze(args, engine)
    elif args.command == "ice":
        cmd_ice(args, engine)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
