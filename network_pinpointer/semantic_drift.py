#!/usr/bin/env python3
"""
Semantic Drift Detection - Detect Configuration Drift and Compromises

Analyzes semantic drift from baseline profiles to detect:
- Configuration changes
- Security incidents
- Performance degradation
- Architectural drift
"""

import math
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Tuple

from .semantic_storage import SemanticDatabase
from .semantic_probe import SemanticProfile
from .semantic_engine import Coordinates


@dataclass
class DriftAnalysis:
    """Analysis of semantic drift from baseline"""
    target: str
    baseline_timestamp: datetime
    current_timestamp: datetime
    drift_magnitude: float  # 0.0-2.0 (Euclidean distance)
    drift_percentage: float  # 0-100%
    drift_type: str
    affected_dimensions: List[Tuple[str, float, float]]  # (dimension, old, new)
    severity: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    description: str
    possible_causes: List[str]
    recommendations: List[str]
    
    # Coordinate changes
    baseline_coords: Coordinates
    current_coords: Coordinates
    
    # Archetype changes
    baseline_archetype: Optional[str] = None
    current_archetype: Optional[str] = None
    archetype_changed: bool = False
    
    # Security changes
    baseline_security: Optional[str] = None
    current_security: Optional[str] = None
    security_degraded: bool = False


class SemanticDriftDetector:
    """Detects and analyzes semantic drift from baselines"""
    
    # Thresholds for drift classification
    DRIFT_THRESHOLDS = {
        'LOW': 0.1,
        'MEDIUM': 0.2,
        'HIGH': 0.35,
        'CRITICAL': 0.5,
    }
    
    def __init__(self, db: SemanticDatabase):
        self.db = db
    
    def analyze_drift(
        self, 
        target: str, 
        current_profile: SemanticProfile = None
    ) -> Optional[DriftAnalysis]:
        """
        Analyze drift from baseline.
        
        Args:
            target: Target to analyze
            current_profile: Current profile (if None, fetches latest from DB)
        
        Returns:
            DriftAnalysis or None if no baseline exists
        """
        # Get baseline
        baseline_dict = self.db.get_baseline(target)
        if not baseline_dict:
            return None  # No baseline set
        
        # Get current profile
        if current_profile is None:
            current_dict = self.db.get_profile(target)
            if not current_dict:
                return None  # No current profile
        else:
            # Convert SemanticProfile to dict-like structure
            current_dict = self._profile_to_dict(current_profile)
        
        # Extract coordinates
        baseline_coords = self.db.dict_to_coordinates(baseline_dict)
        current_coords = self.db.dict_to_coordinates(current_dict)
        
        if not baseline_coords or not current_coords:
            return None
        
        # Calculate drift magnitude
        drift_magnitude = self._calculate_drift_magnitude(baseline_coords, current_coords)
        drift_percentage = (drift_magnitude / 2.0) * 100  # Normalize to 0-100%
        
        # Identify affected dimensions
        affected = self._identify_affected_dimensions(baseline_coords, current_coords)
        
        # Classify drift type
        drift_type = self._classify_drift_type(baseline_dict, current_dict, affected)
        
        # Determine severity
        severity = self._determine_severity(drift_magnitude)
        
        # Check archetype change
        baseline_archetype = baseline_dict.get('archetype')
        current_archetype = current_dict.get('archetype')
        archetype_changed = baseline_archetype != current_archetype
        
        # Check security degradation
        baseline_security = baseline_dict.get('security_posture')
        current_security = current_dict.get('security_posture')
        security_degraded = self._is_security_degraded(baseline_security, current_security)
        
        # Generate description
        description = self._generate_description(
            drift_type, affected, archetype_changed, security_degraded
        )
        
        # Identify possible causes
        possible_causes = self._identify_possible_causes(
            drift_type, affected, archetype_changed
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            drift_type, affected, severity, security_degraded
        )
        
        return DriftAnalysis(
            target=target,
            baseline_timestamp=datetime.fromisoformat(baseline_dict['timestamp']),
            current_timestamp=datetime.fromisoformat(current_dict['timestamp']),
            drift_magnitude=drift_magnitude,
            drift_percentage=drift_percentage,
            drift_type=drift_type,
            affected_dimensions=affected,
            severity=severity,
            description=description,
            possible_causes=possible_causes,
            recommendations=recommendations,
            baseline_coords=baseline_coords,
            current_coords=current_coords,
            baseline_archetype=baseline_archetype,
            current_archetype=current_archetype,
            archetype_changed=archetype_changed,
            baseline_security=baseline_security,
            current_security=current_security,
            security_degraded=security_degraded,
        )
    
    def check_all_targets(self) -> List[DriftAnalysis]:
        """Check drift for all targets with baselines"""
        targets = self.db.get_targets_with_baselines()
        results = []
        
        for target in targets:
            analysis = self.analyze_drift(target)
            if analysis and analysis.drift_magnitude > 0.05:  # Only report significant drift
                results.append(analysis)
        
        # Sort by severity and magnitude
        severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        results.sort(key=lambda x: (severity_order.get(x.severity, 4), -x.drift_magnitude))
        
        return results
    
    def _calculate_drift_magnitude(self, baseline: Coordinates, current: Coordinates) -> float:
        """Calculate Euclidean distance between coordinates"""
        return math.sqrt(
            (baseline.love - current.love) ** 2 +
            (baseline.justice - current.justice) ** 2 +
            (baseline.power - current.power) ** 2 +
            (baseline.wisdom - current.wisdom) ** 2
        )
    
    def _identify_affected_dimensions(
        self, 
        baseline: Coordinates, 
        current: Coordinates
    ) -> List[Tuple[str, float, float]]:
        """Identify which dimensions changed significantly"""
        affected = []
        threshold = 0.1  # 10% change is significant
        
        dims = [
            ('Love', baseline.love, current.love),
            ('Justice', baseline.justice, current.justice),
            ('Power', baseline.power, current.power),
            ('Wisdom', baseline.wisdom, current.wisdom),
        ]
        
        for name, old_val, new_val in dims:
            if abs(old_val - new_val) >= threshold:
                affected.append((name, old_val, new_val))
        
        # Sort by magnitude of change
        affected.sort(key=lambda x: abs(x[2] - x[1]), reverse=True)
        
        return affected
    
    def _classify_drift_type(
        self, 
        baseline: Dict, 
        current: Dict, 
        affected: List[Tuple[str, float, float]]
    ) -> str:
        """Classify the type of drift"""
        # Dominant dimension changed
        if baseline.get('dominant_dimension') != current.get('dominant_dimension'):
            return "dimension_shift"
        
        # Archetype changed
        if baseline.get('archetype') != current.get('archetype'):
            return "archetype_change"
        
        # Security posture changed
        if baseline.get('security_posture') != current.get('security_posture'):
            return "security_change"
        
        # Harmony degraded significantly
        baseline_harmony = baseline.get('harmony_score', 0)
        current_harmony = current.get('harmony_score', 0)
        if baseline_harmony - current_harmony > 0.2:
            return "harmony_degradation"
        
        # Service classification changed
        if baseline.get('service_classification') != current.get('service_classification'):
            return "service_change"
        
        # Multiple dimensions affected
        if len(affected) >= 3:
            return "major_reconfiguration"
        
        # Single dimension drift
        if len(affected) == 1:
            return f"{affected[0][0].lower()}_drift"
        
        return "gradual_drift"
    
    def _determine_severity(self, drift_magnitude: float) -> str:
        """Determine severity based on drift magnitude"""
        if drift_magnitude >= self.DRIFT_THRESHOLDS['CRITICAL']:
            return "CRITICAL"
        elif drift_magnitude >= self.DRIFT_THRESHOLDS['HIGH']:
            return "HIGH"
        elif drift_magnitude >= self.DRIFT_THRESHOLDS['MEDIUM']:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _is_security_degraded(self, baseline: str, current: str) -> bool:
        """Check if security posture degraded"""
        security_levels = {
            'VERY_SECURE': 5,
            'SECURE': 4,
            'BALANCED': 3,
            'MODERATE': 2,
            'OPEN': 1,
            'POTENTIALLY_VULNERABLE': 0,
        }
        
        baseline_level = security_levels.get(baseline, 3)
        current_level = security_levels.get(current, 3)
        
        return current_level < baseline_level
    
    def _generate_description(
        self, 
        drift_type: str, 
        affected: List[Tuple[str, float, float]],
        archetype_changed: bool,
        security_degraded: bool
    ) -> str:
        """Generate human-readable description"""
        descriptions = {
            'dimension_shift': "System's dominant dimension has changed",
            'archetype_change': "System's archetype has changed",
            'security_change': "Security posture has changed",
            'harmony_degradation': "Overall harmony has degraded significantly",
            'service_change': "Service classification has changed",
            'major_reconfiguration': "Major reconfiguration detected across multiple dimensions",
            'gradual_drift': "Gradual drift from baseline",
        }
        
        base_desc = descriptions.get(drift_type, "Semantic drift detected")
        
        if affected:
            dim_changes = ", ".join([
                f"{name} {'+' if new > old else ''}{new-old:.2f}"
                for name, old, new in affected[:2]
            ])
            base_desc += f" ({dim_changes})"
        
        if security_degraded:
            base_desc += " - Security degraded!"
        
        return base_desc
    
    def _identify_possible_causes(
        self, 
        drift_type: str, 
        affected: List[Tuple[str, float, float]],
        archetype_changed: bool
    ) -> List[str]:
        """Identify possible causes of drift"""
        causes = []
        
        if drift_type == "dimension_shift":
            causes.append("Configuration change altered system's primary purpose")
            causes.append("New services added or removed")
            causes.append("Firewall rules modified")
        
        if drift_type == "archetype_change":
            causes.append("System role changed (e.g., web server → database)")
            causes.append("Major architectural change")
            causes.append("Possible security incident or compromise")
        
        if drift_type == "security_change":
            causes.append("Security policies updated")
            causes.append("Firewall configuration changed")
            causes.append("Access controls modified")
        
        if drift_type == "harmony_degradation":
            causes.append("Configuration drift over time")
            causes.append("Conflicting changes applied")
            causes.append("System instability")
        
        # Dimension-specific causes
        for name, old, new in affected:
            if name == "Love" and new < old:
                causes.append("Connectivity reduced (ports closed, services stopped)")
            elif name == "Love" and new > old:
                causes.append("New services exposed or connectivity increased")
            
            if name == "Justice" and new < old:
                causes.append("Security controls relaxed")
            elif name == "Justice" and new > old:
                causes.append("Security hardening applied")
            
            if name == "Power" and new < old:
                causes.append("Performance degradation or resource constraints")
            elif name == "Power" and new > old:
                causes.append("Performance optimization or resource increase")
        
        return list(set(causes))  # Remove duplicates
    
    def _generate_recommendations(
        self, 
        drift_type: str, 
        affected: List[Tuple[str, float, float]],
        severity: str,
        security_degraded: bool
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Always recommend verification
        recommendations.append("Verify this change was intentional and authorized")
        
        if severity in ["HIGH", "CRITICAL"]:
            recommendations.append("Investigate immediately - significant drift detected")
            recommendations.append("Review recent configuration changes")
            recommendations.append("Check system logs for anomalies")
        
        if security_degraded:
            recommendations.append("⚠️  Security posture degraded - review security controls")
            recommendations.append("Audit access controls and firewall rules")
        
        if drift_type == "archetype_change":
            recommendations.append("Update documentation to reflect new system role")
            recommendations.append("Consider setting new baseline if change is permanent")
        
        if drift_type == "harmony_degradation":
            recommendations.append("Review configuration for conflicts or errors")
            recommendations.append("Consider rolling back recent changes")
        
        # Dimension-specific recommendations
        for name, old, new in affected:
            if name == "Love" and new < old - 0.2:
                recommendations.append("Investigate connectivity loss - services may be unavailable")
            
            if name == "Justice" and new < old - 0.2:
                recommendations.append("Security controls weakened - review security posture")
            
            if name == "Power" and new < old - 0.2:
                recommendations.append("Performance degraded - check resource utilization")
        
        # General recommendations
        if severity == "LOW":
            recommendations.append("Monitor for continued drift")
            recommendations.append("Update baseline if this is the new normal")
        
        return recommendations
    
    def _profile_to_dict(self, profile: SemanticProfile) -> Dict:
        """Convert SemanticProfile to dict for comparison"""
        archetype_name = None
        if profile.matched_archetypes:
            archetype_name = profile.matched_archetypes[0][0].name
        
        return {
            'target': profile.target,
            'timestamp': profile.timestamp.isoformat(),
            'love': profile.ljpw_coordinates.love if profile.ljpw_coordinates else 0,
            'justice': profile.ljpw_coordinates.justice if profile.ljpw_coordinates else 0,
            'power': profile.ljpw_coordinates.power if profile.ljpw_coordinates else 0,
            'wisdom': profile.ljpw_coordinates.wisdom if profile.ljpw_coordinates else 0,
            'dominant_dimension': profile.dominant_dimension,
            'harmony_score': profile.harmony_score,
            'archetype': archetype_name,
            'security_posture': profile.security_posture,
            'service_classification': profile.service_classification,
        }
