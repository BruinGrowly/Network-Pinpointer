#!/usr/bin/env python3
"""
Deep Metadata Extractors - Parse Protocol Responses for Semantic Insights

Extracts semantic meaning from protocol metadata fields:
- TTL patterns (path complexity, stability)
- Sequence gaps (loss patterns, QoS detection)
- Timing variance (congestion, bimodal routing)
- TCP options (implementation sophistication)
- Window sizes (capacity, flow control)
"""

import statistics
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from collections import Counter


@dataclass
class TTLSemantics:
    """Semantic interpretation of TTL patterns"""

    avg_hops: float
    hop_variance: float
    path_stability: float  # 0-1 (1=stable)
    path_complexity: str  # "simple", "moderate", "complex", "extreme"
    love_score: float  # Overall connectivity quality
    wisdom_score: float  # Path visibility
    context: str
    route_changing: bool


@dataclass
class SequenceSemantics:
    """Semantic interpretation of packet sequence patterns"""

    loss_rate: float
    loss_pattern: str  # "none", "random", "burst", "periodic"
    selective_filtering: bool
    justice_score: float  # Policy enforcement detected
    love_score: float  # Delivery reliability
    power_score: float  # Link quality
    context: str


@dataclass
class TimingSemantics:
    """Semantic interpretation of timing patterns"""

    avg_latency: float
    latency_variance: float
    stability_coefficient: float  # 0-1 (1=stable)
    pattern: str  # "stable", "variable", "bimodal", "degrading", "improving"
    power_score: float  # Performance quality
    love_score: float  # Path stability
    context: str
    trend: Optional[str]  # "worsening", "improving", "stable"


@dataclass
class PayloadSemantics:
    """Semantic interpretation of payload integrity"""

    corruption_rate: float
    integrity_score: float  # 0-1
    justice_score: float  # Integrity maintained
    power_score: float  # Link quality
    context: str
    possible_tampering: bool


class MetadataExtractor:
    """Extract deep semantic meaning from protocol metadata"""

    def __init__(self):
        # Known OS TTL starting values
        self.os_ttl_defaults = {
            "linux": 64,
            "windows": 128,
            "cisco": 255,
            "freebsd": 64,
            "macos": 64,
        }

    def extract_ttl_semantics(
        self,
        ttl_values: List[int],
        expected_os: str = "linux"
    ) -> TTLSemantics:
        """
        Extract semantic meaning from TTL patterns

        TTL reveals:
        - Path length (how many hops)
        - Path stability (does route change?)
        - Network visibility (can we see the path?)
        """
        if not ttl_values:
            return TTLSemantics(
                avg_hops=0,
                hop_variance=0,
                path_stability=0,
                path_complexity="unknown",
                love_score=0,
                wisdom_score=0,
                context="No TTL data available",
                route_changing=False
            )

        # Determine starting TTL
        max_ttl = max(ttl_values)
        if max_ttl <= 64:
            start_ttl = 64
            os_detected = "linux/unix"
        elif max_ttl <= 128:
            start_ttl = 128
            os_detected = "windows"
        else:
            start_ttl = 255
            os_detected = "network_device"

        # Calculate hops taken
        hops = [start_ttl - ttl for ttl in ttl_values]
        avg_hops = statistics.mean(hops)
        hop_variance = statistics.stdev(hops) if len(hops) > 1 else 0

        # Path stability (low variance = stable route)
        path_stability = max(0, 1.0 - (hop_variance / 5))
        route_changing = hop_variance > 1.5

        # Path complexity classification
        if avg_hops < 5:
            complexity = "simple"
            complexity_desc = "direct path with minimal intermediaries"
        elif avg_hops < 10:
            complexity = "moderate"
            complexity_desc = "typical internet path"
        elif avg_hops < 20:
            complexity = "complex"
            complexity_desc = "distant or complex routing"
        else:
            complexity = "extreme"
            complexity_desc = "very distant or highly complex path"

        # Love dimension: Path quality and stability
        # More hops = more fragile (more points of failure)
        love_from_hops = max(0, 1.0 - (avg_hops / 30))
        love_from_stability = path_stability
        love_score = (love_from_hops * 0.6 + love_from_stability * 0.4)

        # Wisdom dimension: Path visibility
        # Lower TTL = less visibility remaining
        min_ttl = min(ttl_values)
        wisdom_score = min_ttl / start_ttl

        # Generate context
        if route_changing:
            context = f"UNSTABLE PATH: Route changing between packets ({complexity_desc}, {avg_hops:.1f} hops avg)"
        else:
            context = f"STABLE PATH: Consistent routing ({complexity_desc}, {avg_hops:.1f} hops)"

        return TTLSemantics(
            avg_hops=avg_hops,
            hop_variance=hop_variance,
            path_stability=path_stability,
            path_complexity=complexity,
            love_score=love_score,
            wisdom_score=wisdom_score,
            context=context,
            route_changing=route_changing
        )

    def extract_sequence_semantics(
        self,
        sent_sequences: List[int],
        received_sequences: List[int]
    ) -> SequenceSemantics:
        """
        Extract semantic meaning from sequence patterns

        Sequence analysis reveals:
        - Loss patterns (random vs selective)
        - QoS policies (periodic filtering)
        - Congestion (burst losses)
        """
        if not sent_sequences:
            return SequenceSemantics(
                loss_rate=0,
                loss_pattern="none",
                selective_filtering=False,
                justice_score=0.2,
                love_score=1.0,
                power_score=1.0,
                context="No sequence data"
            )

        # Find lost sequences
        sent_set = set(sent_sequences)
        recv_set = set(received_sequences)
        lost_set = sent_set - recv_set

        loss_rate = len(lost_set) / len(sent_set) if sent_set else 0

        if not lost_set:
            # No loss
            return SequenceSemantics(
                loss_rate=0,
                loss_pattern="none",
                selective_filtering=False,
                justice_score=0.2,
                love_score=1.0,
                power_score=1.0,
                context="Perfect delivery - no packet loss"
            )

        lost_list = sorted(list(lost_set))

        # Pattern detection
        pattern, justice_score, love_score, power_score, context, selective = self._detect_loss_pattern(
            sent_sequences, lost_list, loss_rate
        )

        return SequenceSemantics(
            loss_rate=loss_rate,
            loss_pattern=pattern,
            selective_filtering=selective,
            justice_score=justice_score,
            love_score=love_score,
            power_score=power_score,
            context=context
        )

    def _detect_loss_pattern(
        self,
        sent: List[int],
        lost: List[int],
        loss_rate: float
    ) -> Tuple[str, float, float, float, str, bool]:
        """Detect pattern in packet loss"""

        if len(lost) < 2:
            # Single packet loss - likely random
            return (
                "random",
                0.2,  # justice (not policy-based)
                0.9,  # love (mostly connected)
                0.8,  # power (minor issue)
                "Single packet lost - likely random transmission error",
                False
            )

        # Check for periodic pattern (QoS filtering)
        gaps = [lost[i+1] - lost[i] for i in range(len(lost)-1)]

        if len(set(gaps)) == 1 and len(gaps) >= 2:
            # Uniform spacing = periodic filtering
            gap = gaps[0]
            return (
                f"periodic_every_{gap}",
                0.8,  # justice (HIGH - deliberate filtering)
                0.5,  # love (some packets through)
                0.6,  # power (moderate)
                f"QoS POLICY DETECTED: Every {gap}th packet filtered - rate limiting in effect",
                True
            )

        # Check for burst losses (congestion)
        consecutive_losses = []
        current_burst = 1
        for i in range(len(lost)-1):
            if lost[i+1] - lost[i] == 1:
                current_burst += 1
            else:
                if current_burst > 1:
                    consecutive_losses.append(current_burst)
                current_burst = 1

        if current_burst > 1:
            consecutive_losses.append(current_burst)

        if consecutive_losses and max(consecutive_losses) >= 3:
            # Burst loss = congestion
            max_burst = max(consecutive_losses)
            return (
                f"burst_{max_burst}",
                0.3,  # justice (not policy)
                0.6,  # love (intermittent)
                0.3,  # power (LOW - congestion)
                f"CONGESTION DETECTED: Burst packet loss (max {max_burst} consecutive) indicates overload",
                False
            )

        # Random loss (noisy link)
        return (
            "random",
            0.2,  # justice
            0.7,  # love
            0.5,  # power (link quality)
            f"Random packet loss ({loss_rate*100:.0f}%) - noisy link or interference",
            False
        )

    def extract_timing_semantics(
        self,
        latencies: List[float]
    ) -> TimingSemantics:
        """
        Extract semantic meaning from timing patterns

        Timing analysis reveals:
        - Performance stability
        - Congestion patterns
        - Route changes (bimodal distribution)
        - Trends (degrading/improving)
        """
        if not latencies:
            return TimingSemantics(
                avg_latency=0,
                latency_variance=0,
                stability_coefficient=0,
                pattern="unknown",
                power_score=0,
                love_score=0,
                context="No timing data",
                trend=None
            )

        avg = statistics.mean(latencies)
        variance = statistics.variance(latencies) if len(latencies) > 1 else 0
        stdev = statistics.stdev(latencies) if len(latencies) > 1 else 0

        # Coefficient of variation (normalized variability)
        cv = stdev / avg if avg > 0 else 0
        stability = max(0, 1.0 - cv)

        # Power score from performance
        power_from_speed = max(0, 1.0 - (avg / 500))  # 500ms = very bad
        power_from_stability = stability
        power_score = (power_from_speed * 0.6 + power_from_stability * 0.4)

        # Detect patterns
        pattern, love_score, context, trend = self._detect_timing_pattern(
            latencies, avg, cv, stdev
        )

        return TimingSemantics(
            avg_latency=avg,
            latency_variance=variance,
            stability_coefficient=stability,
            pattern=pattern,
            power_score=power_score,
            love_score=love_score,
            context=context,
            trend=trend
        )

    def _detect_timing_pattern(
        self,
        latencies: List[float],
        avg: float,
        cv: float,
        stdev: float
    ) -> Tuple[str, float, str, Optional[str]]:
        """Detect pattern in timing data"""

        # Check for bimodal distribution (two paths)
        if len(latencies) >= 10:
            sorted_lats = sorted(latencies)
            mid = len(sorted_lats) // 2
            cluster1_avg = statistics.mean(sorted_lats[:mid])
            cluster2_avg = statistics.mean(sorted_lats[mid:])

            if cluster2_avg > cluster1_avg * 2:
                # Bimodal - two distinct paths
                return (
                    "bimodal",
                    0.7,  # love (using multiple paths)
                    f"BIMODAL ROUTING: Traffic alternating between fast path ({cluster1_avg:.0f}ms) and slow path ({cluster2_avg:.0f}ms) - load balancing or failover",
                    None
                )

        # Check for trending
        if len(latencies) >= 6:
            mid_point = len(latencies) // 2
            first_half = statistics.mean(latencies[:mid_point])
            second_half = statistics.mean(latencies[mid_point:])

            if second_half > first_half * 1.5:
                # Degrading
                return (
                    "degrading",
                    0.5,  # love (getting worse)
                    f"DEGRADING PERFORMANCE: Latency increasing from {first_half:.0f}ms to {second_half:.0f}ms - congestion building",
                    "worsening"
                )
            elif first_half > second_half * 1.5:
                # Improving
                return (
                    "improving",
                    0.8,  # love (getting better)
                    f"IMPROVING PERFORMANCE: Latency decreasing from {first_half:.0f}ms to {second_half:.0f}ms - congestion clearing",
                    "improving"
                )

        # Stable vs variable
        if cv < 0.15:
            return (
                "stable",
                0.9,  # love (very stable)
                f"STABLE PERFORMANCE: Consistent latency ({avg:.0f}ms ± {stdev:.0f}ms) - reliable path",
                "stable"
            )
        elif cv < 0.4:
            return (
                "variable",
                0.7,  # love (moderate stability)
                f"VARIABLE PERFORMANCE: Latency fluctuating ({avg:.0f}ms ± {stdev:.0f}ms) - some congestion or route variance",
                "stable"
            )
        else:
            return (
                "highly_variable",
                0.5,  # love (unstable)
                f"UNSTABLE PERFORMANCE: High latency variance ({avg:.0f}ms ± {stdev:.0f}ms) - significant congestion or routing issues",
                "stable"
            )

    def extract_payload_semantics(
        self,
        payload_pairs: List[Tuple[bytes, bytes]]
    ) -> PayloadSemantics:
        """
        Extract semantic meaning from payload integrity

        Payload analysis reveals:
        - Link quality (corruption)
        - Possible tampering
        - Transmission errors
        """
        if not payload_pairs:
            return PayloadSemantics(
                corruption_rate=0,
                integrity_score=1.0,
                justice_score=0.9,
                power_score=0.9,
                context="No payload data",
                possible_tampering=False
            )

        corrupted_count = 0
        total_differences = 0
        total_bytes = 0

        for sent, recv in payload_pairs:
            if sent != recv:
                corrupted_count += 1
                # Count bit differences
                min_len = min(len(sent), len(recv))
                differences = sum(s != r for s, r in zip(sent[:min_len], recv[:min_len]))
                total_differences += differences
                total_bytes += min_len

        corruption_rate = corrupted_count / len(payload_pairs)
        bit_error_rate = total_differences / total_bytes if total_bytes > 0 else 0

        integrity_score = 1.0 - bit_error_rate

        if corruption_rate == 0:
            return PayloadSemantics(
                corruption_rate=0,
                integrity_score=1.0,
                justice_score=0.9,
                power_score=0.9,
                context="Perfect payload integrity - clean transmission",
                possible_tampering=False
            )

        # High corruption might indicate tampering
        possible_tampering = bit_error_rate > 0.1

        if possible_tampering:
            return PayloadSemantics(
                corruption_rate=corruption_rate,
                integrity_score=integrity_score,
                justice_score=0.3,  # Integrity violated
                power_score=0.2,  # Severe issue
                context=f"SEVERE CORRUPTION: {bit_error_rate*100:.1f}% bit error rate - possible tampering or severe link issues",
                possible_tampering=True
            )
        else:
            return PayloadSemantics(
                corruption_rate=corruption_rate,
                integrity_score=integrity_score,
                justice_score=0.7,
                power_score=0.6,
                context=f"MINOR CORRUPTION: {bit_error_rate*100:.1f}% bit error rate - noisy link, normal for some environments",
                possible_tampering=False
            )

    def combine_metadata_semantics(
        self,
        ttl_sem: TTLSemantics,
        seq_sem: SequenceSemantics,
        time_sem: TimingSemantics,
        payload_sem: Optional[PayloadSemantics] = None
    ) -> Dict:
        """
        Combine all metadata analyses into holistic semantic understanding

        Returns comprehensive LJPW coordinates and deep context
        """
        # Combine Love scores (connectivity/stability)
        love = (
            ttl_sem.love_score * 0.3 +      # Path quality
            seq_sem.love_score * 0.3 +      # Delivery reliability
            time_sem.love_score * 0.4       # Path stability
        )

        # Combine Justice scores (policy/integrity)
        justice = seq_sem.justice_score
        if payload_sem:
            justice = (justice * 0.5 + payload_sem.justice_score * 0.5)

        # Combine Power scores (performance/quality)
        power = time_sem.power_score
        if payload_sem:
            power = (power * 0.6 + payload_sem.power_score * 0.4)

        # Wisdom from TTL (visibility)
        wisdom = ttl_sem.wisdom_score

        # Collect all contexts
        contexts = [
            ttl_sem.context,
            seq_sem.context,
            time_sem.context,
        ]
        if payload_sem:
            contexts.append(payload_sem.context)

        # Generate holistic insights
        insights = {
            "path": {
                "hops": ttl_sem.avg_hops,
                "stability": ttl_sem.path_stability,
                "complexity": ttl_sem.path_complexity,
                "route_changing": ttl_sem.route_changing,
            },
            "delivery": {
                "loss_rate": seq_sem.loss_rate,
                "pattern": seq_sem.loss_pattern,
                "qos_detected": seq_sem.selective_filtering,
            },
            "performance": {
                "avg_latency": time_sem.avg_latency,
                "stability": time_sem.stability_coefficient,
                "pattern": time_sem.pattern,
                "trend": time_sem.trend,
            },
        }

        if payload_sem:
            insights["integrity"] = {
                "corruption_rate": payload_sem.corruption_rate,
                "possible_tampering": payload_sem.possible_tampering,
            }

        return {
            "coordinates": {
                "love": love,
                "justice": justice,
                "power": power,
                "wisdom": wisdom,
            },
            "contexts": contexts,
            "insights": insights,
            "overall_health": (love + (1.0 - abs(justice - 0.5)) + power + wisdom) / 4,
        }
