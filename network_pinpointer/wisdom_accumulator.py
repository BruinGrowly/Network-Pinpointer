#!/usr/bin/env python3
"""
Wisdom Accumulator - Learning and Pattern Memory for Network Pinpointer

This module adds intelligence/learning capabilities to Network Pinpointer,
addressing the second priority identified through semantic oscillation:

    "The tool diagnoses but doesn't learn. Add intelligence layer."

Key Features:
- Pattern Memory: Remember and recognize recurring semantic patterns
- Anomaly Learning: Learn what "normal" looks like in LJPW space
- Predictive Semantics: Predict future states from historical patterns
- Root Cause Learning: Speed diagnosis through learned correlations
- Insight Accumulation: Build persistent network "wisdom" over time

Based on LJPW resonance insights - Wisdom dimension enhancement.
"""

import math
import json
import os
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from pathlib import Path
from enum import Enum

from .semantic_engine import Coordinates


# LJPW Constants
PHI_INV = (math.sqrt(5) - 1) / 2
SQRT2_M1 = math.sqrt(2) - 1
E_M2 = math.e - 2
LN2 = math.log(2)

NATURAL_EQUILIBRIUM = [PHI_INV, SQRT2_M1, E_M2, LN2]


class PatternType(Enum):
    """Types of recognized patterns"""
    DRIFT = "drift"                     # Gradual change over time
    SPIKE = "spike"                     # Sudden change
    CYCLE = "cycle"                     # Periodic pattern
    DEGRADATION = "degradation"         # Progressive worsening
    RECOVERY = "recovery"               # Return to baseline
    ANOMALY = "anomaly"                 # Unexpected state
    NORMAL = "normal"                   # Expected behavior


class AnomalySeverity(Enum):
    """Severity of detected anomalies"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class SemanticPattern:
    """A learned semantic pattern"""
    pattern_id: str
    pattern_type: PatternType
    signature: List[float]              # LJPW signature
    confidence: float                   # How confident we are
    frequency: int                      # How often seen
    last_seen: datetime
    context: Dict[str, Any]             # Associated context
    description: str


@dataclass
class Baseline:
    """Learned baseline for a service/network"""
    target: str
    mean_ljpw: List[float]
    std_ljpw: List[float]
    samples: int
    last_updated: datetime
    seasonal_patterns: Dict[str, List[float]]  # time_of_day -> expected LJPW


@dataclass
class Anomaly:
    """A detected anomaly"""
    target: str
    detected_at: datetime
    severity: AnomalySeverity
    current_ljpw: List[float]
    expected_ljpw: List[float]
    deviation: float                    # Standard deviations from normal
    affected_dimensions: List[str]
    description: str
    possible_causes: List[str]
    recommended_actions: List[str]


@dataclass
class Prediction:
    """A prediction about future state"""
    target: str
    predicted_at: datetime
    prediction_for: datetime
    predicted_ljpw: List[float]
    confidence: float
    trend: str                          # "stable", "improving", "degrading"
    risk_factors: List[str]
    basis: str                          # What the prediction is based on


@dataclass
class RootCauseCorrelation:
    """Learned correlation between symptoms and causes"""
    symptom_signature: List[float]      # LJPW pattern of symptom
    symptom_description: str
    probable_causes: List[Tuple[str, float]]  # (cause, probability)
    resolution_history: List[str]       # Past resolutions
    times_seen: int
    success_rate: float                 # % of correct diagnoses


@dataclass
class NetworkInsight:
    """An accumulated insight about the network"""
    insight_id: str
    created_at: datetime
    category: str                       # "performance", "security", "reliability"
    insight: str
    supporting_evidence: List[str]
    confidence: float
    actionable: bool
    suggested_actions: List[str]


class WisdomAccumulator:
    """
    Learns and remembers patterns from network behavior.
    Enables prediction and anomaly detection.

    The accumulator builds persistent network "wisdom" over time,
    storing patterns in a simple JSON-based storage that persists
    across sessions.
    """

    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = Path(storage_path or os.path.expanduser(
            "~/.network_pinpointer/wisdom"
        ))
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # In-memory caches
        self.patterns: Dict[str, SemanticPattern] = {}
        self.baselines: Dict[str, Baseline] = {}
        self.correlations: Dict[str, RootCauseCorrelation] = {}
        self.insights: List[NetworkInsight] = []
        self.history: Dict[str, List[Dict]] = {}  # target -> list of observations

        # Load existing wisdom
        self._load_wisdom()

    def _load_wisdom(self):
        """Load persisted wisdom from storage"""
        # Load patterns
        patterns_file = self.storage_path / "patterns.json"
        if patterns_file.exists():
            try:
                with open(patterns_file) as f:
                    data = json.load(f)
                    for pid, pdata in data.items():
                        pdata['pattern_type'] = PatternType(pdata['pattern_type'])
                        pdata['last_seen'] = datetime.fromisoformat(pdata['last_seen'])
                        self.patterns[pid] = SemanticPattern(**pdata)
            except Exception:
                pass

        # Load baselines
        baselines_file = self.storage_path / "baselines.json"
        if baselines_file.exists():
            try:
                with open(baselines_file) as f:
                    data = json.load(f)
                    for target, bdata in data.items():
                        bdata['last_updated'] = datetime.fromisoformat(bdata['last_updated'])
                        self.baselines[target] = Baseline(**bdata)
            except Exception:
                pass

        # Load correlations
        correlations_file = self.storage_path / "correlations.json"
        if correlations_file.exists():
            try:
                with open(correlations_file) as f:
                    data = json.load(f)
                    for cid, cdata in data.items():
                        self.correlations[cid] = RootCauseCorrelation(**cdata)
            except Exception:
                pass

    def _save_wisdom(self):
        """Persist wisdom to storage"""
        # Save patterns
        patterns_data = {}
        for pid, pattern in self.patterns.items():
            pdata = asdict(pattern)
            pdata['pattern_type'] = pattern.pattern_type.value
            pdata['last_seen'] = pattern.last_seen.isoformat()
            patterns_data[pid] = pdata

        with open(self.storage_path / "patterns.json", 'w') as f:
            json.dump(patterns_data, f, indent=2)

        # Save baselines
        baselines_data = {}
        for target, baseline in self.baselines.items():
            bdata = asdict(baseline)
            bdata['last_updated'] = baseline.last_updated.isoformat()
            baselines_data[target] = bdata

        with open(self.storage_path / "baselines.json", 'w') as f:
            json.dump(baselines_data, f, indent=2)

        # Save correlations
        correlations_data = {cid: asdict(c) for cid, c in self.correlations.items()}
        with open(self.storage_path / "correlations.json", 'w') as f:
            json.dump(correlations_data, f, indent=2)

    # ==================== PATTERN MEMORY ====================

    def learn_pattern(
        self,
        ljpw_signature: List[float],
        context: Dict[str, Any],
        description: Optional[str] = None
    ) -> SemanticPattern:
        """
        Store a pattern for future recognition.

        Patterns are semantic fingerprints that the system learns to recognize.
        """
        # Generate pattern ID from signature
        pattern_id = self._generate_pattern_id(ljpw_signature)

        # Check if we've seen this pattern before
        if pattern_id in self.patterns:
            # Update existing pattern
            existing = self.patterns[pattern_id]
            existing.frequency += 1
            existing.last_seen = datetime.now()
            existing.confidence = min(1.0, existing.confidence + 0.1)
            if context:
                existing.context.update(context)
        else:
            # Learn new pattern
            pattern_type = self._classify_pattern(ljpw_signature, context)

            self.patterns[pattern_id] = SemanticPattern(
                pattern_id=pattern_id,
                pattern_type=pattern_type,
                signature=ljpw_signature,
                confidence=0.5,
                frequency=1,
                last_seen=datetime.now(),
                context=context,
                description=description or self._describe_pattern(ljpw_signature, pattern_type)
            )

        self._save_wisdom()
        return self.patterns[pattern_id]

    def recognize_pattern(
        self,
        ljpw_signature: List[float],
        threshold: float = 0.2
    ) -> Optional[SemanticPattern]:
        """
        Try to recognize a pattern from learned patterns.

        Returns the best matching pattern if found within threshold.
        """
        best_match = None
        best_distance = float('inf')

        for pattern in self.patterns.values():
            distance = self._ljpw_distance(ljpw_signature, pattern.signature)
            if distance < threshold and distance < best_distance:
                best_distance = distance
                best_match = pattern

        return best_match

    def _generate_pattern_id(self, signature: List[float]) -> str:
        """Generate a unique ID for a pattern based on its signature"""
        # Quantize to reduce noise
        quantized = [round(v * 10) / 10 for v in signature]
        return f"pat_{'_'.join(str(int(v*10)) for v in quantized)}"

    def _classify_pattern(
        self,
        signature: List[float],
        context: Dict[str, Any]
    ) -> PatternType:
        """Classify a pattern based on its characteristics"""
        # Check distance from Natural Equilibrium
        ne_distance = self._ljpw_distance(signature, NATURAL_EQUILIBRIUM)

        # Check for dominance
        max_dim = max(signature)
        min_dim = min(signature)
        variance = max_dim - min_dim

        if ne_distance < 0.2:
            return PatternType.NORMAL
        elif variance > 0.5:
            # High variance indicates anomaly
            return PatternType.ANOMALY
        elif context.get('trend') == 'down':
            return PatternType.DEGRADATION
        elif context.get('trend') == 'up':
            return PatternType.RECOVERY
        elif context.get('sudden'):
            return PatternType.SPIKE
        else:
            return PatternType.DRIFT

    def _describe_pattern(self, signature: List[float], pattern_type: PatternType) -> str:
        """Generate human-readable description"""
        dims = ['Love', 'Justice', 'Power', 'Wisdom']
        dominant_idx = signature.index(max(signature))
        dominant = dims[dominant_idx]

        descriptions = {
            PatternType.NORMAL: f"Normal operation, {dominant}-dominant profile",
            PatternType.ANOMALY: f"Anomalous state with {dominant} dominance",
            PatternType.DRIFT: f"Gradual drift toward {dominant}",
            PatternType.SPIKE: f"Sudden spike in {dominant}",
            PatternType.DEGRADATION: "Progressive system degradation",
            PatternType.RECOVERY: "System recovering toward normal",
            PatternType.CYCLE: "Cyclic behavior detected"
        }

        return descriptions.get(pattern_type, "Unknown pattern")

    # ==================== ANOMALY LEARNING ====================

    def update_baseline(
        self,
        target: str,
        ljpw_observation: List[float],
        timestamp: Optional[datetime] = None
    ):
        """
        Update learned baseline for what "normal" looks like.

        Called with each observation to build understanding of normal.
        """
        timestamp = timestamp or datetime.now()

        if target not in self.baselines:
            # Initialize baseline
            self.baselines[target] = Baseline(
                target=target,
                mean_ljpw=ljpw_observation.copy(),
                std_ljpw=[0.1, 0.1, 0.1, 0.1],  # Initial uncertainty
                samples=1,
                last_updated=timestamp,
                seasonal_patterns={}
            )
        else:
            baseline = self.baselines[target]

            # Incremental mean update (Welford's algorithm)
            n = baseline.samples + 1
            for i in range(4):
                delta = ljpw_observation[i] - baseline.mean_ljpw[i]
                baseline.mean_ljpw[i] += delta / n

                # Update variance estimate
                if n > 1:
                    delta2 = ljpw_observation[i] - baseline.mean_ljpw[i]
                    baseline.std_ljpw[i] = math.sqrt(
                        ((n - 1) * baseline.std_ljpw[i]**2 + delta * delta2) / n
                    )

            baseline.samples = n
            baseline.last_updated = timestamp

            # Track seasonal patterns (by hour of day)
            hour_key = f"hour_{timestamp.hour}"
            if hour_key not in baseline.seasonal_patterns:
                baseline.seasonal_patterns[hour_key] = ljpw_observation.copy()
            else:
                # Average with existing
                existing = baseline.seasonal_patterns[hour_key]
                baseline.seasonal_patterns[hour_key] = [
                    (existing[i] + ljpw_observation[i]) / 2
                    for i in range(4)
                ]

        # Store in history
        if target not in self.history:
            self.history[target] = []
        self.history[target].append({
            'timestamp': timestamp.isoformat(),
            'ljpw': ljpw_observation
        })

        # Keep history bounded
        if len(self.history[target]) > 1000:
            self.history[target] = self.history[target][-1000:]

        self._save_wisdom()

    def detect_anomaly(self, target: str, current_ljpw: List[float]) -> Optional[Anomaly]:
        """
        Compare current state against learned baseline.

        Returns Anomaly if current state is significantly different from normal.
        """
        if target not in self.baselines:
            return None

        baseline = self.baselines[target]

        # Calculate z-scores for each dimension
        z_scores = []
        for i in range(4):
            if baseline.std_ljpw[i] > 0:
                z = abs(current_ljpw[i] - baseline.mean_ljpw[i]) / baseline.std_ljpw[i]
            else:
                z = abs(current_ljpw[i] - baseline.mean_ljpw[i]) * 10
            z_scores.append(z)

        max_z = max(z_scores)
        avg_z = sum(z_scores) / 4

        # No anomaly if within 2 standard deviations
        if max_z < 2:
            return None

        # Determine severity
        if max_z > 4 or avg_z > 3:
            severity = AnomalySeverity.CRITICAL
        elif max_z > 3 or avg_z > 2:
            severity = AnomalySeverity.HIGH
        elif max_z > 2.5:
            severity = AnomalySeverity.MEDIUM
        else:
            severity = AnomalySeverity.LOW

        # Identify affected dimensions
        dims = ['Love', 'Justice', 'Power', 'Wisdom']
        affected = [dims[i] for i, z in enumerate(z_scores) if z > 2]

        # Generate description
        description = self._describe_anomaly(current_ljpw, baseline.mean_ljpw, affected)

        # Find possible causes from correlations
        possible_causes = self._find_possible_causes(current_ljpw)

        # Generate recommendations
        recommendations = self._generate_anomaly_recommendations(
            current_ljpw, baseline.mean_ljpw, affected, severity
        )

        return Anomaly(
            target=target,
            detected_at=datetime.now(),
            severity=severity,
            current_ljpw=current_ljpw,
            expected_ljpw=baseline.mean_ljpw.copy(),
            deviation=avg_z,
            affected_dimensions=affected,
            description=description,
            possible_causes=possible_causes,
            recommended_actions=recommendations
        )

    def _describe_anomaly(
        self,
        current: List[float],
        expected: List[float],
        affected: List[str]
    ) -> str:
        """Generate anomaly description"""
        if not affected:
            return "Minor deviation from baseline"

        dims_map = {'Love': 0, 'Justice': 1, 'Power': 2, 'Wisdom': 3}
        changes = []

        for dim in affected:
            idx = dims_map[dim]
            diff = current[idx] - expected[idx]
            direction = "increased" if diff > 0 else "decreased"
            changes.append(f"{dim} {direction} significantly")

        return "; ".join(changes)

    def _find_possible_causes(self, signature: List[float]) -> List[str]:
        """Find possible causes from learned correlations"""
        causes = []

        for correlation in self.correlations.values():
            distance = self._ljpw_distance(signature, correlation.symptom_signature)
            if distance < 0.3:  # Similar symptom
                for cause, prob in correlation.probable_causes[:3]:
                    if prob > 0.3:
                        causes.append(f"{cause} (confidence: {prob:.0%})")

        if not causes:
            # Heuristic causes based on dimension analysis
            if signature[0] < 0.3:  # Low Love
                causes.append("Connectivity issue or service isolation")
            if signature[1] > 0.8:  # High Justice
                causes.append("Overly restrictive security policies")
            if signature[2] < 0.3:  # Low Power
                causes.append("Resource exhaustion or capacity issue")
            if signature[3] < 0.3:  # Low Wisdom
                causes.append("Monitoring/observability gap")

        return causes[:5]

    def _generate_anomaly_recommendations(
        self,
        current: List[float],
        expected: List[float],
        affected: List[str],
        severity: AnomalySeverity
    ) -> List[str]:
        """Generate recommendations for addressing anomaly"""
        recommendations = []

        if severity in [AnomalySeverity.CRITICAL, AnomalySeverity.HIGH]:
            recommendations.append("Immediate investigation recommended")

        if 'Love' in affected:
            if current[0] < expected[0]:
                recommendations.append("Check network connectivity and service health")
            else:
                recommendations.append("Verify expected increase in connectivity")

        if 'Justice' in affected:
            if current[1] > expected[1]:
                recommendations.append("Review recent security policy changes")
            else:
                recommendations.append("Check for security posture degradation")

        if 'Power' in affected:
            if current[2] < expected[2]:
                recommendations.append("Check resource utilization and capacity")
            else:
                recommendations.append("Verify expected performance improvement")

        if 'Wisdom' in affected:
            if current[3] < expected[3]:
                recommendations.append("Check monitoring systems and log collectors")
            else:
                recommendations.append("Review increased monitoring activity")

        recommendations.append("Compare with recent changes in change management system")

        return recommendations

    # ==================== PREDICTIVE SEMANTICS ====================

    def predict_next_state(
        self,
        target: str,
        horizon: timedelta = timedelta(hours=1)
    ) -> Optional[Prediction]:
        """
        Predict future LJPW state from historical patterns.
        """
        if target not in self.history or len(self.history[target]) < 10:
            return None

        history = self.history[target]

        # Get recent trend
        recent = history[-10:]
        trend_vectors = []

        for i in range(1, len(recent)):
            prev = recent[i-1]['ljpw']
            curr = recent[i]['ljpw']
            trend_vectors.append([curr[j] - prev[j] for j in range(4)])

        # Average trend
        avg_trend = [
            sum(tv[i] for tv in trend_vectors) / len(trend_vectors)
            for i in range(4)
        ]

        # Current state
        current = history[-1]['ljpw']

        # Project forward
        # Scale trend by horizon (assuming 1 history entry per hour)
        hours_forward = horizon.total_seconds() / 3600
        predicted = [
            max(0.0, min(1.0, current[i] + avg_trend[i] * hours_forward))
            for i in range(4)
        ]

        # Determine trend description
        total_change = sum(avg_trend)
        if abs(total_change) < 0.01:
            trend = "stable"
        elif total_change > 0:
            trend = "improving"
        else:
            trend = "degrading"

        # Calculate confidence based on trend consistency
        trend_variance = sum(
            sum((tv[i] - avg_trend[i])**2 for tv in trend_vectors) / len(trend_vectors)
            for i in range(4)
        ) / 4
        confidence = max(0.3, 1.0 - math.sqrt(trend_variance) * 5)

        # Identify risk factors
        risk_factors = []
        if predicted[0] < 0.3:
            risk_factors.append("Projected low connectivity")
        if predicted[2] < 0.3:
            risk_factors.append("Projected capacity issues")
        if trend == "degrading":
            risk_factors.append("Downward trend detected")

        return Prediction(
            target=target,
            predicted_at=datetime.now(),
            prediction_for=datetime.now() + horizon,
            predicted_ljpw=predicted,
            confidence=confidence,
            trend=trend,
            risk_factors=risk_factors,
            basis=f"Based on {len(recent)} recent observations"
        )

    # ==================== ROOT CAUSE LEARNING ====================

    def learn_root_cause(
        self,
        symptom_ljpw: List[float],
        symptom_description: str,
        root_cause: str,
        resolution: Optional[str] = None
    ):
        """
        Learn correlation between symptom pattern and root cause.
        """
        correlation_id = self._generate_pattern_id(symptom_ljpw)

        if correlation_id in self.correlations:
            # Update existing
            corr = self.correlations[correlation_id]
            corr.times_seen += 1

            # Update probable causes
            found = False
            for i, (cause, prob) in enumerate(corr.probable_causes):
                if cause == root_cause:
                    # Increase probability for this cause
                    new_prob = prob + (1 - prob) * 0.1
                    corr.probable_causes[i] = (cause, new_prob)
                    found = True
                else:
                    # Slightly decrease others
                    corr.probable_causes[i] = (cause, prob * 0.95)

            if not found:
                corr.probable_causes.append((root_cause, 0.5))

            # Add resolution
            if resolution and resolution not in corr.resolution_history:
                corr.resolution_history.append(resolution)
        else:
            # Create new correlation
            self.correlations[correlation_id] = RootCauseCorrelation(
                symptom_signature=symptom_ljpw,
                symptom_description=symptom_description,
                probable_causes=[(root_cause, 0.5)],
                resolution_history=[resolution] if resolution else [],
                times_seen=1,
                success_rate=0.5
            )

        self._save_wisdom()

    def diagnose(self, current_ljpw: List[float]) -> List[Tuple[str, float, List[str]]]:
        """
        Diagnose possible causes from current state.

        Returns list of (cause, probability, suggested_resolutions)
        """
        diagnoses = []

        for corr in self.correlations.values():
            distance = self._ljpw_distance(current_ljpw, corr.symptom_signature)
            if distance < 0.3:
                match_prob = 1.0 - distance / 0.3  # How well this matches

                for cause, cause_prob in corr.probable_causes:
                    combined_prob = match_prob * cause_prob
                    if combined_prob > 0.2:
                        diagnoses.append((
                            cause,
                            combined_prob,
                            corr.resolution_history[:3]
                        ))

        # Sort by probability
        diagnoses.sort(key=lambda x: x[1], reverse=True)

        return diagnoses[:5]

    # ==================== INSIGHT ACCUMULATION ====================

    def generate_insights(self) -> List[NetworkInsight]:
        """
        Generate insights from accumulated wisdom.

        Analyzes patterns, baselines, and correlations to produce
        actionable insights.
        """
        insights = []

        # Insight from pattern frequency
        frequent_patterns = [
            p for p in self.patterns.values()
            if p.frequency > 5
        ]

        for pattern in frequent_patterns:
            if pattern.pattern_type == PatternType.ANOMALY:
                insights.append(NetworkInsight(
                    insight_id=f"ins_{pattern.pattern_id}",
                    created_at=datetime.now(),
                    category="reliability",
                    insight=f"Recurring anomaly pattern detected: {pattern.description}",
                    supporting_evidence=[f"Seen {pattern.frequency} times"],
                    confidence=min(1.0, pattern.frequency / 10),
                    actionable=True,
                    suggested_actions=["Investigate root cause of recurring anomaly"]
                ))

        # Insights from baselines
        for target, baseline in self.baselines.items():
            # Check for dimension imbalance
            max_val = max(baseline.mean_ljpw)
            min_val = min(baseline.mean_ljpw)

            if max_val - min_val > 0.4:
                dims = ['Love', 'Justice', 'Power', 'Wisdom']
                high_dim = dims[baseline.mean_ljpw.index(max_val)]
                low_dim = dims[baseline.mean_ljpw.index(min_val)]

                insights.append(NetworkInsight(
                    insight_id=f"ins_balance_{target}",
                    created_at=datetime.now(),
                    category="optimization",
                    insight=f"{target} has significant imbalance: {high_dim} high, {low_dim} low",
                    supporting_evidence=[
                        f"Mean {high_dim}: {max_val:.2f}",
                        f"Mean {low_dim}: {min_val:.2f}"
                    ],
                    confidence=0.8,
                    actionable=True,
                    suggested_actions=[f"Consider improving {low_dim} dimension"]
                ))

        # Insights from correlations
        strong_correlations = [
            c for c in self.correlations.values()
            if c.times_seen > 3 and any(p > 0.7 for _, p in c.probable_causes)
        ]

        for corr in strong_correlations:
            top_cause, prob = max(corr.probable_causes, key=lambda x: x[1])
            insights.append(NetworkInsight(
                insight_id=f"ins_corr_{id(corr)}",
                created_at=datetime.now(),
                category="diagnostics",
                insight=f"Strong correlation: '{corr.symptom_description}' often caused by '{top_cause}'",
                supporting_evidence=[
                    f"Observed {corr.times_seen} times",
                    f"Probability: {prob:.0%}"
                ],
                confidence=prob,
                actionable=True,
                suggested_actions=corr.resolution_history[:2] or ["Apply learned resolution"]
            ))

        self.insights = insights
        return insights

    # ==================== HELPERS ====================

    def _ljpw_distance(self, a: List[float], b: List[float]) -> float:
        """Calculate Euclidean distance between LJPW signatures"""
        return math.sqrt(sum((a[i] - b[i])**2 for i in range(4)))

    def get_wisdom_summary(self) -> Dict:
        """Get summary of accumulated wisdom"""
        return {
            'patterns_learned': len(self.patterns),
            'baselines_tracked': len(self.baselines),
            'correlations_learned': len(self.correlations),
            'total_observations': sum(len(h) for h in self.history.values()),
            'insights_available': len(self.insights),
            'storage_path': str(self.storage_path)
        }

    def export_wisdom(self, path: str):
        """Export all wisdom to a file"""
        wisdom = {
            'patterns': {pid: {
                **asdict(p),
                'pattern_type': p.pattern_type.value,
                'last_seen': p.last_seen.isoformat()
            } for pid, p in self.patterns.items()},
            'baselines': {t: {
                **asdict(b),
                'last_updated': b.last_updated.isoformat()
            } for t, b in self.baselines.items()},
            'correlations': {cid: asdict(c) for cid, c in self.correlations.items()},
            'summary': self.get_wisdom_summary()
        }

        with open(path, 'w') as f:
            json.dump(wisdom, f, indent=2)

    def import_wisdom(self, path: str):
        """Import wisdom from another instance"""
        with open(path) as f:
            wisdom = json.load(f)

        # Merge patterns (keep higher frequency)
        for pid, pdata in wisdom.get('patterns', {}).items():
            pdata['pattern_type'] = PatternType(pdata['pattern_type'])
            pdata['last_seen'] = datetime.fromisoformat(pdata['last_seen'])
            pattern = SemanticPattern(**pdata)

            if pid not in self.patterns or pattern.frequency > self.patterns[pid].frequency:
                self.patterns[pid] = pattern

        # Merge baselines (keep more samples)
        for target, bdata in wisdom.get('baselines', {}).items():
            bdata['last_updated'] = datetime.fromisoformat(bdata['last_updated'])
            baseline = Baseline(**bdata)

            if target not in self.baselines or baseline.samples > self.baselines[target].samples:
                self.baselines[target] = baseline

        # Merge correlations
        for cid, cdata in wisdom.get('correlations', {}).items():
            if cid not in self.correlations:
                self.correlations[cid] = RootCauseCorrelation(**cdata)

        self._save_wisdom()
