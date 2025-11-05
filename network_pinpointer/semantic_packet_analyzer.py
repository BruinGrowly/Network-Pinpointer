#!/usr/bin/env python3
"""
Semantic Packet Analyzer: Map Real Packet Metadata → LJPW Coordinates

Takes captured packet metadata and performs deep semantic analysis
to extract meaning and context.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from .semantic_engine import Coordinates, NetworkSemanticEngine
from .metadata_extractor import (
    MetadataExtractor,
    TTLSemantics,
    SequenceSemantics,
    TimingSemantics
)
from .real_packet_capture import ICMPMetadata, TCPMetadata, DNSMetadata


@dataclass
class SemanticPacketAnalysis:
    """Complete semantic analysis of packet(s)"""

    coordinates: Coordinates
    context: str
    patterns_detected: List[str]
    insights: List[str]
    health_assessment: str
    confidence: float


class SemanticPacketAnalyzer:
    """Analyzes real packet metadata and extracts semantic meaning"""

    def __init__(self):
        self.engine = NetworkSemanticEngine()
        self.metadata_extractor = MetadataExtractor()

    def analyze_icmp_packets(
        self,
        packets: List[ICMPMetadata]
    ) -> SemanticPacketAnalysis:
        """
        Analyze a series of ICMP packets semantically

        Extracts patterns from TTL, sequences, timing
        """
        if not packets:
            return SemanticPacketAnalysis(
                coordinates=Coordinates(0, 0, 0, 0),
                context="No packets to analyze",
                patterns_detected=[],
                insights=[],
                health_assessment="UNKNOWN",
                confidence=0.0
            )

        # Extract metadata patterns
        ttl_values = [p.ttl for p in packets]
        sequences = [p.sequence for p in packets if p.sequence is not None]

        # Get semantic analysis from metadata
        ttl_sem = self.metadata_extractor.extract_ttl_semantics(ttl_values)
        seq_sem = self.metadata_extractor.extract_sequence_semantics(
            list(range(len(sequences))),
            sequences
        )

        # Build LJPW coordinates from metadata
        coords = self._icmp_metadata_to_coordinates(
            packets, ttl_sem, seq_sem
        )

        # Detect patterns
        patterns = self._detect_icmp_patterns(packets, ttl_sem, seq_sem)

        # Generate insights
        insights = self._generate_icmp_insights(
            packets, ttl_sem, seq_sem, coords
        )

        # Health assessment
        health = self._assess_health(coords)

        # Context description
        context = self._describe_icmp_context(coords, ttl_sem, seq_sem)

        return SemanticPacketAnalysis(
            coordinates=coords,
            context=context,
            patterns_detected=patterns,
            insights=insights,
            health_assessment=health,
            confidence=0.9
        )

    def analyze_tcp_packets(
        self,
        packets: List[TCPMetadata]
    ) -> SemanticPacketAnalysis:
        """
        Analyze TCP packets semantically

        Focuses on flags, window sizes, sequences
        """
        if not packets:
            return SemanticPacketAnalysis(
                coordinates=Coordinates(0, 0, 0, 0),
                context="No packets to analyze",
                patterns_detected=[],
                insights=[],
                health_assessment="UNKNOWN",
                confidence=0.0
            )

        # Analyze TCP flags to determine semantic meaning
        coords = self._tcp_metadata_to_coordinates(packets)

        # Detect patterns
        patterns = self._detect_tcp_patterns(packets)

        # Generate insights
        insights = self._generate_tcp_insights(packets, coords)

        # Health assessment
        health = self._assess_health(coords)

        # Context
        context = self._describe_tcp_context(packets, coords)

        return SemanticPacketAnalysis(
            coordinates=coords,
            context=context,
            patterns_detected=patterns,
            insights=insights,
            health_assessment=health,
            confidence=0.85
        )

    def analyze_dns_packets(
        self,
        packets: List[DNSMetadata]
    ) -> SemanticPacketAnalysis:
        """
        Analyze DNS packets semantically

        Focuses on resolution success, TTLs, answer patterns
        """
        if not packets:
            return SemanticPacketAnalysis(
                coordinates=Coordinates(0, 0, 0, 0),
                context="No packets to analyze",
                patterns_detected=[],
                insights=[],
                health_assessment="UNKNOWN",
                confidence=0.0
            )

        coords = self._dns_metadata_to_coordinates(packets)
        patterns = self._detect_dns_patterns(packets)
        insights = self._generate_dns_insights(packets, coords)
        health = self._assess_health(coords)
        context = self._describe_dns_context(packets, coords)

        return SemanticPacketAnalysis(
            coordinates=coords,
            context=context,
            patterns_detected=patterns,
            insights=insights,
            health_assessment=health,
            confidence=0.8
        )

    # ICMP Analysis Methods

    def _icmp_metadata_to_coordinates(
        self,
        packets: List[ICMPMetadata],
        ttl_sem: TTLSemantics,
        seq_sem: SequenceSemantics
    ) -> Coordinates:
        """Map ICMP metadata to LJPW coordinates"""

        # Love: Connectivity strength (based on packet reception)
        # Assume all packets received since they're in our list
        love = 0.9  # High - we're getting responses

        # Justice: Path policy enforcement (TTL patterns)
        # Stable TTL = low policy variance
        # Unstable TTL = routes changing (policy adjustments)
        if ttl_sem.path_stability > 0.8:
            justice = 0.2  # Low - consistent routing
        elif ttl_sem.path_stability > 0.5:
            justice = 0.4  # Medium - some routing changes
        else:  # unstable
            justice = 0.6  # High - active route changes/policy

        # Power: Performance (path complexity, latency would go here)
        # Simple path = high power, complex path = lower power
        if ttl_sem.path_complexity == "simple":
            power = 0.9
        elif ttl_sem.path_complexity == "normal":
            power = 0.7
        elif ttl_sem.path_complexity == "complex":
            power = 0.5
        else:  # extreme
            power = 0.3

        # Wisdom: Visibility and information quality
        # Can we see clearly what's happening?
        if seq_sem.loss_pattern == "none":
            wisdom = 0.95  # Perfect visibility
        elif seq_sem.loss_pattern in ["burst", "periodic"]:
            wisdom = 0.6  # Some blind spots
        else:  # random
            wisdom = 0.4  # Poor visibility

        return Coordinates(love, justice, power, wisdom)

    def _detect_icmp_patterns(
        self,
        packets: List[ICMPMetadata],
        ttl_sem: TTLSemantics,
        seq_sem: SequenceSemantics
    ) -> List[str]:
        """Detect semantic patterns in ICMP packets"""
        patterns = []

        # TTL patterns
        if ttl_sem.route_changing:
            patterns.append(f"Route instability detected (TTL variance: {ttl_sem.hop_variance:.2f})")

        if ttl_sem.path_complexity in ["complex", "extreme"]:
            patterns.append(f"Complex path ({ttl_sem.avg_hops} hops)")

        # Sequence patterns
        if seq_sem.loss_pattern == "periodic":
            patterns.append("Periodic packet loss detected (QoS policy?)")
        elif seq_sem.loss_pattern == "burst":
            patterns.append("Burst packet loss detected (congestion?)")
        elif seq_sem.loss_rate > 0.5:
            patterns.append("Heavy packet loss detected (critical issue)")

        # Type patterns
        type_counts = {}
        for p in packets:
            type_counts[p.type] = type_counts.get(p.type, 0) + 1

        if 0 in type_counts:  # Echo reply
            patterns.append(f"Normal ping responses ({type_counts[0]} replies)")
        if 3 in type_counts:  # Destination unreachable
            patterns.append(f"Destination unreachable detected ({type_counts[3]} packets)")
        if 11 in type_counts:  # Time exceeded
            patterns.append(f"TTL exceeded detected ({type_counts[11]} packets)")

        return patterns

    def _generate_icmp_insights(
        self,
        packets: List[ICMPMetadata],
        ttl_sem: TTLSemantics,
        seq_sem: SequenceSemantics,
        coords: Coordinates
    ) -> List[str]:
        """Generate semantic insights from ICMP metadata"""
        insights = []

        # Path stability insights
        if ttl_sem.route_changing:
            insights.append(
                f"Path is changing (stability: {ttl_sem.path_stability:.2f}). "
                "Network may be experiencing routing updates or failovers."
            )

        # Performance insights
        if ttl_sem.path_complexity == "extreme":
            insights.append(
                "Extremely long path detected. This indicates sub-optimal routing "
                "or possible routing loops."
            )

        # Loss pattern insights
        if seq_sem.loss_pattern == "periodic":
            insights.append(
                "Periodic loss suggests QoS policy or traffic shaping. "
                "This is Justice dimension enforcement (intentional limiting)."
            )
        elif seq_sem.loss_pattern == "burst":
            insights.append(
                "Burst loss suggests congestion events. "
                "This is Power dimension deficit (capacity issue)."
            )

        # Semantic dimension insights
        if coords.love < 0.5:
            insights.append(
                "Love dimension low: Connectivity is compromised. "
                "Check for link failures or excessive filtering."
            )

        if coords.power < 0.5:
            insights.append(
                "Power dimension low: Performance is degraded. "
                "Path complexity or congestion affecting throughput."
            )

        if coords.justice > 0.6:
            insights.append(
                "Justice dimension high: Active policy enforcement or routing changes. "
                "Network is being actively managed/controlled."
            )

        return insights

    def _describe_icmp_context(
        self,
        coords: Coordinates,
        ttl_sem: TTLSemantics,
        seq_sem: SequenceSemantics
    ) -> str:
        """Describe the overall context of ICMP communication"""

        stability_desc = "stable" if ttl_sem.path_stability > 0.8 else "unstable"

        # Determine dominant issue
        if coords.love < 0.5:
            return f"CONNECTIVITY ISSUE: Path {stability_desc}, {seq_sem.loss_pattern} loss pattern"
        elif coords.power < 0.5:
            return f"PERFORMANCE ISSUE: {ttl_sem.path_complexity} path, limited capacity"
        elif coords.justice > 0.6:
            return f"POLICY ENFORCEMENT: Active routing changes, {stability_desc} path"
        else:
            return f"HEALTHY: {stability_desc} path, {seq_sem.loss_pattern} reception"

    # TCP Analysis Methods

    def _tcp_metadata_to_coordinates(
        self,
        packets: List[TCPMetadata]
    ) -> Coordinates:
        """Map TCP metadata to LJPW coordinates"""

        # Analyze flag distribution
        flag_counts = {}
        for p in packets:
            for flag in p.flags.split('|'):
                flag_counts[flag] = flag_counts.get(flag, 0) + 1

        total_packets = len(packets)

        # Love: Connection establishment success
        syn_count = flag_counts.get('SYN', 0)
        ack_count = flag_counts.get('ACK', 0)
        if syn_count > 0 and ack_count > 0:
            love = 0.8  # Connections being established
        elif ack_count > 0:
            love = 0.9  # Active connections
        else:
            love = 0.3  # Few acknowledgments

        # Justice: Rejection and policy enforcement
        rst_count = flag_counts.get('RST', 0)
        fin_count = flag_counts.get('FIN', 0)
        if rst_count > total_packets * 0.3:
            justice = 0.8  # High rejection rate
        elif rst_count > 0:
            justice = 0.5  # Some rejections
        else:
            justice = 0.2  # Normal operation

        # Power: Active data transfer
        psh_count = flag_counts.get('PSH', 0)
        if psh_count > total_packets * 0.5:
            power = 0.9  # Lots of data moving
        elif psh_count > 0:
            power = 0.6  # Some data transfer
        else:
            power = 0.3  # Control packets only

        # Wisdom: Information visibility
        # We can see the packets, so high wisdom
        wisdom = 0.85

        return Coordinates(love, justice, power, wisdom)

    def _detect_tcp_patterns(self, packets: List[TCPMetadata]) -> List[str]:
        """Detect TCP-specific patterns"""
        patterns = []

        # Analyze connection patterns
        syn_packets = [p for p in packets if 'SYN' in p.flags]
        rst_packets = [p for p in packets if 'RST' in p.flags]
        fin_packets = [p for p in packets if 'FIN' in p.flags]

        if syn_packets:
            patterns.append(f"Connection attempts detected ({len(syn_packets)} SYN packets)")

        if rst_packets:
            patterns.append(f"Connection resets detected ({len(rst_packets)} RST packets)")
            if len(rst_packets) > len(packets) * 0.3:
                patterns.append("HIGH RST RATE: Possible port scan or service unavailable")

        if fin_packets:
            patterns.append(f"Clean connection terminations ({len(fin_packets)} FIN packets)")

        # Window size patterns
        window_sizes = [p.window_size for p in packets]
        if window_sizes:
            avg_window = sum(window_sizes) / len(window_sizes)
            if avg_window < 5000:
                patterns.append("Small window sizes (potential flow control)")
            elif avg_window > 60000:
                patterns.append("Large window sizes (high-performance transfer)")

        return patterns

    def _generate_tcp_insights(
        self,
        packets: List[TCPMetadata],
        coords: Coordinates
    ) -> List[str]:
        """Generate TCP-specific insights"""
        insights = []

        if coords.justice > 0.7:
            insights.append(
                "High Justice dimension: Many connection resets detected. "
                "Service may be unavailable or actively rejecting connections."
            )

        if coords.love > 0.7 and coords.power > 0.7:
            insights.append(
                "High Love + Power: Active, healthy data transfer occurring. "
                "Connections are established and data is flowing."
            )

        if coords.love < 0.5:
            insights.append(
                "Low Love dimension: Connection establishment problems. "
                "Check if service is running and accessible."
            )

        return insights

    def _describe_tcp_context(
        self,
        packets: List[TCPMetadata],
        coords: Coordinates
    ) -> str:
        """Describe TCP communication context"""
        if coords.justice > 0.7:
            return "CONNECTION REJECTION: High RST rate indicates service blocking"
        elif coords.love > 0.7 and coords.power > 0.7:
            return "ACTIVE TRANSFER: Healthy data exchange in progress"
        elif coords.love > 0.7:
            return "CONNECTED: Established connections with limited data transfer"
        else:
            return "CONNECTION ISSUES: Problems establishing or maintaining connections"

    # DNS Analysis Methods

    def _dns_metadata_to_coordinates(
        self,
        packets: List[DNSMetadata]
    ) -> Coordinates:
        """Map DNS metadata to LJPW coordinates"""

        # Analyze success rate
        successful = [p for p in packets if p.answers]
        success_rate = len(successful) / len(packets) if packets else 0

        # Love: Resolution success (connects names to IPs)
        love = 0.3 + (success_rate * 0.6)  # 0.3-0.9 range

        # Justice: Policy/filtering (low for DNS)
        justice = 0.2

        # Power: Speed of resolution (we don't have timing, assume medium)
        power = 0.6

        # Wisdom: Information quality (did we get answers?)
        wisdom = 0.5 + (success_rate * 0.4)  # 0.5-0.9 range

        return Coordinates(love, justice, power, wisdom)

    def _detect_dns_patterns(self, packets: List[DNSMetadata]) -> List[str]:
        """Detect DNS-specific patterns"""
        patterns = []

        queries = [p for p in packets if p.query_name]
        responses = [p for p in packets if p.answers]

        if queries:
            patterns.append(f"DNS queries detected ({len(queries)} queries)")

        if responses:
            patterns.append(f"DNS responses received ({len(responses)} responses)")

        # Analyze TTL patterns in answers
        all_ttls = []
        for p in responses:
            all_ttls.extend(p.answer_ttls)

        if all_ttls:
            avg_ttl = sum(all_ttls) / len(all_ttls)
            if avg_ttl < 60:
                patterns.append("Low DNS TTLs (frequent updates expected)")
            elif avg_ttl > 86400:
                patterns.append("High DNS TTLs (static records)")

        return patterns

    def _generate_dns_insights(
        self,
        packets: List[DNSMetadata],
        coords: Coordinates
    ) -> List[str]:
        """Generate DNS-specific insights"""
        insights = []

        if coords.wisdom < 0.6:
            insights.append(
                "Low Wisdom dimension: Many DNS queries failing. "
                "Check DNS server availability and configuration."
            )

        if coords.love < 0.5:
            insights.append(
                "Low Love dimension: Name resolution failing. "
                "Applications cannot connect to named services."
            )

        return insights

    def _describe_dns_context(
        self,
        packets: List[DNSMetadata],
        coords: Coordinates
    ) -> str:
        """Describe DNS communication context"""
        if coords.wisdom > 0.7:
            return "HEALTHY: DNS resolution working well"
        elif coords.wisdom < 0.5:
            return "DNS ISSUES: Many queries failing"
        else:
            return "PARTIAL: Some DNS queries succeeding"

    # Common Methods

    def _assess_health(self, coords: Coordinates) -> str:
        """Assess overall health from coordinates"""
        avg = (coords.love + coords.justice + coords.power + coords.wisdom) / 4

        if avg > 0.8:
            return "EXCELLENT"
        elif avg > 0.6:
            return "GOOD"
        elif avg > 0.4:
            return "FAIR"
        elif avg > 0.2:
            return "POOR"
        else:
            return "CRITICAL"


if __name__ == "__main__":
    # Demo with simulated data
    print("Semantic Packet Analyzer Demo")
    print("=" * 70)

    analyzer = SemanticPacketAnalyzer()

    # Simulate some ICMP packets
    from datetime import datetime

    simulated_icmp = [
        ICMPMetadata(
            type=0, code=0, ttl=64, packet_size=64,
            sequence=i, timestamp=datetime.now(),
            source_ip="8.8.8.8", dest_ip="192.168.1.1"
        )
        for i in range(10)
    ]

    print("\nAnalyzing simulated ICMP packets...")
    result = analyzer.analyze_icmp_packets(simulated_icmp)

    print(f"\nCoordinates: {result.coordinates}")
    print(f"Context: {result.context}")
    print(f"Health: {result.health_assessment}")
    print(f"\nPatterns:")
    for p in result.patterns_detected:
        print(f"  - {p}")
    print(f"\nInsights:")
    for i in result.insights:
        print(f"  - {i}")
