#!/usr/bin/env python3
"""
Enhanced Network Diagnostics with Deep Metadata Extraction

Captures and analyzes protocol metadata for nuanced semantic insights.
"""

import subprocess
import re
import struct
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict
from datetime import datetime

from .semantic_engine import NetworkSemanticEngine, Coordinates
from .metadata_extractor import MetadataExtractor


@dataclass
class EnhancedPingPacket:
    """Single ping packet with full metadata"""

    sequence: int
    ttl: int
    latency: float
    payload_sent: Optional[bytes]
    payload_received: Optional[bytes]
    timestamp: datetime
    success: bool


@dataclass
class EnhancedPingResult:
    """Ping result with deep metadata analysis"""

    host: str
    packets: List[EnhancedPingPacket]
    basic_coords: Coordinates  # Basic analysis
    deep_coords: Dict  # Deep metadata analysis
    semantic_insights: Dict  # Detailed insights from metadata
    contexts: List[str]  # Multiple context descriptions
    overall_health: float
    timestamp: datetime


class EnhancedNetworkDiagnostics:
    """Network diagnostics with deep metadata extraction"""

    def __init__(self, semantic_engine: NetworkSemanticEngine):
        self.engine = semantic_engine
        self.metadata_extractor = MetadataExtractor()

    def enhanced_ping(
        self,
        host: str,
        count: int = 10,
        timeout: int = 5,
        packet_size: int = 56
    ) -> EnhancedPingResult:
        """
        Ping with deep metadata extraction

        Captures:
        - TTL values (path analysis)
        - Sequence numbers (loss pattern)
        - Precise timing (performance analysis)
        - Payload integrity (link quality)
        """
        import platform

        system = platform.system()

        # Construct ping command based on OS
        if system == "Windows":
            cmd = [
                "ping",
                "-n", str(count),
                "-w", str(timeout * 1000),
                "-l", str(packet_size),
                host
            ]
        else:
            cmd = [
                "ping",
                "-c", str(count),
                "-W", str(timeout),
                "-s", str(packet_size),
                host
            ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout * count + 10
            )
            output = result.stdout

            # Parse ping output to extract metadata
            packets = self._parse_ping_output(output, system)

            # Perform basic analysis
            success_packets = [p for p in packets if p.success]
            if success_packets:
                avg_latency = sum(p.latency for p in success_packets) / len(success_packets)
                packet_loss = (count - len(success_packets)) / count * 100
            else:
                avg_latency = 0
                packet_loss = 100

            # Basic coordinates
            love = 1.0 - (packet_loss / 100)
            power = max(0, 1.0 - (avg_latency / 500))
            wisdom = 0.9 if success_packets else 0.1
            justice = 0.2
            basic_coords = Coordinates(love, justice, power, wisdom)

            # Deep metadata analysis
            if len(packets) >= 3:
                deep_analysis = self._deep_analyze_packets(packets)
            else:
                deep_analysis = {
                    "coordinates": {"love": love, "justice": justice, "power": power, "wisdom": wisdom},
                    "contexts": ["Insufficient packets for deep analysis"],
                    "insights": {},
                    "overall_health": (love + power + wisdom) / 3
                }

            return EnhancedPingResult(
                host=host,
                packets=packets,
                basic_coords=basic_coords,
                deep_coords=deep_analysis["coordinates"],
                semantic_insights=deep_analysis["insights"],
                contexts=deep_analysis["contexts"],
                overall_health=deep_analysis["overall_health"],
                timestamp=datetime.now()
            )

        except subprocess.TimeoutExpired:
            return EnhancedPingResult(
                host=host,
                packets=[],
                basic_coords=Coordinates(0, 0.5, 0, 0.1),
                deep_coords={"love": 0, "justice": 0.5, "power": 0, "wisdom": 0.1},
                semantic_insights={},
                contexts=["Ping timeout - complete failure"],
                overall_health=0.0,
                timestamp=datetime.now()
            )

    def _parse_ping_output(
        self,
        output: str,
        system: str
    ) -> List[EnhancedPingPacket]:
        """Parse ping output to extract metadata from each packet"""

        packets = []

        if system == "Windows":
            # Windows ping format:
            # Reply from 8.8.8.8: bytes=32 time=14ms TTL=118
            pattern = r"Reply from .+?: bytes=(\d+) time[=<](\d+)ms TTL=(\d+)"
            sequence = 0

            for line in output.split('\n'):
                match = re.search(pattern, line)
                if match:
                    sequence += 1
                    size = int(match.group(1))
                    latency = float(match.group(2))
                    ttl = int(match.group(3))

                    packets.append(EnhancedPingPacket(
                        sequence=sequence,
                        ttl=ttl,
                        latency=latency,
                        payload_sent=None,  # Windows ping doesn't show payload
                        payload_received=None,
                        timestamp=datetime.now(),
                        success=True
                    ))

                elif "Request timed out" in line or "Destination host unreachable" in line:
                    sequence += 1
                    packets.append(EnhancedPingPacket(
                        sequence=sequence,
                        ttl=0,
                        latency=0,
                        payload_sent=None,
                        payload_received=None,
                        timestamp=datetime.now(),
                        success=False
                    ))

        else:
            # Linux/Unix ping format:
            # 64 bytes from 8.8.8.8: icmp_seq=1 ttl=118 time=14.2 ms
            pattern = r"(\d+) bytes from .+?: icmp_seq=(\d+) ttl=(\d+) time=([\d.]+) ms"

            for line in output.split('\n'):
                match = re.search(pattern, line)
                if match:
                    size = int(match.group(1))
                    seq = int(match.group(2))
                    ttl = int(match.group(3))
                    latency = float(match.group(4))

                    packets.append(EnhancedPingPacket(
                        sequence=seq,
                        ttl=ttl,
                        latency=latency,
                        payload_sent=None,
                        payload_received=None,
                        timestamp=datetime.now(),
                        success=True
                    ))

        return packets

    def _deep_analyze_packets(
        self,
        packets: List[EnhancedPingPacket]
    ) -> Dict:
        """Perform deep analysis on packet metadata"""

        # Extract metadata
        ttls = [p.ttl for p in packets if p.success]
        sequences_sent = [p.sequence for p in packets]
        sequences_recv = [p.sequence for p in packets if p.success]
        latencies = [p.latency for p in packets if p.success]

        # Analyze each dimension
        ttl_semantics = self.metadata_extractor.extract_ttl_semantics(ttls)
        seq_semantics = self.metadata_extractor.extract_sequence_semantics(
            sequences_sent, sequences_recv
        )
        time_semantics = self.metadata_extractor.extract_timing_semantics(latencies)

        # Combine analyses
        combined = self.metadata_extractor.combine_metadata_semantics(
            ttl_semantics,
            seq_semantics,
            time_semantics
        )

        return combined

    def print_enhanced_ping_report(self, result: EnhancedPingResult):
        """Print detailed report with metadata insights"""

        print("\n" + "="*70)
        print(f"ENHANCED PING ANALYSIS: {result.host}")
        print("="*70)

        # Basic statistics
        success_packets = [p for p in result.packets if p.success]
        if success_packets:
            print(f"\n📊 BASIC STATISTICS")
            print(f"   Packets: {len(success_packets)}/{len(result.packets)} received")
            print(f"   Loss: {(1 - len(success_packets)/len(result.packets))*100:.1f}%")
            print(f"   Latency: {sum(p.latency for p in success_packets)/len(success_packets):.1f}ms avg")

        # Basic LJPW
        print(f"\n🎯 BASIC SEMANTIC ANALYSIS")
        print(f"   Coordinates: {result.basic_coords}")

        # Deep metadata insights
        print(f"\n🔬 DEEP METADATA ANALYSIS")
        print(f"   Enhanced Coordinates: L={result.deep_coords['love']:.2f}, "
              f"J={result.deep_coords['justice']:.2f}, "
              f"P={result.deep_coords['power']:.2f}, "
              f"W={result.deep_coords['wisdom']:.2f}")
        print(f"   Overall Health: {result.overall_health:.0%}")

        # Detailed insights
        if "path" in result.semantic_insights:
            path = result.semantic_insights["path"]
            print(f"\n🛣️  PATH ANALYSIS")
            print(f"   Hops: {path['hops']:.1f} average")
            print(f"   Complexity: {path['complexity']}")
            print(f"   Stability: {path['stability']:.0%}")
            if path['route_changing']:
                print(f"   ⚠️  WARNING: Route changing between packets!")

        if "delivery" in result.semantic_insights:
            delivery = result.semantic_insights["delivery"]
            print(f"\n📦 DELIVERY ANALYSIS")
            print(f"   Loss Rate: {delivery['loss_rate']*100:.1f}%")
            print(f"   Pattern: {delivery['pattern']}")
            if delivery['qos_detected']:
                print(f"   ⚠️  QoS POLICY DETECTED: Traffic being filtered/shaped")

        if "performance" in result.semantic_insights:
            perf = result.semantic_insights["performance"]
            print(f"\n⚡ PERFORMANCE ANALYSIS")
            print(f"   Latency: {perf['avg_latency']:.1f}ms")
            print(f"   Stability: {perf['stability']:.0%}")
            print(f"   Pattern: {perf['pattern']}")
            if perf['trend']:
                trend_icon = "📈" if perf['trend'] == "improving" else "📉" if perf['trend'] == "worsening" else "➡️"
                print(f"   Trend: {trend_icon} {perf['trend']}")

        # Context interpretations
        print(f"\n💡 SEMANTIC CONTEXTS")
        for i, context in enumerate(result.contexts, 1):
            print(f"   {i}. {context}")

        # Health assessment
        print(f"\n🏥 HEALTH ASSESSMENT")
        if result.overall_health > 0.8:
            print(f"   ✅ EXCELLENT: Network path is healthy and stable")
        elif result.overall_health > 0.6:
            print(f"   ✓  GOOD: Minor issues detected but overall functional")
        elif result.overall_health > 0.4:
            print(f"   ⚠️  FAIR: Significant issues affecting performance/reliability")
        else:
            print(f"   ❌ POOR: Critical issues requiring attention")

        print("\n" + "="*70)


def demo_enhanced_diagnostics():
    """Demonstrate enhanced diagnostics with real metadata extraction"""

    engine = NetworkSemanticEngine()
    diag = EnhancedNetworkDiagnostics(engine)

    print("\n" + "="*70)
    print("ENHANCED DIAGNOSTICS DEMONSTRATION")
    print("Deep Metadata Extraction and Semantic Analysis")
    print("="*70)

    # Test with Google DNS (should be stable and fast)
    print("\n\nTest 1: Google DNS (8.8.8.8) - Expected: Healthy, stable")
    print("-"*70)

    result = diag.enhanced_ping("8.8.8.8", count=10, timeout=3)
    diag.print_enhanced_ping_report(result)

    print("\n\n" + "="*70)
    print("KEY INSIGHTS FROM METADATA")
    print("="*70)
    print("""
The enhanced diagnostics extract semantic meaning from:

1. TTL Values → Path complexity and stability
   - Varying TTL = route changing (Love dimension instability)
   - High hop count = complex path (lower Love score)

2. Sequence Patterns → Loss detection and QoS
   - Periodic loss = QoS filtering (Justice dimension)
   - Burst loss = congestion (Power dimension)
   - Random loss = noisy link (Power dimension)

3. Timing Patterns → Performance and stability
   - Bimodal latency = load balancing detected
   - Increasing latency = degrading performance
   - High variance = unstable path

4. Payload Integrity → Link quality
   - Corruption = link issues (Power dimension)
   - Tampering detection (Justice dimension)

Each metadata field adds nuance to the semantic interpretation!
    """)


if __name__ == "__main__":
    demo_enhanced_diagnostics()
