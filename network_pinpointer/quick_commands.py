#!/usr/bin/env python3
"""
Quick Commands - Fast operations for common network diagnostics

Provides simple, single-command operations:
- quick-check: 30-second health assessment
- ping: Enhanced ping with semantic analysis
- health: Network health status
- explain: Natural language explanations
"""

import sys
from typing import Optional, List, Dict
import time

from .real_packet_capture import get_packet_capture, ICMPMetadata
from .semantic_packet_analyzer import SemanticPacketAnalyzer
from .holistic_health import NetworkHealthTracker
from .root_cause_analyzer import RootCauseAnalyzer
from .semantic_engine import Coordinates
from .cli_output import get_formatter, print_success, print_error, print_info


class QuickCommands:
    """Handler for quick command operations"""

    def __init__(self):
        self.fmt = get_formatter()
        self.capture = get_packet_capture()
        self.analyzer = SemanticPacketAnalyzer()
        self.root_cause = RootCauseAnalyzer()

    def quick_check(self, target: str = "8.8.8.8") -> bool:
        """
        Run a quick 30-second health check

        Args:
            target: Target to test (default: 8.8.8.8)

        Returns:
            True if healthy, False if issues found
        """
        print(self.fmt.section_header(f"Quick Health Check: {target}"))
        print(self.fmt.info(f"Running 30-second diagnostic...\n"))

        try:
            # Step 1: Basic ping test
            print(self.fmt.spinner("Testing connectivity...", 0))

            if hasattr(self.capture, 'capture_icmp_via_ping'):
                packets = self.capture.capture_icmp_via_ping(target, count=10)

                if not packets:
                    print_error(f"Cannot reach {target}")
                    return False

                print_success(f"Connectivity OK ({len(packets)}/10 packets received)")

                # Step 2: Semantic analysis
                print(self.fmt.spinner("Analyzing network semantics...", 1))
                result = self.analyzer.analyze_icmp_packets(packets)

                print("")
                print(self.fmt.coordinates_display(result.coordinates))
                print("")
                print(self.fmt.health_score_display(
                    (result.coordinates.love + result.coordinates.power +
                     result.coordinates.wisdom) / 3
                ))

                # Step 3: Quick diagnosis
                if result.health_assessment in ["EXCELLENT", "GOOD"]:
                    print_success(f"\nNetwork health: {result.health_assessment}")
                    return True
                else:
                    print(self.fmt.warning(f"\nNetwork health: {result.health_assessment}"))

                    # Show top issue
                    metadata = {
                        "packet_loss": 0,
                        "avg_ttl": sum(p.ttl for p in packets) / len(packets) if packets else 64
                    }
                    analysis = self.root_cause.analyze(result.coordinates, metadata)

                    if analysis.primary_issue:
                        print(self.fmt.subsection_header("\nPrimary Issue:"))
                        print(f"  {self.fmt.priority_indicator(analysis.primary_issue.severity.value)} "
                              f"{analysis.primary_issue.title}")
                        print(f"  {analysis.primary_issue.description}")

                        if analysis.primary_issue.recommendations:
                            print(f"\n  {self.fmt.bold('Quick Fix:')}")
                            print(f"    • {analysis.primary_issue.recommendations[0]}")

                    return False

            else:
                print_error("Packet capture not available")
                return False

        except Exception as e:
            print_error(f"Quick check failed: {e}")
            return False

    def enhanced_ping(
        self,
        target: str,
        count: int = 10,
        show_details: bool = True
    ) -> bool:
        """
        Enhanced ping with semantic analysis

        Args:
            target: Target to ping
            count: Number of packets
            show_details: Show detailed analysis

        Returns:
            True if successful
        """
        print(self.fmt.section_header(f"Enhanced Ping: {target}"))

        try:
            # Check if we have real packet capture (not fallback)
            from .real_packet_capture import FallbackPacketCapture
            use_packet_capture = (
                hasattr(self.capture, 'capture_icmp_via_ping') and
                not isinstance(self.capture, FallbackPacketCapture)
            )

            if use_packet_capture:
                print(self.fmt.progress_bar(0, count, prefix="Pinging"))

                packets = self.capture.capture_icmp_via_ping(target, count=count)

                print(self.fmt.progress_bar(count, count, prefix="Pinging"))

                if not packets:
                    print_error("No response received")
                    return False

                # Basic stats
                print(f"\n{self.fmt.subsection_header('Basic Statistics')}")
                print(f"  Packets sent: {count}")
                print(f"  Packets received: {len(packets)}")
                print(f"  Loss rate: {(count - len(packets)) / count * 100:.1f}%")

                if packets:
                    ttls = [p.ttl for p in packets]
                    print(f"  TTL: min={min(ttls)}, max={max(ttls)}, avg={sum(ttls)/len(ttls):.1f}")

                # Semantic analysis
                if show_details:
                    result = self.analyzer.analyze_icmp_packets(packets)

                    print(f"\n{self.fmt.subsection_header('Semantic Analysis')}")
                    print(self.fmt.coordinates_display(result.coordinates, show_labels=False))

                    if result.patterns_detected:
                        print(f"\n{self.fmt.subsection_header('Patterns Detected')}")
                        print(self.fmt.bullet_list(result.patterns_detected, indent=2))

                    if result.insights:
                        print(f"\n{self.fmt.subsection_header('Insights')}")
                        print(self.fmt.bullet_list(result.insights, indent=2))

                return True

            else:
                # Fallback to standard diagnostics ping when packet capture unavailable
                print_info("Using standard ping (packet capture not available)")
                from .diagnostics import NetworkDiagnostics
                from .semantic_engine import NetworkSemanticEngine

                engine = NetworkSemanticEngine()
                diagnostics = NetworkDiagnostics(engine)

                result = diagnostics.ping(target, count=count, timeout=2.0)

                # Print results
                print(f"\nHost: {result.host}")
                print(f"Status: {self.fmt.success('Reachable') if result.success else self.fmt.error('Unreachable')}")

                if result.success:
                    print(f"Packets: {result.packets_received}/{result.packets_sent} received")
                    print(f"Packet Loss: {result.packet_loss:.1f}%")
                    print(f"Average Latency: {result.avg_latency:.1f}ms")

                # Semantic analysis
                if show_details and result.semantic_coords:
                    print(f"\n{self.fmt.subsection_header('Semantic Analysis')}")
                    print(self.fmt.coordinates_display(result.semantic_coords, show_labels=False))
                    print(f"\n{result.semantic_analysis}")

                return result.success

        except Exception as e:
            print_error(f"Ping failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def show_health(self) -> bool:
        """
        Show current network health status

        Returns:
            True if healthy
        """
        try:
            tracker = NetworkHealthTracker()

            if not tracker.snapshots:
                print_info("No health history available. Run some diagnostics first.")
                return True

            # Get latest snapshot
            latest = list(tracker.snapshots)[-1]

            print(self.fmt.section_header("Network Health Status"))
            print(f"\n{self.fmt.subsection_header('Current State')}")
            print(f"Time: {latest.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Devices: {latest.device_count}")
            print(f"\n{self.fmt.health_score_display(latest.health_score)}")

            print(f"\n{self.fmt.coordinates_display(latest.aggregate_coords)}")

            # Show baseline comparison if available
            if tracker.baseline:
                print(f"\n{self.fmt.subsection_header('Baseline Comparison')}")
                expected = tracker.baseline.expected_coords

                print(self.fmt.comparison("Love", expected.love, latest.aggregate_coords.love))
                print(self.fmt.comparison("Justice", expected.justice, latest.aggregate_coords.justice))
                print(self.fmt.comparison("Power", expected.power, latest.aggregate_coords.power))
                print(self.fmt.comparison("Wisdom", expected.wisdom, latest.aggregate_coords.wisdom))

            # Show recent alerts
            if tracker.alerts:
                recent_alerts = list(tracker.alerts)[-3:]
                print(f"\n{self.fmt.subsection_header('Recent Alerts')}")
                for alert in recent_alerts:
                    print(f"  {self.fmt.priority_indicator(alert.severity)} {alert.dimension}: {alert.context}")

            return latest.health_score > 0.6

        except Exception as e:
            print_error(f"Failed to retrieve health: {e}")
            return False

    def explain(self, topic: str) -> None:
        """
        Explain a network concept or dimension

        Args:
            topic: What to explain (connectivity, security, performance, visibility, or a question)
        """
        topic_lower = topic.lower()

        # Map user-friendly names to internal names
        aliases = {
            "connectivity": "love",
            "connect": "love",
            "reachability": "love",
            "security": "justice",
            "policy": "justice",
            "access": "justice",
            "performance": "power",
            "speed": "power",
            "capacity": "power",
            "visibility": "wisdom",
            "monitoring": "wisdom",
            "observability": "wisdom",
        }

        # Resolve alias if present
        if topic_lower in aliases:
            topic_lower = aliases[topic_lower]

        explanations = {
            "love": """
{header}
CONNECTIVITY - Reachability & Relationships

What is Connectivity?
  Connectivity represents how well network components can reach and
  communicate with each other.

  Think of it as: "Can things reach each other?"

High Connectivity (0.7+) means:
  ✓ Strong, reliable reachability
  ✓ Low packet loss
  ✓ Stable routes
  ✓ Services can reach each other

Low Connectivity (<0.5) means:
  ✗ Reachability problems
  ✗ High packet loss
  ✗ Route failures
  ✗ Services isolated

What affects Connectivity:
  • Packet loss (drops Connectivity)
  • Route stability (stable = higher Connectivity)
  • Link quality (good links = higher Connectivity)
  • Network topology (well-connected = higher Connectivity)

How to improve Connectivity:
  1. Fix packet loss (check physical links)
  2. Optimize routing (reduce complexity)
  3. Add redundant paths (failover capability)
  4. Improve link quality (better equipment)
""",

            "justice": """
{header}
SECURITY - Access Control & Policies

What is Security?
  Security represents policy enforcement, access control, and boundaries
  in your network. It measures how much rules and restrictions are applied.

  Think of it as: "What rules govern access?"

High Security (0.7+) means:
  • Active access control enforcement
  • Strict firewall rules
  • Policy enforcement
  • Heavy restrictions

Low Security (<0.3) means:
  • Minimal restrictions
  • Open network
  • Few policies
  • May need more protection

What affects Security:
  • Firewall rules (more rules = higher Security)
  • ACLs and filters (restrictions = higher Security)
  • Authentication requirements (stricter = higher Security)
  • Policy enforcement (active = higher Security)

When is high Security good?
  ✓ High-security environments
  ✓ Compliance requirements
  ✓ DMZ or public-facing networks

When is high Security bad?
  ✗ Blocking legitimate traffic
  ✗ Over-restrictive policies
  ✗ Impeding productivity
""",

            "power": """
{header}
PERFORMANCE - Speed & Capacity

What is Performance?
  Performance represents the speed and capacity of your network.
  It measures how efficiently data flows and how much throughput
  is available.

  Think of it as: "How fast and capable is the network?"

High Performance (0.7+) means:
  ✓ Low latency
  ✓ Simple, direct paths
  ✓ High bandwidth available
  ✓ Efficient routing

Low Performance (<0.5) means:
  ✗ High latency
  ✗ Complex paths (many hops)
  ✗ Bandwidth saturation
  ✗ Bottlenecks

What affects Performance:
  • Path complexity (more hops = lower Performance)
  • Bandwidth (saturation = lower Performance)
  • Latency (high latency = lower Performance)
  • Congestion (traffic = lower Performance)

How to improve Performance:
  1. Optimize routing (reduce hops)
  2. Increase bandwidth (upgrade links)
  3. Add caching/CDN (reduce distance)
  4. Implement QoS (prioritize critical traffic)
  5. Use direct peering (bypass intermediaries)
""",

            "wisdom": """
{header}
VISIBILITY - Monitoring & Observability

What is Visibility?
  Visibility represents how well you can observe and understand your network.
  It measures the quality and completeness of information you have about
  network state.

  Think of it as: "How clearly can I see what's happening?"

High Visibility (0.7+) means:
  ✓ Clear observability
  ✓ Good monitoring
  ✓ Complete information
  ✓ Few blind spots

Low Visibility (<0.5) means:
  ✗ Limited observability
  ✗ Poor monitoring
  ✗ Information gaps
  ✗ Blind spots in network

What affects Visibility:
  • Monitoring tools (more tools = higher Visibility)
  • Logging (good logs = higher Visibility)
  • Metrics collection (richer data = higher Visibility)
  • Alerting systems (active = higher Visibility)

How to improve Visibility:
  1. Deploy monitoring tools (NetFlow, SNMP, etc.)
  2. Enable comprehensive logging
  3. Set up alerting and dashboards
  4. Add visibility at key points
  5. Implement network analytics
""",

            "ljpw": """
{header}
The Four Dimensions of Network Operations

The four dimensions work together to describe any network state:

Connectivity (L):
  Reachability, relationships, how things connect
  Example: Can services reach each other?

Security (J):
  Access control, policies, rules
  Example: Are firewalls blocking traffic?

Performance (P):
  Speed, capacity, throughput
  Example: Is the network fast enough?

Visibility (W):
  Monitoring, observability, diagnostics
  Example: Can we see what's happening?

Why these four?
  These dimensions are mathematically proven to be:
  • Complete: All network meaning can be expressed
  • Minimal: Can't remove any dimension
  • Orthogonal: Independent of each other

How to read coordinates:
  Coordinates(L=0.85, J=0.35, P=0.70, W=0.90)

  This means:
  - Excellent connectivity (L=0.85)
  - Minimal security restrictions (J=0.35)
  - Good performance (P=0.70)
  - Excellent visibility (W=0.90)

  Overall: Healthy, open, well-monitored network
"""
        }

        # Get explanation
        if topic_lower in explanations:
            explanation = explanations[topic_lower].format(
                header=self.fmt.section_header(f"Explaining: {topic.upper()}")
            )
            print(explanation)
        else:
            # Try to match keywords
            if "connect" in topic_lower or "reach" in topic_lower:
                self.explain("love")
            elif "firewall" in topic_lower or "block" in topic_lower or "security" in topic_lower:
                self.explain("justice")
            elif "slow" in topic_lower or "latency" in topic_lower or "performance" in topic_lower:
                self.explain("power")
            elif "monitor" in topic_lower or "visibility" in topic_lower or "see" in topic_lower:
                self.explain("wisdom")
            else:
                print(self.fmt.section_header("Help Topics"))
                print("\nAvailable topics to explain:")
                print(self.fmt.bullet_list([
                    "connectivity - Reachability dimension",
                    "security - Access control dimension",
                    "performance - Speed/capacity dimension",
                    "visibility - Monitoring dimension",
                    "ljpw - Overview of all dimensions"
                ], indent=2))


if __name__ == "__main__":
    # Demo quick commands
    commands = QuickCommands()

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "quick-check":
            target = sys.argv[2] if len(sys.argv) > 2 else "8.8.8.8"
            commands.quick_check(target)
        elif cmd == "ping":
            if len(sys.argv) < 3:
                print("Usage: quick_commands.py ping <target>")
            else:
                commands.enhanced_ping(sys.argv[2])
        elif cmd == "health":
            commands.show_health()
        elif cmd == "explain":
            if len(sys.argv) < 3:
                commands.explain("help")
            else:
                commands.explain(" ".join(sys.argv[2:]))
    else:
        print("Quick Commands Demo")
        print("\nUsage:")
        print("  python quick_commands.py quick-check [target]")
        print("  python quick_commands.py ping <target>")
        print("  python quick_commands.py health")
        print("  python quick_commands.py explain <topic>")
