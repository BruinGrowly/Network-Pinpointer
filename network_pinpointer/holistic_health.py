#!/usr/bin/env python3
"""
Holistic Network Health System

Tracks network-wide LJPW state over time, detects drift, and provides
system-level diagnosis (not just individual operations).

Key Features:
- Network-wide health score
- Temporal state tracking (detect drift)
- Reference models for healthy states
- Anomaly detection
- Root cause analysis
"""

import json
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from collections import deque

from .semantic_engine import Coordinates
from .metadata_extractor import MetadataExtractor


@dataclass
class NetworkSnapshot:
    """Single point-in-time network state"""

    timestamp: datetime
    aggregate_coords: Coordinates  # Network-wide LJPW
    device_count: int
    health_score: float  # 0-1
    dominant_weakness: str  # Which dimension is weakest
    critical_issues: int
    metadata: Dict  # Additional context


@dataclass
class HealthBaseline:
    """Expected healthy state for a network type"""

    network_type: str  # "enterprise", "datacenter", "high-security", etc.
    expected_coords: Coordinates
    tolerance: Dict[str, float]  # Acceptable variance per dimension
    description: str


@dataclass
class DriftAlert:
    """Alert for significant state drift"""

    timestamp: datetime
    dimension: str  # Which LJPW dimension drifted
    baseline_value: float
    current_value: float
    drift_amount: float
    severity: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    context: str


class NetworkHealthTracker:
    """Track holistic network health over time"""

    def __init__(self, state_file: str = ".network_health_state.json"):
        self.state_file = Path(state_file)
        self.snapshots: deque = deque(maxlen=1000)  # Keep last 1000 snapshots
        self.baseline: Optional[HealthBaseline] = None
        self.alerts: List[DriftAlert] = []

        # Load existing state if available
        self._load_state()

        # Reference models for different network types
        self.reference_models = self._build_reference_models()

    def _build_reference_models(self) -> Dict[str, HealthBaseline]:
        """Build reference models for healthy network states"""

        return {
            "enterprise": HealthBaseline(
                network_type="enterprise",
                expected_coords=Coordinates(
                    love=0.45,    # Good connectivity
                    justice=0.35, # Security present but not overwhelming
                    power=0.35,   # Adequate performance
                    wisdom=0.25   # Monitoring in place
                ),
                tolerance={
                    "love": 0.15,
                    "justice": 0.10,
                    "power": 0.15,
                    "wisdom": 0.10
                },
                description="Balanced enterprise network - connectivity with security"
            ),

            "datacenter": HealthBaseline(
                network_type="datacenter",
                expected_coords=Coordinates(
                    love=0.40,    # High connectivity between services
                    justice=0.25, # Moderate security (internal)
                    power=0.50,   # Performance-focused
                    wisdom=0.35   # Heavy monitoring
                ),
                tolerance={
                    "love": 0.10,
                    "justice": 0.15,
                    "power": 0.10,
                    "wisdom": 0.15
                },
                description="High-performance datacenter - power and monitoring focused"
            ),

            "high_security": HealthBaseline(
                network_type="high_security",
                expected_coords=Coordinates(
                    love=0.25,    # Limited connectivity by design
                    justice=0.60, # Security-dominant
                    power=0.25,   # Performance secondary
                    wisdom=0.40   # High monitoring for threats
                ),
                tolerance={
                    "love": 0.10,
                    "justice": 0.10,
                    "power": 0.15,
                    "wisdom": 0.10
                },
                description="High-security network - justice and wisdom dominant"
            ),

            "development": HealthBaseline(
                network_type="development",
                expected_coords=Coordinates(
                    love=0.50,    # High connectivity for collaboration
                    justice=0.20, # Minimal security (internal dev)
                    power=0.30,   # Moderate performance
                    wisdom=0.30   # Some monitoring
                ),
                tolerance={
                    "love": 0.15,
                    "justice": 0.20,
                    "power": 0.20,
                    "wisdom": 0.20
                },
                description="Development network - connectivity and collaboration focused"
            ),
        }

    def set_baseline(self, network_type: str):
        """Set the expected healthy baseline for this network"""

        if network_type in self.reference_models:
            self.baseline = self.reference_models[network_type]
            print(f"✓ Baseline set to: {network_type}")
            print(f"  Expected: {self.baseline.expected_coords}")
            self._save_state()
        else:
            available = ", ".join(self.reference_models.keys())
            raise ValueError(f"Unknown network type. Available: {available}")

    def record_snapshot(
        self,
        aggregate_coords: Coordinates,
        device_count: int,
        metadata: Optional[Dict] = None
    ) -> NetworkSnapshot:
        """Record a network state snapshot"""

        # Calculate health score
        health = self._calculate_health_score(aggregate_coords)

        # Find dominant weakness
        dims = {
            "Love": aggregate_coords.love,
            "Justice": aggregate_coords.justice,
            "Power": aggregate_coords.power,
            "Wisdom": aggregate_coords.wisdom
        }
        dominant_weakness = min(dims, key=dims.get)

        # Count critical issues
        critical = sum(1 for v in dims.values() if v < 0.3)

        snapshot = NetworkSnapshot(
            timestamp=datetime.now(),
            aggregate_coords=aggregate_coords,
            device_count=device_count,
            health_score=health,
            dominant_weakness=dominant_weakness,
            critical_issues=critical,
            metadata=metadata or {}
        )

        self.snapshots.append(snapshot)

        # Check for drift if we have a baseline
        if self.baseline:
            self._check_drift(snapshot)

        self._save_state()

        return snapshot

    def _calculate_health_score(self, coords: Coordinates) -> float:
        """Calculate overall network health (0-1)"""

        if self.baseline:
            # Compare to baseline
            expected = self.baseline.expected_coords
            tolerance = self.baseline.tolerance

            # Calculate how far from expected (within tolerance)
            love_dev = abs(coords.love - expected.love) / tolerance["love"]
            justice_dev = abs(coords.justice - expected.justice) / tolerance["justice"]
            power_dev = abs(coords.power - expected.power) / tolerance["power"]
            wisdom_dev = abs(coords.wisdom - expected.wisdom) / tolerance["wisdom"]

            # Average deviation (0 = perfect, >1 = outside tolerance)
            avg_deviation = (love_dev + justice_dev + power_dev + wisdom_dev) / 4

            # Convert to health score (0-1)
            health = max(0, 1.0 - (avg_deviation * 0.5))
        else:
            # No baseline - use absolute values
            # Health = average of all dimensions
            health = (coords.love + coords.justice + coords.power + coords.wisdom) / 4

        return health

    def _check_drift(self, snapshot: NetworkSnapshot):
        """Check if network state has drifted from baseline"""

        if not self.baseline:
            return

        expected = self.baseline.expected_coords
        current = snapshot.aggregate_coords
        tolerance = self.baseline.tolerance

        # Check each dimension
        dims = [
            ("Love", expected.love, current.love, tolerance["love"]),
            ("Justice", expected.justice, current.justice, tolerance["justice"]),
            ("Power", expected.power, current.power, tolerance["power"]),
            ("Wisdom", expected.wisdom, current.wisdom, tolerance["wisdom"]),
        ]

        for dim_name, exp_val, cur_val, tol in dims:
            drift = abs(cur_val - exp_val)

            if drift > tol:
                # Significant drift detected
                drift_ratio = drift / tol

                if drift_ratio > 2.0:
                    severity = "CRITICAL"
                elif drift_ratio > 1.5:
                    severity = "HIGH"
                elif drift_ratio > 1.2:
                    severity = "MEDIUM"
                else:
                    severity = "LOW"

                direction = "increased" if cur_val > exp_val else "decreased"

                alert = DriftAlert(
                    timestamp=datetime.now(),
                    dimension=dim_name,
                    baseline_value=exp_val,
                    current_value=cur_val,
                    drift_amount=drift,
                    severity=severity,
                    context=f"{dim_name} {direction} from {exp_val:.2f} to {cur_val:.2f} (expected ±{tol:.2f})"
                )

                self.alerts.append(alert)
                print(f"⚠️  DRIFT ALERT [{severity}]: {alert.context}")

    def get_current_health(self) -> Optional[NetworkSnapshot]:
        """Get most recent health snapshot"""
        return self.snapshots[-1] if self.snapshots else None

    def get_health_history(self, hours: int = 24) -> List[NetworkSnapshot]:
        """Get health snapshots from last N hours"""

        cutoff = datetime.now() - timedelta(hours=hours)
        return [s for s in self.snapshots if s.timestamp > cutoff]

    def analyze_trend(self, dimension: str, hours: int = 24) -> Dict:
        """Analyze trend for a specific dimension"""

        history = self.get_health_history(hours)

        if len(history) < 2:
            return {"trend": "insufficient_data"}

        # Extract dimension values over time
        dim_map = {
            "Love": lambda c: c.aggregate_coords.love,
            "Justice": lambda c: c.aggregate_coords.justice,
            "Power": lambda c: c.aggregate_coords.power,
            "Wisdom": lambda c: c.aggregate_coords.wisdom,
        }

        if dimension not in dim_map:
            return {"trend": "invalid_dimension"}

        values = [dim_map[dimension](s) for s in history]

        # Calculate trend
        first_half = sum(values[:len(values)//2]) / (len(values)//2)
        second_half = sum(values[len(values)//2:]) / (len(values) - len(values)//2)

        change = second_half - first_half
        change_pct = (change / first_half * 100) if first_half > 0 else 0

        if abs(change_pct) < 5:
            trend = "stable"
        elif change_pct > 0:
            trend = "improving"
        else:
            trend = "degrading"

        return {
            "trend": trend,
            "change": change,
            "change_percent": change_pct,
            "first_half_avg": first_half,
            "second_half_avg": second_half,
            "current": values[-1],
        }

    def generate_health_report(self) -> str:
        """Generate comprehensive health report"""

        report = []
        report.append("=" * 70)
        report.append("NETWORK HEALTH REPORT")
        report.append("=" * 70)

        current = self.get_current_health()

        if not current:
            report.append("\n❌ No health data available")
            return "\n".join(report)

        # Current state
        report.append(f"\n📊 CURRENT STATE ({current.timestamp.strftime('%Y-%m-%d %H:%M:%S')})")
        report.append(f"   Devices Monitored: {current.device_count}")
        report.append(f"   Health Score: {current.health_score:.0%}")
        report.append(f"   Dominant Weakness: {current.dominant_weakness}")
        report.append(f"   Critical Issues: {current.critical_issues}")

        # LJPW Coordinates
        c = current.aggregate_coords
        report.append(f"\n🎯 NETWORK-WIDE LJPW COORDINATES")
        report.append(f"   Love (Connectivity):  {c.love:.2f}  {'█' * int(c.love * 30)}")
        report.append(f"   Justice (Policy):     {c.justice:.2f}  {'█' * int(c.justice * 30)}")
        report.append(f"   Power (Performance):  {c.power:.2f}  {'█' * int(c.power * 30)}")
        report.append(f"   Wisdom (Monitoring):  {c.wisdom:.2f}  {'█' * int(c.wisdom * 30)}")

        # Baseline comparison
        if self.baseline:
            report.append(f"\n📏 BASELINE COMPARISON ({self.baseline.network_type})")
            exp = self.baseline.expected_coords

            for dim_name, exp_val, cur_val in [
                ("Love", exp.love, c.love),
                ("Justice", exp.justice, c.justice),
                ("Power", exp.power, c.power),
                ("Wisdom", exp.wisdom, c.wisdom),
            ]:
                diff = cur_val - exp_val
                icon = "✓" if abs(diff) < 0.15 else "⚠️"
                sign = "+" if diff > 0 else ""
                report.append(f"   {icon} {dim_name:10s}: {cur_val:.2f} (expected {exp_val:.2f}, {sign}{diff:.2f})")

        # Trends
        if len(self.snapshots) >= 5:
            report.append(f"\n📈 TRENDS (Last 24 hours)")

            for dim in ["Love", "Justice", "Power", "Wisdom"]:
                trend_data = self.analyze_trend(dim, hours=24)

                if trend_data["trend"] != "insufficient_data":
                    trend = trend_data["trend"]
                    change_pct = trend_data["change_percent"]

                    icon = "📈" if trend == "improving" else "📉" if trend == "degrading" else "➡️"
                    report.append(f"   {icon} {dim:10s}: {trend:10s} ({change_pct:+.1f}%)")

        # Recent alerts
        recent_alerts = [a for a in self.alerts if a.timestamp > datetime.now() - timedelta(hours=24)]

        if recent_alerts:
            report.append(f"\n🚨 RECENT ALERTS (Last 24 hours): {len(recent_alerts)}")

            # Group by severity
            by_severity = {}
            for alert in recent_alerts:
                if alert.severity not in by_severity:
                    by_severity[alert.severity] = []
                by_severity[alert.severity].append(alert)

            for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
                if severity in by_severity:
                    report.append(f"\n   {severity} ({len(by_severity[severity])}):")
                    for alert in by_severity[severity][:3]:  # Show top 3
                        report.append(f"     • {alert.context}")

                    if len(by_severity[severity]) > 3:
                        report.append(f"     ... and {len(by_severity[severity]) - 3} more")

        # Health assessment
        report.append(f"\n🏥 ASSESSMENT")

        if current.health_score > 0.8:
            report.append(f"   ✅ EXCELLENT: Network is healthy and stable")
        elif current.health_score > 0.6:
            report.append(f"   ✓  GOOD: Minor issues but overall functional")
        elif current.health_score > 0.4:
            report.append(f"   ⚠️  FAIR: Significant issues affecting network")
        else:
            report.append(f"   ❌ POOR: Critical issues requiring immediate attention")

        if current.dominant_weakness:
            report.append(f"\n   Primary Concern: {current.dominant_weakness} dimension is weakest")

            # Provide recommendations
            recommendations = self._get_recommendations(current)
            if recommendations:
                report.append(f"\n💡 RECOMMENDATIONS:")
                for rec in recommendations:
                    report.append(f"     → {rec}")

        report.append("\n" + "=" * 70)

        return "\n".join(report)

    def _get_recommendations(self, snapshot: NetworkSnapshot) -> List[str]:
        """Generate recommendations based on current state"""

        recommendations = []
        c = snapshot.aggregate_coords

        if c.love < 0.3:
            recommendations.append("Connectivity is critically low - check network topology and routing")
        elif c.love < 0.5:
            recommendations.append("Improve connectivity - consider redundant paths or load balancing")

        if c.justice > 0.7:
            recommendations.append("Very high security posture - ensure policies don't impede legitimate traffic")
        elif c.justice < 0.2:
            recommendations.append("Security is weak - implement firewall rules and access controls")

        if c.power < 0.3:
            recommendations.append("Performance is critically poor - check bandwidth and congestion")
        elif c.power < 0.5:
            recommendations.append("Performance degraded - consider capacity upgrades or QoS")

        if c.wisdom < 0.2:
            recommendations.append("Monitoring is insufficient - implement logging and metrics collection")
        elif c.wisdom < 0.4:
            recommendations.append("Improve visibility - add monitoring for key network components")

        if snapshot.critical_issues > 2:
            recommendations.append(f"Multiple critical issues detected - prioritize addressing {snapshot.dominant_weakness} dimension")

        return recommendations

    def _save_state(self):
        """Save state to disk"""

        try:
            state = {
                "baseline": {
                    "network_type": self.baseline.network_type,
                    "expected_coords": {
                        "love": self.baseline.expected_coords.love,
                        "justice": self.baseline.expected_coords.justice,
                        "power": self.baseline.expected_coords.power,
                        "wisdom": self.baseline.expected_coords.wisdom,
                    },
                    "tolerance": self.baseline.tolerance,
                    "description": self.baseline.description,
                } if self.baseline else None,

                "snapshots": [
                    {
                        "timestamp": s.timestamp.isoformat(),
                        "aggregate_coords": {
                            "love": s.aggregate_coords.love,
                            "justice": s.aggregate_coords.justice,
                            "power": s.aggregate_coords.power,
                            "wisdom": s.aggregate_coords.wisdom,
                        },
                        "device_count": s.device_count,
                        "health_score": s.health_score,
                        "dominant_weakness": s.dominant_weakness,
                        "critical_issues": s.critical_issues,
                        "metadata": s.metadata,
                    }
                    for s in list(self.snapshots)[-100:]  # Save last 100
                ],

                "alerts": [
                    {
                        "timestamp": a.timestamp.isoformat(),
                        "dimension": a.dimension,
                        "baseline_value": a.baseline_value,
                        "current_value": a.current_value,
                        "drift_amount": a.drift_amount,
                        "severity": a.severity,
                        "context": a.context,
                    }
                    for a in self.alerts[-50:]  # Save last 50 alerts
                ]
            }

            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)

        except Exception as e:
            print(f"Warning: Could not save state: {e}")

    def _load_state(self):
        """Load state from disk"""

        if not self.state_file.exists():
            return

        try:
            with open(self.state_file, 'r') as f:
                state = json.load(f)

            # Load baseline
            if state.get("baseline"):
                b = state["baseline"]
                exp = b["expected_coords"]
                self.baseline = HealthBaseline(
                    network_type=b["network_type"],
                    expected_coords=Coordinates(
                        love=exp["love"],
                        justice=exp["justice"],
                        power=exp["power"],
                        wisdom=exp["wisdom"],
                    ),
                    tolerance=b["tolerance"],
                    description=b["description"],
                )

            # Load snapshots
            for s in state.get("snapshots", []):
                coords = s["aggregate_coords"]
                snapshot = NetworkSnapshot(
                    timestamp=datetime.fromisoformat(s["timestamp"]),
                    aggregate_coords=Coordinates(
                        love=coords["love"],
                        justice=coords["justice"],
                        power=coords["power"],
                        wisdom=coords["wisdom"],
                    ),
                    device_count=s["device_count"],
                    health_score=s["health_score"],
                    dominant_weakness=s["dominant_weakness"],
                    critical_issues=s["critical_issues"],
                    metadata=s["metadata"],
                )
                self.snapshots.append(snapshot)

            # Load alerts
            for a in state.get("alerts", []):
                alert = DriftAlert(
                    timestamp=datetime.fromisoformat(a["timestamp"]),
                    dimension=a["dimension"],
                    baseline_value=a["baseline_value"],
                    current_value=a["current_value"],
                    drift_amount=a["drift_amount"],
                    severity=a["severity"],
                    context=a["context"],
                )
                self.alerts.append(alert)

            print(f"✓ Loaded {len(self.snapshots)} snapshots, {len(self.alerts)} alerts from state file")

        except Exception as e:
            print(f"Warning: Could not load state: {e}")
