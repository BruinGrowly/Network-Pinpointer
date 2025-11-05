#!/usr/bin/env python3
"""
Root Cause Analyzer - Prioritizes issues and provides actionable recommendations

Takes diagnostic results and determines:
1. What's wrong (root cause)
2. How bad is it (severity)
3. What to fix first (priority)
4. How to fix it (recommendations)
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum

from .semantic_engine import Coordinates
from .cli_output import get_formatter, Symbols


class Severity(Enum):
    """Issue severity levels"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


@dataclass
class Issue:
    """A diagnosed network issue"""
    title: str
    description: str
    severity: Severity
    dimension: str  # Which LJPW dimension
    impact_percentage: float  # Estimated % of total problem
    confidence: float  # How confident are we (0-1)
    evidence: List[str]  # What led to this conclusion
    recommendations: List[str]  # How to fix


@dataclass
class RootCauseAnalysis:
    """Complete root cause analysis"""
    primary_issue: Issue
    secondary_issues: List[Issue]
    all_issues: List[Issue]
    coordinates: Coordinates
    overall_health: float
    fix_order: List[str]  # Ordered list of what to fix


class RootCauseAnalyzer:
    """Analyzes diagnostic results to find root causes"""

    def __init__(self):
        self.fmt = get_formatter()

    def analyze(
        self,
        coords: Coordinates,
        metadata: Optional[Dict] = None
    ) -> RootCauseAnalysis:
        """
        Analyze LJPW coordinates and metadata to find root causes

        Args:
            coords: LJPW coordinates from diagnostics
            metadata: Additional diagnostic metadata (TTL, loss, etc.)

        Returns:
            Complete root cause analysis with prioritized issues
        """
        metadata = metadata or {}
        issues = []

        # Analyze each dimension
        issues.extend(self._analyze_love_dimension(coords.love, metadata))
        issues.extend(self._analyze_justice_dimension(coords.justice, metadata))
        issues.extend(self._analyze_power_dimension(coords.power, metadata))
        issues.extend(self._analyze_wisdom_dimension(coords.wisdom, metadata))

        # Sort by severity and impact
        issues.sort(key=lambda i: (
            self._severity_weight(i.severity),
            -i.impact_percentage,
            -i.confidence
        ))

        # Calculate overall health
        health = (coords.love + coords.justice + coords.power + coords.wisdom) / 4

        # Identify primary and secondary issues
        primary = issues[0] if issues else None
        secondary = issues[1:3] if len(issues) > 1 else []

        # Determine fix order
        fix_order = self._determine_fix_order(issues, coords)

        return RootCauseAnalysis(
            primary_issue=primary,
            secondary_issues=secondary,
            all_issues=issues,
            coordinates=coords,
            overall_health=health,
            fix_order=fix_order
        )

    def _severity_weight(self, severity: Severity) -> int:
        """Convert severity to numeric weight for sorting"""
        weights = {
            Severity.CRITICAL: 0,
            Severity.HIGH: 1,
            Severity.MEDIUM: 2,
            Severity.LOW: 3,
            Severity.INFO: 4
        }
        return weights.get(severity, 5)

    def _analyze_love_dimension(
        self,
        love: float,
        metadata: Dict
    ) -> List[Issue]:
        """Analyze Love dimension for connectivity issues"""
        issues = []

        if love < 0.3:
            # Critical connectivity problem
            evidence = ["Love dimension critically low"]
            recommendations = []

            # Determine specific cause
            packet_loss = metadata.get("packet_loss", 0)
            ttl = metadata.get("avg_ttl", 64)

            if packet_loss > 0.5:
                evidence.append(f"Heavy packet loss: {packet_loss*100:.0f}%")
                recommendations.append("Check physical link quality")
                recommendations.append("Verify network interface status")
                recommendations.append("Check for congestion or QoS policies")
            elif ttl == 0:
                evidence.append("No response from target")
                recommendations.append("Verify target is reachable")
                recommendations.append("Check routing table")
                recommendations.append("Verify firewall rules")
            else:
                evidence.append("Connection severely degraded")
                recommendations.append("Check network topology")
                recommendations.append("Verify routing configuration")

            issues.append(Issue(
                title="Critical Connectivity Failure",
                description="Network connectivity is critically impaired",
                severity=Severity.CRITICAL,
                dimension="Love",
                impact_percentage=70.0,
                confidence=0.95,
                evidence=evidence,
                recommendations=recommendations
            ))

        elif love < 0.5:
            # Significant connectivity issue
            packet_loss = metadata.get("packet_loss", 0)

            evidence = [f"Love dimension low: {love:.2f}"]
            if packet_loss > 0:
                evidence.append(f"Packet loss detected: {packet_loss*100:.0f}%")

            issues.append(Issue(
                title="Connectivity Problems",
                description="Network connectivity is degraded but functional",
                severity=Severity.HIGH,
                dimension="Love",
                impact_percentage=40.0,
                confidence=0.85,
                evidence=evidence,
                recommendations=[
                    "Investigate packet loss patterns",
                    "Check link quality and utilization",
                    "Verify no routing loops exist"
                ]
            ))

        elif love < 0.7:
            # Minor connectivity issue
            issues.append(Issue(
                title="Suboptimal Connectivity",
                description="Connectivity could be improved",
                severity=Severity.MEDIUM,
                dimension="Love",
                impact_percentage=20.0,
                confidence=0.70,
                evidence=[f"Love dimension: {love:.2f}"],
                recommendations=[
                    "Monitor for degradation trends",
                    "Consider optimizing routing"
                ]
            ))

        return issues

    def _analyze_justice_dimension(
        self,
        justice: float,
        metadata: Dict
    ) -> List[Issue]:
        """Analyze Justice dimension for policy/routing issues"""
        issues = []

        if justice > 0.7:
            # Over-securitization or excessive policy
            evidence = [f"Justice dimension elevated: {justice:.2f}"]

            route_changing = metadata.get("route_changing", False)
            ttl_variance = metadata.get("ttl_variance", 0)

            if route_changing or ttl_variance > 2:
                evidence.append(f"Route instability detected (TTL variance: {ttl_variance:.1f})")
                severity = Severity.HIGH
                recommendations = [
                    "Check BGP routing stability",
                    "Verify routing protocol configuration",
                    "Investigate if load balancing is intentional"
                ]
            else:
                evidence.append("High policy enforcement detected")
                severity = Severity.MEDIUM
                recommendations = [
                    "Audit firewall rules for over-restriction",
                    "Review security policies",
                    "Ensure legitimate traffic isn't blocked"
                ]

            issues.append(Issue(
                title="Excessive Policy Enforcement" if not route_changing else "Route Instability",
                description="Justice dimension indicates active policy enforcement or routing changes",
                severity=severity,
                dimension="Justice",
                impact_percentage=30.0,
                confidence=0.80,
                evidence=evidence,
                recommendations=recommendations
            ))

        elif justice < 0.2:
            # Possibly under-secured
            issues.append(Issue(
                title="Minimal Security Enforcement",
                description="Very low Justice may indicate insufficient security",
                severity=Severity.INFO,
                dimension="Justice",
                impact_percentage=5.0,
                confidence=0.60,
                evidence=[f"Justice dimension very low: {justice:.2f}"],
                recommendations=[
                    "Verify security policies are in place",
                    "Consider if additional access controls needed"
                ]
            ))

        return issues

    def _analyze_power_dimension(
        self,
        power: float,
        metadata: Dict
    ) -> List[Issue]:
        """Analyze Power dimension for performance issues"""
        issues = []

        if power < 0.3:
            # Critical performance problem
            evidence = [f"Power dimension critically low: {power:.2f}"]

            avg_hops = metadata.get("avg_hops", 0)
            path_complexity = metadata.get("path_complexity", "unknown")

            if avg_hops > 20 or path_complexity == "extreme":
                evidence.append(f"Extremely complex path ({avg_hops:.0f} hops)")
                recommendations = [
                    "Path is sub-optimal - investigate routing",
                    "Consider direct peering if possible",
                    "Check for routing loops",
                    "Evaluate CDN or caching solutions"
                ]
                impact = 60.0
            else:
                evidence.append("Severe performance degradation")
                recommendations = [
                    "Check for congestion",
                    "Verify link capacity",
                    "Investigate QoS settings",
                    "Consider bandwidth upgrade"
                ]
                impact = 50.0

            issues.append(Issue(
                title="Critical Performance Degradation",
                description="Network performance is severely limited",
                severity=Severity.CRITICAL,
                dimension="Power",
                impact_percentage=impact,
                confidence=0.90,
                evidence=evidence,
                recommendations=recommendations
            ))

        elif power < 0.5:
            # Significant performance issue
            issues.append(Issue(
                title="Performance Problems",
                description="Network performance is below expected levels",
                severity=Severity.HIGH,
                dimension="Power",
                impact_percentage=35.0,
                confidence=0.80,
                evidence=[f"Power dimension low: {power:.2f}"],
                recommendations=[
                    "Analyze path complexity and latency",
                    "Check for bandwidth saturation",
                    "Review QoS policies",
                    "Monitor for peak usage patterns"
                ]
            ))

        elif power < 0.7:
            # Minor performance issue
            issues.append(Issue(
                title="Suboptimal Performance",
                description="Performance could be improved",
                severity=Severity.MEDIUM,
                dimension="Power",
                impact_percentage=25.0,
                confidence=0.70,
                evidence=[f"Power dimension: {power:.2f}"],
                recommendations=[
                    "Monitor performance trends",
                    "Consider optimization opportunities"
                ]
            ))

        return issues

    def _analyze_wisdom_dimension(
        self,
        wisdom: float,
        metadata: Dict
    ) -> List[Issue]:
        """Analyze Wisdom dimension for visibility issues"""
        issues = []

        if wisdom < 0.4:
            # Poor visibility
            loss_pattern = metadata.get("loss_pattern", "none")
            packet_loss = metadata.get("packet_loss", 0)

            evidence = [f"Wisdom dimension low: {wisdom:.2f}"]

            if packet_loss > 0.3:
                evidence.append(f"High packet loss reduces visibility ({packet_loss*100:.0f}%)")
                severity = Severity.HIGH
                impact = 30.0
            else:
                evidence.append("Limited network visibility")
                severity = Severity.MEDIUM
                impact = 15.0

            issues.append(Issue(
                title="Poor Network Visibility",
                description="Limited visibility into network state",
                severity=severity,
                dimension="Wisdom",
                impact_percentage=impact,
                confidence=0.75,
                evidence=evidence,
                recommendations=[
                    "Improve monitoring coverage",
                    "Add visibility tools (NetFlow, SNMP)",
                    "Investigate packet loss sources",
                    "Ensure logging is enabled"
                ]
            ))

        elif wisdom < 0.6:
            # Some visibility gaps
            issues.append(Issue(
                title="Visibility Gaps",
                description="Some blind spots in network monitoring",
                severity=Severity.LOW,
                dimension="Wisdom",
                impact_percentage=10.0,
                confidence=0.65,
                evidence=[f"Wisdom dimension: {wisdom:.2f}"],
                recommendations=[
                    "Enhance monitoring for key components",
                    "Consider additional visibility tools"
                ]
            ))

        return issues

    def _determine_fix_order(
        self,
        issues: List[Issue],
        coords: Coordinates
    ) -> List[str]:
        """
        Determine optimal order to fix issues

        Uses dependency logic:
        - Fix critical issues first
        - Fix issues that might resolve others
        - Love/Power before Justice (restore connectivity before security)
        """
        order = []

        # Group by dimension
        by_dimension = {
            "Love": [],
            "Justice": [],
            "Power": [],
            "Wisdom": []
        }

        for issue in issues:
            if issue.severity in [Severity.CRITICAL, Severity.HIGH]:
                by_dimension[issue.dimension].append(issue)

        # Fix order logic:
        # 1. Critical Love issues (can't connect at all)
        # 2. Critical Power issues (too slow to be usable)
        # 3. Justice issues (might be blocking legitimate traffic)
        # 4. Remaining issues

        for issue in by_dimension["Love"]:
            if issue.severity == Severity.CRITICAL:
                order.append(f"Fix {issue.title} (restores connectivity)")

        for issue in by_dimension["Power"]:
            if issue.severity == Severity.CRITICAL:
                order.append(f"Fix {issue.title} (restores performance)")

        for issue in by_dimension["Justice"]:
            if issue.severity in [Severity.CRITICAL, Severity.HIGH]:
                order.append(f"Address {issue.title} (may unblock traffic)")

        for issue in by_dimension["Love"]:
            if issue.severity == Severity.HIGH:
                order.append(f"Improve {issue.title}")

        for issue in by_dimension["Power"]:
            if issue.severity == Severity.HIGH:
                order.append(f"Optimize {issue.title}")

        for issue in by_dimension["Wisdom"]:
            if issue.severity == Severity.HIGH:
                order.append(f"Enhance {issue.title}")

        return order

    def display_analysis(self, analysis: RootCauseAnalysis) -> str:
        """Display root cause analysis in formatted output"""
        lines = []

        lines.append(self.fmt.section_header("ROOT CAUSE ANALYSIS"))

        # Overall health
        lines.append("")
        lines.append(self.fmt.health_score_display(analysis.overall_health))

        # Primary issue
        if analysis.primary_issue:
            lines.append(self.fmt.subsection_header("PRIMARY ISSUE (Fix First)"))
            lines.append(self._format_issue(analysis.primary_issue, is_primary=True))

        # Secondary issues
        if analysis.secondary_issues:
            lines.append(self.fmt.subsection_header("SECONDARY ISSUES (Fix Soon)"))
            for issue in analysis.secondary_issues:
                lines.append(self._format_issue(issue, is_primary=False))
                lines.append("")

        # Fix order
        if analysis.fix_order:
            lines.append(self.fmt.subsection_header("RECOMMENDED FIX ORDER"))
            lines.append(self.fmt.numbered_list(analysis.fix_order))

        # All issues summary
        if len(analysis.all_issues) > 3:
            lines.append(self.fmt.subsection_header("ALL ISSUES SUMMARY"))
            severity_counts = {}
            for issue in analysis.all_issues:
                severity_counts[issue.severity.value] = severity_counts.get(issue.severity.value, 0) + 1

            for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
                count = severity_counts.get(severity.value, 0)
                if count > 0:
                    lines.append(f"  {self.fmt.priority_indicator(severity.value)}: {count} issue(s)")

        return "\n".join(lines)

    def _format_issue(self, issue: Issue, is_primary: bool = False) -> str:
        """Format a single issue for display"""
        lines = []

        # Title with priority
        title_line = f"{self.fmt.priority_indicator(issue.severity.value)} {self.fmt.bold(issue.title)}"
        lines.append(title_line)

        # Description
        lines.append(f"   {issue.description}")

        # Impact
        impact_str = f"Impact: {issue.impact_percentage:.0f}% of total problem"
        confidence_str = f"Confidence: {issue.confidence*100:.0f}%"
        lines.append(f"   {self.fmt.dim(f'{impact_str} | {confidence_str}')}")

        # Evidence
        if issue.evidence:
            lines.append(f"\n   {self.fmt.bold('Evidence:')}")
            for evidence in issue.evidence:
                lines.append(f"     {Symbols.BULLET} {evidence}")

        # Recommendations
        if issue.recommendations:
            lines.append(f"\n   {self.fmt.bold('How to Fix:')}")
            for i, rec in enumerate(issue.recommendations, 1):
                lines.append(f"     {i}. {rec}")

        return "\n".join(lines)


if __name__ == "__main__":
    # Demo root cause analysis
    from .semantic_engine import Coordinates

    analyzer = RootCauseAnalyzer()

    # Scenario: Over-secured network with connectivity problems
    coords = Coordinates(love=0.25, justice=0.75, power=0.55, wisdom=0.60)
    metadata = {
        "packet_loss": 0.15,
        "route_changing": True,
        "ttl_variance": 3.5,
        "avg_hops": 12
    }

    analysis = analyzer.analyze(coords, metadata)
    print(analyzer.display_analysis(analysis))
