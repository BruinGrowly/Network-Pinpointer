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
