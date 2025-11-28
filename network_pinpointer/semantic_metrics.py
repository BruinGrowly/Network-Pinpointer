#!/usr/bin/env python3
"""
Semantic Metrics - Dimensional Combinations and Derived Insights

Combines LJPW dimensions to reveal deeper semantic patterns:
- Two-dimension combinations (L+J, P+W, etc.)
- Three-dimension combinations (L+J+P, etc.)
- Ratios and relationships (L/J, P/W, etc.)
- Dangerous pattern detection
- Domain-specific scores
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from enum import Enum

from .semantic_engine import Coordinates


class MetricCategory(Enum):
    """Categories of semantic metrics"""
    SERVICE_QUALITY = "service_quality"
    SECURITY = "security"
    PERFORMANCE = "performance"
    OBSERVABILITY = "observability"
    BALANCE = "balance"
    RISK = "risk"


@dataclass
class SemanticMetric:
    """A derived semantic metric"""
    name: str
    value: float
    category: MetricCategory
    interpretation: str
    grade: str  # A, B, C, D, F
    threshold_low: float = 0.3
    threshold_medium: float = 0.5
    threshold_good: float = 0.7
    threshold_excellent: float = 0.85


@dataclass
class DimensionalCombination:
    """Analysis of a specific dimensional combination"""
    name: str
    formula: str
    value: float
    interpretation: str
    implications: List[str]
    recommendations: List[str]


@dataclass
class PatternWarning:
    """Warning about dangerous dimensional patterns"""
    severity: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    pattern: str
    description: str
    recommendation: str


class SemanticMetrics:
    """Calculate derived metrics from LJPW coordinates"""
    
    def __init__(self, coords: Coordinates):
        self.coords = coords
        self.L = coords.love
        self.J = coords.justice
        self.P = coords.power
        self.W = coords.wisdom
    
    # ==================== TWO-DIMENSION COMBINATIONS ====================
    
    def secure_connectivity(self) -> SemanticMetric:
        """Love + Justice - How well accessibility is balanced with security"""
        value = (self.L + self.J) / 2
        
        if value > 0.85:
            interpretation = "Excellent balance of accessibility and security"
            grade = "A"
        elif value > 0.7:
            interpretation = "Good secure connectivity"
            grade = "B"
        elif value > 0.5:
            interpretation = "Moderate secure connectivity"
            grade = "C"
        elif value > 0.3:
            interpretation = "Weak secure connectivity"
            grade = "D"
        else:
            interpretation = "Poor secure connectivity"
            grade = "F"
        
        return SemanticMetric(
            name="Secure Connectivity (L+J)",
            value=value,
            category=MetricCategory.SECURITY,
            interpretation=interpretation,
            grade=grade
        )
    
    def service_capacity(self) -> SemanticMetric:
        """Love + Power - Ability to deliver services at scale"""
        value = (self.L + self.P) / 2
        
        if value > 0.85:
            interpretation = "Excellent service delivery capacity"
            grade = "A"
        elif value > 0.7:
            interpretation = "Good service capacity"
            grade = "B"
        elif value > 0.5:
            interpretation = "Moderate service capacity"
            grade = "C"
        elif value > 0.3:
            interpretation = "Limited service capacity"
            grade = "D"
        else:
            interpretation = "Poor service capacity"
            grade = "F"
        
        return SemanticMetric(
            name="Service Capacity (L+P)",
            value=value,
            category=MetricCategory.SERVICE_QUALITY,
            interpretation=interpretation,
            grade=grade
        )
    
    def observable_connectivity(self) -> SemanticMetric:
        """Love + Wisdom - How well connectivity is monitored"""
        value = (self.L + self.W) / 2
        
        if value > 0.85:
            interpretation = "Excellent connectivity monitoring"
            grade = "A"
        elif value > 0.7:
            interpretation = "Good connectivity visibility"
            grade = "B"
        elif value > 0.5:
            interpretation = "Moderate connectivity monitoring"
            grade = "C"
        elif value > 0.3:
            interpretation = "Limited connectivity visibility"
            grade = "D"
        else:
            interpretation = "Poor connectivity monitoring - blind spots likely"
            grade = "F"
        
        return SemanticMetric(
            name="Observable Connectivity (L+W)",
            value=value,
            category=MetricCategory.OBSERVABILITY,
            interpretation=interpretation,
            grade=grade
        )
    
    def enforcement_capability(self) -> SemanticMetric:
        """Justice + Power - Ability to enforce policies"""
        value = (self.J + self.P) / 2
        
        if value > 0.85:
            interpretation = "Excellent policy enforcement capability"
            grade = "A"
        elif value > 0.7:
            interpretation = "Good enforcement capability"
            grade = "B"
        elif value > 0.5:
            interpretation = "Moderate enforcement capability"
            grade = "C"
        elif value > 0.3:
            interpretation = "Weak enforcement capability"
            grade = "D"
        else:
            interpretation = "Poor enforcement - policies without teeth"
            grade = "F"
        
        return SemanticMetric(
            name="Enforcement Capability (J+P)",
            value=value,
            category=MetricCategory.SECURITY,
            interpretation=interpretation,
            grade=grade
        )
    
    def security_intelligence(self) -> SemanticMetric:
        """Justice + Wisdom - How well security is monitored"""
        value = (self.J + self.W) / 2
        
        if value > 0.85:
            interpretation = "Excellent security visibility and monitoring"
            grade = "A"
        elif value > 0.7:
            interpretation = "Good security intelligence"
            grade = "B"
        elif value > 0.5:
            interpretation = "Moderate security monitoring"
            grade = "C"
        elif value > 0.3:
            interpretation = "Limited security visibility"
            grade = "D"
        else:
            interpretation = "Poor security monitoring - blind and vulnerable"
            grade = "F"
        
        return SemanticMetric(
            name="Security Intelligence (J+W)",
            value=value,
            category=MetricCategory.SECURITY,
            interpretation=interpretation,
            grade=grade
        )
    
    def intelligent_performance(self) -> SemanticMetric:
        """Power + Wisdom - Performance with observability"""
        value = (self.P + self.W) / 2
        
        if value > 0.85:
            interpretation = "Excellent performance with full observability"
            grade = "A"
        elif value > 0.7:
            interpretation = "Good intelligent performance"
            grade = "B"
        elif value > 0.5:
            interpretation = "Moderate performance observability"
            grade = "C"
        elif value > 0.3:
            interpretation = "Limited performance visibility"
            grade = "D"
        else:
            interpretation = "Poor performance monitoring - flying blind"
            grade = "F"
        
        return SemanticMetric(
            name="Intelligent Performance (P+W)",
            value=value,
            category=MetricCategory.PERFORMANCE,
            interpretation=interpretation,
            grade=grade
        )
    
    # ==================== THREE-DIMENSION COMBINATIONS ====================
    
    def operational_excellence(self) -> SemanticMetric:
        """L+J+P - Accessible, secure, and performant"""
        value = (self.L + self.J + self.P) / 3
        
        if value > 0.85:
            interpretation = "Excellent operational state - production ready"
            grade = "A"
        elif value > 0.7:
            interpretation = "Good operational excellence"
            grade = "B"
        elif value > 0.5:
            interpretation = "Moderate operational state"
            grade = "C"
        elif value > 0.3:
            interpretation = "Operational issues detected"
            grade = "D"
        else:
            interpretation = "Poor operational state - needs attention"
            grade = "F"
        
        return SemanticMetric(
            name="Operational Excellence (L+J+P)",
            value=value,
            category=MetricCategory.SERVICE_QUALITY,
            interpretation=interpretation,
            grade=grade
        )
    
    def governed_connectivity(self) -> SemanticMetric:
        """L+J+W - Accessible, secure, and monitored"""
        value = (self.L + self.J + self.W) / 3
        
        if value > 0.85:
            interpretation = "Excellent governance - well-managed service"
            grade = "A"
        elif value > 0.7:
            interpretation = "Good governance and compliance readiness"
            grade = "B"
        elif value > 0.5:
            interpretation = "Moderate governance"
            grade = "C"
        elif value > 0.3:
            interpretation = "Weak governance"
            grade = "D"
        else:
            interpretation = "Poor governance - ungoverned or chaotic"
            grade = "F"
        
        return SemanticMetric(
            name="Governed Connectivity (L+J+W)",
            value=value,
            category=MetricCategory.SECURITY,
            interpretation=interpretation,
            grade=grade
        )
    
    def service_intelligence(self) -> SemanticMetric:
        """L+P+W - Accessible, performant, and observable"""
        value = (self.L + self.P + self.W) / 3
        
        if value > 0.85:
            interpretation = "Excellent DevOps maturity - smart, scalable service"
            grade = "A"
        elif value > 0.7:
            interpretation = "Good service intelligence"
            grade = "B"
        elif value > 0.5:
            interpretation = "Moderate DevOps readiness"
            grade = "C"
        elif value > 0.3:
            interpretation = "Limited service intelligence"
            grade = "D"
        else:
            interpretation = "Poor service intelligence - dumb or limited"
            grade = "F"
        
        return SemanticMetric(
            name="Service Intelligence (L+P+W)",
            value=value,
            category=MetricCategory.SERVICE_QUALITY,
            interpretation=interpretation,
            grade=grade
        )
    
    def security_operations(self) -> SemanticMetric:
        """J+P+W - Secure, capable, and monitored"""
        value = (self.J + self.P + self.W) / 3
        
        if value > 0.85:
            interpretation = "Excellent security operations maturity"
            grade = "A"
        elif value > 0.7:
            interpretation = "Good security operations"
            grade = "B"
        elif value > 0.5:
            interpretation = "Moderate security maturity"
            grade = "C"
        elif value > 0.3:
            interpretation = "Weak security operations"
            grade = "D"
        else:
            interpretation = "Poor security operations - significant gaps"
            grade = "F"
        
        return SemanticMetric(
            name="Security Operations (J+P+W)",
            value=value,
            category=MetricCategory.SECURITY,
            interpretation=interpretation,
            grade=grade
        )
    
    # ==================== RATIOS AND RELATIONSHIPS ====================
    
    def openness_factor(self) -> SemanticMetric:
        """L/J - Balance between accessibility and security"""
        if self.J < 0.01:
            value = 10.0  # Cap at 10 for very low Justice
            interpretation = "CRITICAL: Extremely open with no security"
            grade = "F"
        else:
            value = min(10.0, self.L / self.J)
            
            if value > 3.0:
                interpretation = "Very open - potentially vulnerable"
                grade = "D"
            elif value > 2.0:
                interpretation = "Open - review security posture"
                grade = "C"
            elif value > 0.5:
                interpretation = "Balanced openness and security"
                grade = "B"
            elif value > 0.3:
                interpretation = "Restricted - may be over-secured"
                grade = "C"
            else:
                interpretation = "Very restricted - verify accessibility requirements"
                grade = "D"
        
        return SemanticMetric(
            name="Openness Factor (L/J)",
            value=value,
            category=MetricCategory.RISK,
            interpretation=interpretation,
            grade=grade,
            threshold_low=0.3,
            threshold_medium=0.5,
            threshold_good=2.0,
            threshold_excellent=3.0
        )
    
    def performance_observability_ratio(self) -> SemanticMetric:
        """P/W - Performance vs monitoring balance"""
        if self.W < 0.01:
            value = 10.0
            interpretation = "CRITICAL: High performance with no monitoring - blind spot"
            grade = "F"
        else:
            value = min(10.0, self.P / self.W)
            
            if value > 3.0:
                interpretation = "Fast but blind - add monitoring"
                grade = "D"
            elif value > 2.0:
                interpretation = "Performance-focused - consider more monitoring"
                grade = "C"
            elif value > 0.5:
                interpretation = "Balanced performance and observability"
                grade = "B"
            elif value > 0.3:
                interpretation = "Well-monitored - may be over-instrumented"
                grade = "C"
            else:
                interpretation = "Heavily monitored - verify performance impact"
                grade = "D"
        
        return SemanticMetric(
            name="Performance/Observability (P/W)",
            value=value,
            category=MetricCategory.PERFORMANCE,
            interpretation=interpretation,
            grade=grade,
            threshold_low=0.3,
            threshold_medium=0.5,
            threshold_good=2.0,
            threshold_excellent=3.0
        )
    
    def service_vs_governance_ratio(self) -> SemanticMetric:
        """(L+P)/(J+W) - Service delivery vs governance balance"""
        denominator = self.J + self.W
        if denominator < 0.01:
            value = 10.0
            interpretation = "CRITICAL: Service without governance"
            grade = "F"
        else:
            value = min(10.0, (self.L + self.P) / denominator)
            
            if value > 3.0:
                interpretation = "Service-first culture - governance may be lacking"
                grade = "C"
            elif value > 1.5:
                interpretation = "Service-focused - good for innovation"
                grade = "B"
            elif value > 0.5:
                interpretation = "Balanced service and governance"
                grade = "A"
            else:
                interpretation = "Governance-first - may slow innovation"
                grade = "C"
        
        return SemanticMetric(
            name="Service/Governance Ratio",
            value=value,
            category=MetricCategory.BALANCE,
            interpretation=interpretation,
            grade=grade,
            threshold_low=0.5,
            threshold_medium=1.0,
            threshold_good=2.0,
            threshold_excellent=3.0
        )
    
    # ==================== PATTERN DETECTION ====================
    
    def detect_dangerous_patterns(self) -> List[PatternWarning]:
        """Detect dangerous dimensional combinations"""
        warnings = []
        
        # High Love, Low Justice - Vulnerable
        if self.L > 0.7 and self.J < 0.2:
            warnings.append(PatternWarning(
                severity="CRITICAL",
                pattern="High Accessibility + Low Security",
                description=f"System is highly accessible (L={self.L:.2f}) but has minimal security (J={self.J:.2f}). This is a critical vulnerability.",
                recommendation="Immediately implement security controls. Add firewall rules, authentication, and access restrictions."
            ))
        elif self.L > 0.6 and self.J < 0.3:
            warnings.append(PatternWarning(
                severity="HIGH",
                pattern="Accessible but Insecure",
                description=f"System is accessible (L={self.L:.2f}) with weak security (J={self.J:.2f}).",
                recommendation="Increase security measures to match accessibility level."
            ))
        
        # High Power, Low Wisdom - Blind Performance
        if self.P > 0.8 and self.W < 0.2:
            warnings.append(PatternWarning(
                severity="HIGH",
                pattern="High Performance + No Monitoring",
                description=f"System has high performance (P={self.P:.2f}) but no monitoring (W={self.W:.2f}). Flying blind.",
                recommendation="Add monitoring, logging, and observability tools immediately."
            ))
        elif self.P > 0.6 and self.W < 0.3:
            warnings.append(PatternWarning(
                severity="MEDIUM",
                pattern="Performance without Observability",
                description=f"Performance-focused (P={self.P:.2f}) with limited monitoring (W={self.W:.2f}).",
                recommendation="Increase observability to match performance requirements."
            ))
        
        # High Love + High Power, Low Justice - Critical Risk
        if self.L + self.P > 1.5 and self.J < 0.2:
            warnings.append(PatternWarning(
                severity="CRITICAL",
                pattern="High-Traffic Service Without Security",
                description=f"High-capacity service (L+P={self.L+self.P:.2f}) with minimal security (J={self.J:.2f}). Maximum risk.",
                recommendation="URGENT: Implement comprehensive security controls before continuing operation."
            ))
        
        # Very High Justice, Very Low Love - Over-Secured
        if self.J > 0.8 and self.L < 0.1:
            warnings.append(PatternWarning(
                severity="MEDIUM",
                pattern="Over-Secured System",
                description=f"Extremely high security (J={self.J:.2f}) with minimal accessibility (L={self.L:.2f}).",
                recommendation="Verify this matches requirements. May be blocking legitimate traffic."
            ))
        
        # All dimensions low - Dead or Dying
        if self.L + self.J + self.P + self.W < 0.8:
            warnings.append(PatternWarning(
                severity="HIGH",
                pattern="Low Activity Across All Dimensions",
                description=f"All dimensions are low (sum={self.L+self.J+self.P+self.W:.2f}). System may be offline or failing.",
                recommendation="Investigate system health. May be offline, misconfigured, or compromised."
            ))
        
        # High variance - Imbalanced
        dims = [self.L, self.J, self.P, self.W]
        variance = sum((d - sum(dims)/4)**2 for d in dims) / 4
        if variance > 0.15:
            warnings.append(PatternWarning(
                severity="LOW",
                pattern="Highly Imbalanced Dimensions",
                description=f"Large variance across dimensions (σ²={variance:.3f}). System is semantically imbalanced.",
                recommendation="Review configuration for semantic coherence. Consider balancing dimensions."
            ))
        
        # Sort by severity
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        warnings.sort(key=lambda w: severity_order.get(w.severity, 4))
        
        return warnings
    
    # ==================== COMPREHENSIVE ANALYSIS ====================
    
    def get_all_metrics(self) -> Dict[str, SemanticMetric]:
        """Get all calculated metrics"""
        return {
            # Two-dimension
            'secure_connectivity': self.secure_connectivity(),
            'service_capacity': self.service_capacity(),
            'observable_connectivity': self.observable_connectivity(),
            'enforcement_capability': self.enforcement_capability(),
            'security_intelligence': self.security_intelligence(),
            'intelligent_performance': self.intelligent_performance(),
            
            # Three-dimension
            'operational_excellence': self.operational_excellence(),
            'governed_connectivity': self.governed_connectivity(),
            'service_intelligence': self.service_intelligence(),
            'security_operations': self.security_operations(),
            
            # Ratios
            'openness_factor': self.openness_factor(),
            'performance_observability_ratio': self.performance_observability_ratio(),
            'service_vs_governance_ratio': self.service_vs_governance_ratio(),
        }
    
    def get_metrics_by_category(self, category: MetricCategory) -> Dict[str, SemanticMetric]:
        """Get metrics filtered by category"""
        all_metrics = self.get_all_metrics()
        return {
            name: metric 
            for name, metric in all_metrics.items() 
            if metric.category == category
        }
    
    def get_summary(self) -> Dict:
        """Get summary of all metrics and warnings"""
        metrics = self.get_all_metrics()
        warnings = self.detect_dangerous_patterns()
        
        # Calculate average grade
        grade_values = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}
        avg_grade_value = sum(grade_values.get(m.grade, 0) for m in metrics.values()) / len(metrics)
        
        if avg_grade_value >= 3.5:
            overall_grade = 'A'
        elif avg_grade_value >= 2.5:
            overall_grade = 'B'
        elif avg_grade_value >= 1.5:
            overall_grade = 'C'
        elif avg_grade_value >= 0.5:
            overall_grade = 'D'
        else:
            overall_grade = 'F'
        
        return {
            'overall_grade': overall_grade,
            'metrics': metrics,
            'warnings': warnings,
            'critical_warnings': len([w for w in warnings if w.severity == "CRITICAL"]),
            'high_warnings': len([w for w in warnings if w.severity == "HIGH"]),
            'total_warnings': len(warnings),
        }
