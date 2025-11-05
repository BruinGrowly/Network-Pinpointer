#!/usr/bin/env python3
"""
Semantic Interpreter: Translates Tool Output → LJPW Context

Maps raw network tool results to semantic coordinates and generates
meaningful context about what the results MEAN.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
from .semantic_engine import Coordinates, NetworkSemanticEngine


@dataclass
class SemanticInterpretation:
    """Semantic interpretation of tool output"""

    coordinates: Coordinates
    context: str  # What does it mean?
    diagnosis: str  # What's the issue?
    confidence: float  # 0-1
    recommendations: List[str]


class SemanticToolInterpreter:
    """Interprets traditional network tools through LJPW lens"""

    def __init__(self, engine: NetworkSemanticEngine):
        self.engine = engine

    def interpret_ping(
        self,
        host: str,
        packets_sent: int,
        packets_received: int,
        avg_latency: float,
        packet_loss: float,
    ) -> SemanticInterpretation:
        """
        Interpret ping results semantically

        Ping measures connectivity (Love) and performance (Power)
        """
        # Calculate semantic coordinates
        love = 1.0 - (packet_loss / 100.0)  # Connectivity strength
        power = max(0, 1.0 - (avg_latency / 500.0))  # Performance (500ms = bad)
        wisdom = 0.9 if packets_received > 0 else 0.1  # Visibility
        justice = 0.2  # Minimal - just following protocol

        coords = Coordinates(love, justice, power, wisdom)

        # Generate context based on semantic pattern
        if love < 0.3:
            context = "CRITICAL: Severe connectivity failure"
            diagnosis = f"Less than {love*100:.0f}% of packets reaching {host}"
            recommendations = [
                "Check physical connection",
                "Verify routing tables",
                "Check for network congestion",
                "Verify target host is up",
            ]
            confidence = 0.9

        elif love < 0.7:
            context = "WARNING: Degraded connectivity"
            diagnosis = f"{packet_loss:.0f}% packet loss to {host}"
            recommendations = [
                "Check for intermittent link issues",
                "Monitor for network congestion",
                "Consider redundant paths",
            ]
            confidence = 0.8

        elif power < 0.3:
            context = "WARNING: Severe performance degradation"
            diagnosis = f"High latency ({avg_latency:.0f}ms) to {host}"
            recommendations = [
                "Check bandwidth utilization",
                "Look for congestion points in path",
                "Consider QoS configuration",
            ]
            confidence = 0.8

        elif power < 0.7:
            context = "NOTICE: Moderate performance issues"
            diagnosis = f"Elevated latency ({avg_latency:.0f}ms)"
            recommendations = [
                "Monitor latency trends",
                "Check for bandwidth constraints",
            ]
            confidence = 0.7

        else:
            context = "HEALTHY: Good connectivity and performance"
            diagnosis = f"Connection to {host} is optimal"
            recommendations = []
            confidence = 0.95

        return SemanticInterpretation(
            coordinates=coords,
            context=context,
            diagnosis=diagnosis,
            confidence=confidence,
            recommendations=recommendations,
        )

    def interpret_traceroute(
        self, target: str, hops: List[Dict], success: bool
    ) -> SemanticInterpretation:
        """
        Interpret traceroute results semantically

        Traceroute reveals path structure (Love) and bottlenecks (Power)
        """
        if not hops:
            # No hops - complete failure
            coords = Coordinates(0.0, 0.5, 0.0, 0.1)
            return SemanticInterpretation(
                coordinates=coords,
                context="CRITICAL: Cannot trace route - complete connectivity failure",
                diagnosis=f"Unable to reach {target} or any intermediate hops",
                confidence=0.95,
                recommendations=[
                    "Check local network connection",
                    "Verify target host exists",
                    "Check DNS resolution",
                ],
            )

        # Analyze hop pattern
        total_hops = len(hops)
        timeouts = sum(1 for h in hops if h.get("timeout", False))
        max_latency = max((h.get("latency", 0) for h in hops), default=0)
        avg_latency = (
            sum(h.get("latency", 0) for h in hops) / total_hops if total_hops else 0
        )

        # Calculate semantic coordinates
        if timeouts > total_hops * 0.3:  # > 30% timeouts
            # Many timeouts = Justice blocking visibility
            love = 0.4  # Partial connectivity
            justice = 0.7  # High - likely firewalls blocking ICMP
            power = 0.3  # Unknown performance (can't see)
            wisdom = 0.3  # Limited visibility

            context = "WARNING: Path partially obscured by firewalls"
            diagnosis = f"{timeouts}/{total_hops} hops not responding (likely ICMP filtering)"
            recommendations = [
                "Try TCP-based traceroute (-T flag)",
                "Some routers block ICMP - this is normal",
                "Contact network admin if destination unreachable",
            ]
            confidence = 0.75

        elif max_latency > 200:
            # High latency = Power issue
            bottleneck_hop = max((h for h in hops), key=lambda x: x.get("latency", 0))

            love = 0.7  # Path exists
            justice = 0.3  # Normal routing
            power = 0.2  # Performance problem
            wisdom = 0.8  # Can see the issue

            context = f"WARNING: Performance bottleneck at hop {bottleneck_hop.get('hop_number', '?')}"
            diagnosis = f"Severe latency spike ({max_latency:.0f}ms) at {bottleneck_hop.get('host', 'unknown')}"
            recommendations = [
                f"Investigate hop {bottleneck_hop.get('hop_number', '?')} for congestion",
                "Check bandwidth at bottleneck",
                "Consider alternate routing",
            ]
            confidence = 0.85

        else:
            # Healthy path
            love = 0.9  # Good connectivity
            justice = 0.3  # Normal routing
            power = 0.8  # Good performance
            wisdom = 0.9  # Full visibility

            context = "HEALTHY: Clean path with good performance"
            diagnosis = f"Route to {target} is optimal ({total_hops} hops, {avg_latency:.0f}ms total)"
            recommendations = []
            confidence = 0.9

        coords = Coordinates(love, justice, power, wisdom)

        return SemanticInterpretation(
            coordinates=coords,
            context=context,
            diagnosis=diagnosis,
            confidence=confidence,
            recommendations=recommendations,
        )

    def interpret_port_scan(
        self, host: str, port: int, state: str, response_time: float
    ) -> SemanticInterpretation:
        """
        Interpret port scan results semantically

        Port state reveals service availability (Love) and policy (Justice)
        """
        if state == "open":
            # Port open - service available
            love = 0.8  # Service accessible
            justice = 0.2  # Minimal filtering
            power = 0.7 if response_time < 100 else 0.4  # Performance
            wisdom = 0.8  # Clear signal

            context = f"OPEN: Service available on port {port}"
            diagnosis = f"Service responding on {host}:{port}"
            recommendations = []
            confidence = 0.95

        elif state == "closed":
            # Port closed - active rejection (RST)
            love = 0.1  # No service connection
            justice = 0.3  # Some policy (service not running)
            power = 0.5  # Active rejection (not passive)
            wisdom = 0.8  # Clear signal (RST received)

            context = f"CLOSED: Port {port} actively rejecting connections"
            diagnosis = "Service not running or explicitly denying access"
            recommendations = [
                "Verify service is started",
                "Check service configuration",
                "Confirm correct port number",
            ]
            confidence = 0.9

        elif state == "filtered" or state == "timeout":
            # Timeout - silent drop (firewall)
            love = 0.0  # No connection
            justice = 0.8  # High - likely firewall/ACL
            power = 0.1  # Passive blocking
            wisdom = 0.2  # No information (blind)

            context = f"FILTERED: Port {port} silently blocked by firewall"
            diagnosis = "Firewall/ACL dropping packets (no response received)"
            recommendations = [
                "Check firewall rules",
                "Verify ACL configuration",
                "Contact network admin for access",
            ]
            confidence = 0.85

        else:
            # Unknown state
            coords = Coordinates(0.0, 0.0, 0.0, 0.0)
            return SemanticInterpretation(
                coordinates=coords,
                context=f"UNKNOWN: Cannot determine port {port} state",
                diagnosis="Unexpected response from target",
                confidence=0.3,
                recommendations=["Try alternate scanning methods"],
            )

        coords = Coordinates(love, justice, power, wisdom)

        return SemanticInterpretation(
            coordinates=coords,
            context=context,
            diagnosis=diagnosis,
            confidence=confidence,
            recommendations=recommendations,
        )

    def correlate_multi_tool(
        self, interpretations: List[SemanticInterpretation]
    ) -> SemanticInterpretation:
        """
        Correlate multiple tool results to build holistic context

        Example: Ping success + Port timeout = Application-level issue
        """
        if not interpretations:
            return SemanticInterpretation(
                coordinates=Coordinates(0, 0, 0, 0),
                context="No data to correlate",
                diagnosis="No diagnostic results available",
                confidence=0.0,
                recommendations=[],
            )

        # Average coordinates across all tools
        avg_l = sum(i.coordinates.love for i in interpretations) / len(interpretations)
        avg_j = sum(i.coordinates.justice for i in interpretations) / len(
            interpretations
        )
        avg_p = sum(i.coordinates.power for i in interpretations) / len(
            interpretations
        )
        avg_w = sum(i.coordinates.wisdom for i in interpretations) / len(
            interpretations
        )

        coords = Coordinates(avg_l, avg_j, avg_p, avg_w)

        # Detect layer-specific issues
        # If ping good but port bad = application layer issue
        ping_ok = any(
            "ping" in i.diagnosis.lower() and i.coordinates.love > 0.7
            for i in interpretations
        )
        port_bad = any(
            "port" in i.diagnosis.lower() and i.coordinates.love < 0.3
            for i in interpretations
        )

        if ping_ok and port_bad:
            context = "Application-layer issue (network is healthy)"
            diagnosis = "Host is reachable but service not responding"
            recommendations = [
                "Check if service is running",
                "Review application logs",
                "Verify service configuration",
                "Check downstream dependencies (database, etc.)",
            ]
            confidence = 0.9

        elif not ping_ok:
            context = "Network-layer issue (connectivity problem)"
            diagnosis = "Host unreachable at network level"
            recommendations = [
                "Check physical network connection",
                "Verify routing configuration",
                "Check for network outages",
            ]
            confidence = 0.85

        elif avg_j > 0.6:
            context = "Security/policy blocking access"
            diagnosis = "High Justice dimension indicates firewall/ACL blocking"
            recommendations = [
                "Review firewall rules",
                "Check ACL configuration",
                "Verify security policies",
            ]
            confidence = 0.8

        elif avg_p < 0.4:
            context = "Performance degradation"
            diagnosis = "Low Power dimension indicates bandwidth/latency issues"
            recommendations = [
                "Check bandwidth utilization",
                "Identify congestion points",
                "Consider QoS/traffic shaping",
            ]
            confidence = 0.75

        else:
            context = "Mixed results - unclear pattern"
            diagnosis = "Multiple issues detected, requires deeper analysis"
            recommendations = ["Run additional diagnostics", "Check system logs"]
            confidence = 0.5

        return SemanticInterpretation(
            coordinates=coords,
            context=context,
            diagnosis=diagnosis,
            confidence=confidence,
            recommendations=recommendations,
        )


# Example usage patterns
SEMANTIC_PATTERNS = {
    "connection_refused": {
        "signature": {"love": 0.1, "justice": 0.3, "power": 0.5, "wisdom": 0.8},
        "meaning": "Active rejection - service not available",
        "not_cause": "Not a firewall (would be silent)",
    },
    "firewall_block": {
        "signature": {"love": 0.0, "justice": 0.8, "power": 0.1, "wisdom": 0.2},
        "meaning": "Silent policy enforcement - firewall/ACL",
        "not_cause": "Not a service issue (would send RST)",
    },
    "congestion": {
        "signature": {"love": 0.6, "justice": 0.2, "power": 0.2, "wisdom": 0.7},
        "meaning": "Performance bottleneck - bandwidth constraint",
        "not_cause": "Not blocking (Love dimension positive)",
    },
    "healthy": {
        "signature": {"love": 0.9, "justice": 0.3, "power": 0.9, "wisdom": 0.9},
        "meaning": "Optimal state - all dimensions healthy",
        "not_cause": None,
    },
}
