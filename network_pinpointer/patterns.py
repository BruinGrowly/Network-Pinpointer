#!/usr/bin/env python3
"""
Pattern Library - Common network issue patterns and signatures

A library of known network problems with their LJPW signatures,
causes, and recommended fixes.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
from .semantic_engine import Coordinates
from .cli_output import get_formatter


@dataclass
class NetworkPattern:
    """A recognized network problem pattern"""
    name: str
    signature: str  # What it looks like
    ljpw_signature: Dict[str, str]  # Expected LJPW values
    causes: List[str]
    symptoms: List[str]
    fixes: List[str]
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW


class PatternLibrary:
    """Library of known network patterns"""

    def __init__(self):
        self.patterns = self._build_patterns()
        self.fmt = get_formatter()

    def _build_patterns(self) -> List[NetworkPattern]:
        """Build library of known patterns"""
        return [
            # Pattern 1: The Over-Secured Network
            NetworkPattern(
                name="The Over-Secured Network",
                signature="High Justice (>0.7), Low Love (<0.4)",
                ljpw_signature={
                    "love": "< 0.4 (LOW)",
                    "justice": "> 0.7 (HIGH)",
                    "power": "any",
                    "wisdom": "any"
                },
                causes=[
                    "Overly restrictive firewall rules",
                    "Too many ACLs blocking legitimate traffic",
                    "Security policies implemented without testing impact",
                    "Default-deny rules catching needed services"
                ],
                symptoms=[
                    "Can't connect to services that should be accessible",
                    "Intermittent connectivity to internal resources",
                    "Applications timing out",
                    "Users complaining about blocked access"
                ],
                fixes=[
                    "Audit firewall rules - remove overly broad denies",
                    "Test security policies before production deployment",
                    "Implement whitelist for known-good traffic",
                    "Review ACLs for unintended blocking",
                    "Balance security with usability"
                ],
                severity="HIGH"
            ),

            # Pattern 2: The Long Haul
            NetworkPattern(
                name="The Long Haul",
                signature="Low Power (<0.4), Low TTL (<40 in responses)",
                ljpw_signature={
                    "love": "moderate",
                    "justice": "low",
                    "power": "< 0.4 (LOW)",
                    "wisdom": "any"
                },
                causes=[
                    "Sub-optimal routing (too many hops)",
                    "Traffic going through wrong ISP",
                    "No direct peering to destination",
                    "BGP routing issues",
                    "Geographic distance + poor path selection"
                ],
                symptoms=[
                    "High latency (>100ms)",
                    "Slow application performance",
                    "Video/voice quality issues",
                    "Traceroute shows >20 hops"
                ],
                fixes=[
                    "Establish direct peering with destination",
                    "Use CDN for content delivery",
                    "Review BGP routing policies",
                    "Consider SD-WAN for path optimization",
                    "Evaluate different ISP/transit provider"
                ],
                severity="MEDIUM"
            ),

            # Pattern 3: The Flaky Link
            NetworkPattern(
                name="The Flaky Link",
                signature="Varying Wisdom, Burst loss pattern",
                ljpw_signature={
                    "love": "0.5-0.7 (unstable)",
                    "justice": "low",
                    "power": "0.4-0.7 (degraded)",
                    "wisdom": "< 0.6 (LOW)"
                },
                causes=[
                    "Physical link quality issues",
                    "Faulty network interface",
                    "Bad cable or connector",
                    "WiFi interference",
                    "Switch port errors"
                ],
                symptoms=[
                    "Random packet loss (burst pattern)",
                    "Interface errors in logs",
                    "CRC errors on network card",
                    "Performance varies widely",
                    "Connection drops randomly"
                ],
                fixes=[
                    "Check physical cables and connectors",
                    "Replace network interface card",
                    "Verify switch port health",
                    "For WiFi: check channel interference",
                    "Review interface error counters"
                ],
                severity="HIGH"
            ),

            # Pattern 4: QoS Policy in Effect
            NetworkPattern(
                name="QoS Policy in Effect",
                signature="Periodic loss, Justice elevated",
                ljpw_signature={
                    "love": "0.7-0.9 (mostly working)",
                    "justice": "0.5-0.7 (MEDIUM-HIGH)",
                    "power": "0.5-0.8 (limited)",
                    "wisdom": "0.5-0.7 (some gaps)"
                },
                causes=[
                    "Traffic shaping/rate limiting active",
                    "QoS policy prioritizing other traffic",
                    "Bandwidth cap reached",
                    "DiffServ/ToS policy enforcement",
                    "ISP traffic management"
                ],
                symptoms=[
                    "Periodic packet loss (every Nth packet)",
                    "Consistent bandwidth limitation",
                    "Some traffic prioritized over others",
                    "Time-based performance variation"
                ],
                fixes=[
                    "Review QoS policies - adjust if needed",
                    "Verify traffic is marked correctly (DSCP)",
                    "Check if rate limits are appropriate",
                    "Coordinate with ISP on traffic policies",
                    "Consider upgrading bandwidth if consistently capped"
                ],
                severity="MEDIUM"
            ),

            # Pattern 5: Route Flapping
            NetworkPattern(
                name="Route Flapping",
                signature="Justice unstable, TTL variance >2",
                ljpw_signature={
                    "love": "0.6-0.9 (working but unstable)",
                    "justice": "0.4-0.8 (VARYING)",
                    "power": "moderate",
                    "wisdom": "moderate"
                },
                causes=[
                    "BGP route instability",
                    "Intermittent link causing route changes",
                    "Routing protocol timers too aggressive",
                    "Dual-homed setup with oscillating preference",
                    "ISP routing issues"
                ],
                symptoms=[
                    "TTL varies significantly between packets",
                    "Traceroute shows different paths",
                    "Intermittent latency spikes",
                    "BGP routing logs show updates"
                ],
                fixes=[
                    "Check BGP routing table stability",
                    "Adjust routing protocol timers",
                    "Review route preferences and metrics",
                    "Dampen route flapping",
                    "Contact ISP if upstream issue"
                ],
                severity="MEDIUM"
            ),

            # Pattern 6: The DNS Black Hole
            NetworkPattern(
                name="The DNS Black Hole",
                signature="Low Wisdom for DNS, can't resolve names",
                ljpw_signature={
                    "love": "< 0.3 (very low)",
                    "justice": "any",
                    "power": "any",
                    "wisdom": "< 0.4 (LOW)"
                },
                causes=[
                    "DNS server unreachable",
                    "DNS server misconfigured",
                    "Firewall blocking UDP port 53",
                    "Wrong DNS server configured",
                    "DNS server overloaded"
                ],
                symptoms=[
                    "Can ping IPs but not hostnames",
                    "DNS queries timing out",
                    "Intermittent name resolution",
                    "Applications failing to connect"
                ],
                fixes=[
                    "Verify DNS server is reachable",
                    "Check DNS configuration (/etc/resolv.conf)",
                    "Ensure UDP port 53 is not blocked",
                    "Try alternative DNS server (8.8.8.8)",
                    "Check DNS server logs for errors"
                ],
                severity="CRITICAL"
            ),

            # Pattern 7: The Congestion Point
            NetworkPattern(
                name="The Congestion Point",
                signature="Low Power, burst loss, time-dependent",
                ljpw_signature={
                    "love": "0.5-0.8 (degraded during peaks)",
                    "justice": "low",
                    "power": "< 0.5 (LOW)",
                    "wisdom": "0.4-0.7 (gaps)"
                },
                causes=[
                    "Link bandwidth saturation",
                    "Bottleneck at network device",
                    "Too much traffic for capacity",
                    "No QoS prioritization",
                    "Peak usage overwhelming link"
                ],
                symptoms=[
                    "Burst packet loss during peak times",
                    "High latency variations",
                    "Buffer bloat",
                    "Interface shows high utilization",
                    "Performance fine off-peak"
                ],
                fixes=[
                    "Increase link bandwidth",
                    "Implement QoS to prioritize critical traffic",
                    "Add traffic shaping to smooth bursts",
                    "Upgrade congested network equipment",
                    "Distribute load across multiple links"
                ],
                severity="HIGH"
            ),

            # Pattern 8: The Asymmetric Route
            NetworkPattern(
                name="The Asymmetric Route",
                signature="Good outbound, poor inbound (or vice versa)",
                ljpw_signature={
                    "love": "0.4-0.7 (inconsistent)",
                    "justice": "moderate",
                    "power": "0.4-0.7 (degraded one way)",
                    "wisdom": "moderate"
                },
                causes=[
                    "Asymmetric routing paths",
                    "One direction going through poor path",
                    "Firewall stateful tracking issues",
                    "Different ISPs for inbound/outbound",
                    "Policy routing causing asymmetry"
                ],
                symptoms=[
                    "Good upload but poor download (or vice versa)",
                    "Traceroute shows different return path",
                    "Firewall dropping return traffic",
                    "TCP connections timing out"
                ],
                fixes=[
                    "Review routing policies for symmetry",
                    "Adjust BGP preferences for both directions",
                    "Configure stateful firewall for asymmetric routes",
                    "Use same ISP for both directions if possible",
                    "Document and accept if asymmetry is intentional"
                ],
                severity="MEDIUM"
            ),
            NetworkPattern(
                name="The MTU Mismatch",
                signature="Good small packets, large packets fail/fragment",
                ljpw_signature={
                    "love": "0.6-0.8 (works for small data)",
                    "justice": "moderate",
                    "power": "< 0.5 (LOW for large transfers)",
                    "wisdom": "0.4-0.6 (fragmentation visible)"
                },
                causes=[
                    "MTU mismatch somewhere in path",
                    "VPN/tunnel reducing effective MTU",
                    "PPPoE without MTU adjustment",
                    "Path MTU discovery blocked by firewall",
                    "Jumbo frames not supported on all segments"
                ],
                symptoms=[
                    "Small packets (ping) work fine",
                    "Large file transfers fail or are very slow",
                    "HTTP/HTTPS loads partially then hangs",
                    "SSH works but file transfers don't",
                    "Excessive packet fragmentation"
                ],
                fixes=[
                    "Run path MTU discovery manually",
                    "Reduce MTU on local interface to 1400",
                    "Enable TCP MSS clamping on routers",
                    "Fix PMTUD by allowing ICMP fragmentation needed",
                    "Configure consistent MTU across entire path"
                ],
                severity="HIGH"
            ),
            NetworkPattern(
                name="The NAT Exhaustion",
                signature="Intermittent failures, high Justice, connection limits",
                ljpw_signature={
                    "love": "0.3-0.7 (intermittent)",
                    "justice": "0.7-0.9 (HIGH - NAT is policy enforcement)",
                    "power": "0.5-0.7 (degraded)",
                    "wisdom": "0.4-0.6 (some connections invisible)"
                },
                causes=[
                    "NAT port pool exhausted",
                    "Too many connections for available ports",
                    "NAT timeout too long (ports not freed)",
                    "Connection tracking table full",
                    "Many clients behind single NAT IP"
                ],
                symptoms=[
                    "New connections fail while existing work",
                    "Works fine then suddenly fails",
                    "Restarting app temporarily fixes it",
                    "Peak hours have connection failures",
                    "Error logs show 'no route to host' intermittently"
                ],
                fixes=[
                    "Increase NAT port pool size",
                    "Reduce NAT timeout values",
                    "Add more public IPs for NAT pool",
                    "Implement connection limits per client",
                    "Use NAT64/DS-Lite for better scaling"
                ],
                severity="HIGH"
            ),
            NetworkPattern(
                name="The Microservice Cascade Failure",
                signature="Increasing Justice, decreasing Love/Power, timeouts",
                ljpw_signature={
                    "love": "< 0.4 (LOW - services unreachable)",
                    "justice": "0.6-0.9 (circuit breakers triggering)",
                    "power": "0.3-0.6 (degraded)",
                    "wisdom": "0.5-0.8 (lots of error metadata)"
                },
                causes=[
                    "One service failing causing cascade",
                    "Circuit breakers opening everywhere",
                    "Retry storms amplifying problem",
                    "No backpressure/rate limiting",
                    "Dependency chain too long"
                ],
                symptoms=[
                    "One service down takes others with it",
                    "Timeout errors multiplying",
                    "Circuit breakers in OPEN state",
                    "Request queues backing up",
                    "Exponential increase in failed requests"
                ],
                fixes=[
                    "Implement proper circuit breakers",
                    "Add bulkheads to isolate failures",
                    "Use exponential backoff with jitter",
                    "Set appropriate timeouts at each level",
                    "Add backpressure and rate limiting"
                ],
                severity="CRITICAL"
            ),
            NetworkPattern(
                name="The Cloud Egress Surprise",
                signature="High Justice blocking outbound, unexpected restrictions",
                ljpw_signature={
                    "love": "0.2-0.5 (can't reach external)",
                    "justice": "0.7-0.9 (HIGH - security groups)",
                    "power": "moderate",
                    "wisdom": "0.3-0.6 (unclear what's blocked)"
                },
                causes=[
                    "Default-deny security group egress rules",
                    "Network ACLs blocking outbound traffic",
                    "VPC routing table missing IGW route",
                    "NAT gateway not configured",
                    "Service endpoints blocking public internet"
                ],
                symptoms=[
                    "Can't reach internet from cloud instances",
                    "Internal cloud services work fine",
                    "API calls to external services timeout",
                    "Package installations fail",
                    "Outbound connections silently dropped"
                ],
                fixes=[
                    "Review and update security group egress rules",
                    "Check VPC route tables for 0.0.0.0/0 route",
                    "Verify NAT gateway is configured and healthy",
                    "Update network ACLs to allow outbound",
                    "Use VPC endpoints for AWS services"
                ],
                severity="HIGH"
            ),
            NetworkPattern(
                name="The IPv4/IPv6 Split Brain",
                signature="Works on IPv4, fails on IPv6 (or vice versa)",
                ljpw_signature={
                    "love": "0.4-0.9 (depends on protocol used)",
                    "justice": "moderate",
                    "power": "moderate",
                    "wisdom": "0.3-0.6 (dual-stack confusion)"
                },
                causes=[
                    "IPv6 configured but not routed properly",
                    "Firewall rules only for IPv4",
                    "DNS returning both A and AAAA but only one works",
                    "Application preferring IPv6 which doesn't work",
                    "Partial IPv6 deployment"
                ],
                symptoms=[
                    "Service works sometimes but not others",
                    "Works when forcing IPv4, fails on auto",
                    "Different behavior from different clients",
                    "Long connection timeouts before fallback",
                    "Ping works but application doesn't"
                ],
                fixes=[
                    "Disable IPv6 if not fully deployed",
                    "Implement IPv6 firewall rules matching IPv4",
                    "Configure proper IPv6 routing",
                    "Remove AAAA DNS records if IPv6 not working",
                    "Set application to prefer working protocol"
                ],
                severity="MEDIUM"
            ),
            NetworkPattern(
                name="The Container Network Overlay Blues",
                signature="Pod-to-pod works, external access fails",
                ljpw_signature={
                    "love": "0.3-0.6 (partial connectivity)",
                    "justice": "0.6-0.8 (network policies)",
                    "power": "0.5-0.7 (overlay overhead)",
                    "wisdom": "0.4-0.7 (complex networking)"
                },
                causes=[
                    "CNI plugin misconfigured",
                    "Network policies blocking traffic",
                    "Service mesh sidecar injection issues",
                    "NodePort/LoadBalancer misconfiguration",
                    "Overlay network MTU problems"
                ],
                symptoms=[
                    "Pods can talk to each other",
                    "Can't reach services from outside cluster",
                    "Ingress not working",
                    "External DNS not resolving",
                    "Inter-node pod communication fails"
                ],
                fixes=[
                    "Verify CNI plugin installation",
                    "Review and update network policies",
                    "Check service type (ClusterIP vs LoadBalancer)",
                    "Validate ingress controller configuration",
                    "Reduce MTU for overlay networks"
                ],
                severity="HIGH"
            ),
            NetworkPattern(
                name="The Wireless Interference Storm",
                signature="WiFi-specific, periodic degradation, varying Power/Love",
                ljpw_signature={
                    "love": "0.3-0.8 (highly variable)",
                    "justice": "low",
                    "power": "0.2-0.7 (VARYING widely)",
                    "wisdom": "0.3-0.6 (signal quality issues)"
                },
                causes=[
                    "Channel congestion from neighbors",
                    "Microwave/Bluetooth interference",
                    "Too many clients on one AP",
                    "2.4GHz interference from other devices",
                    "Physical obstacles/metal interference"
                ],
                symptoms=[
                    "Wired connections work fine",
                    "WiFi performance varies by location",
                    "Periodic slowdowns or dropouts",
                    "Better performance early morning/late night",
                    "Connection drops when microwave runs"
                ],
                fixes=[
                    "Switch to less congested WiFi channel",
                    "Use 5GHz instead of 2.4GHz",
                    "Add more access points for better coverage",
                    "Enable band steering",
                    "Relocate AP away from interference sources"
                ],
                severity="MEDIUM"
            ),
            NetworkPattern(
                name="The TCP Window Scaling Fail",
                signature="Good latency, poor throughput, high BDP links",
                ljpw_signature={
                    "love": "0.7-0.9 (good latency)",
                    "justice": "moderate",
                    "power": "< 0.4 (LOW throughput)",
                    "wisdom": "0.4-0.6 (TCP metadata shows issues)"
                },
                causes=[
                    "TCP window scaling disabled",
                    "Window size too small for BDP",
                    "Firewall mangling TCP options",
                    "Old OS without window scaling support",
                    "Bandwidth-delay product mismatch"
                ],
                symptoms=[
                    "Ping shows low latency",
                    "Downloads much slower than expected",
                    "Works fine on LAN, slow over WAN",
                    "Single stream slow, multiple streams better",
                    "Never exceeds certain throughput ceiling"
                ],
                fixes=[
                    "Enable TCP window scaling in OS",
                    "Increase TCP window size parameters",
                    "Update firewall to not mangle TCP options",
                    "Use TCP BBR congestion control",
                    "Implement TCP tuning for high BDP links"
                ],
                severity="MEDIUM"
            )
        ]

    def match_pattern(self, coords: Coordinates, metadata: Optional[Dict] = None) -> List[NetworkPattern]:
        """
        Find matching patterns for given coordinates

        Returns list of matching patterns, sorted by relevance
        """
        matches = []

        for pattern in self.patterns:
            if self._matches_signature(coords, pattern, metadata):
                matches.append(pattern)

        return matches

    def _matches_signature(
        self,
        coords: Coordinates,
        pattern: NetworkPattern,
        metadata: Optional[Dict]
    ) -> bool:
        """Check if coordinates match pattern signature"""

        sig = pattern.ljpw_signature

        # Check Love
        if "love" in sig:
            if "< 0.4" in sig["love"] and coords.love >= 0.4:
                return False
            if "> 0.7" in sig["love"] and coords.love <= 0.7:
                return False
            if "0.5-0.7" in sig["love"] and not (0.5 <= coords.love <= 0.7):
                return False

        # Check Justice
        if "justice" in sig:
            if "< 0.4" in sig["justice"] and coords.justice >= 0.4:
                return False
            if "> 0.7" in sig["justice"] and coords.justice <= 0.7:
                return False
            if "0.4-0.8" in sig["justice"] and not (0.4 <= coords.justice <= 0.8):
                return False

        # Check Power
        if "power" in sig:
            if "< 0.4" in sig["power"] and coords.power >= 0.4:
                return False
            if "< 0.5" in sig["power"] and coords.power >= 0.5:
                return False
            if "0.4-0.7" in sig["power"] and not (0.4 <= coords.power <= 0.7):
                return False

        # Check Wisdom
        if "wisdom" in sig:
            if "< 0.4" in sig["wisdom"] and coords.wisdom >= 0.4:
                return False
            if "< 0.6" in sig["wisdom"] and coords.wisdom >= 0.6:
                return False

        return True

    def display_pattern(self, pattern: NetworkPattern) -> str:
        """Display a single pattern"""
        lines = []

        lines.append(self.fmt.bold(f"📌 Pattern: {pattern.name}"))
        lines.append(f"   Severity: {self.fmt.priority_indicator(pattern.severity)}")
        lines.append(f"\n   {self.fmt.bold('Signature:')}")
        lines.append(f"   {pattern.signature}")

        lines.append(f"\n   {self.fmt.bold('LJPW Pattern:')}")
        for dim, sig in pattern.ljpw_signature.items():
            lines.append(f"     {dim.capitalize():8} {sig}")

        lines.append(f"\n   {self.fmt.bold('Likely Causes:')}")
        for cause in pattern.causes[:3]:  # Show top 3
            lines.append(f"     • {cause}")

        lines.append(f"\n   {self.fmt.bold('How to Fix:')}")
        for fix in pattern.fixes[:3]:  # Show top 3
            lines.append(f"     • {fix}")

        return "\n".join(lines)

    def display_all_patterns(self) -> str:
        """Display all patterns in library"""
        lines = []

        lines.append(self.fmt.section_header("Network Pattern Library"))
        lines.append(f"\n{len(self.patterns)} known patterns:\n")

        for i, pattern in enumerate(self.patterns, 1):
            lines.append(f"{i}. {self.fmt.bold(pattern.name)}")
            lines.append(f"   {pattern.signature}")
            lines.append(f"   Severity: {pattern.severity}")
            lines.append("")

        return "\n".join(lines)


if __name__ == "__main__":
    # Demo pattern library
    from .semantic_engine import Coordinates

    library = PatternLibrary()

    # Show all patterns
    print(library.display_all_patterns())

    print("\n" + "=" * 70)
    print("Pattern Matching Example")
    print("=" * 70)

    # Test pattern matching
    coords = Coordinates(love=0.35, justice=0.75, power=0.55, wisdom=0.60)
    print(f"\nTesting coordinates: L={coords.love:.2f}, J={coords.justice:.2f}, "
          f"P={coords.power:.2f}, W={coords.wisdom:.2f}\n")

    matches = library.match_pattern(coords)

    if matches:
        print(f"Found {len(matches)} matching pattern(s):\n")
        for match in matches:
            print(library.display_pattern(match))
            print("\n" + "=" * 70 + "\n")
    else:
        print("No matching patterns found.")
