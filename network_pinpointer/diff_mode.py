#!/usr/bin/env python3
"""
Diff/Comparison Mode - Compare network states over time

Supports:
- Before/after comparisons
- Historical comparisons
- Drift detection
- Trend analysis
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

from .semantic_engine import Coordinates
from .cli_output import get_formatter, Colors


@dataclass
class StateChange:
    """Represents a change in network state"""
    dimension: str
    before: float
    after: float
    change: float
    change_pct: float
    severity: str  # MAJOR, SIGNIFICANT, MINOR, NONE


class DiffAnalyzer:
    """Analyze differences between network states"""

    def __init__(self):
        self.fmt = get_formatter()

    def compare_states(
        self,
        before: Coordinates,
        after: Coordinates,
        before_label: str = "Before",
        after_label: str = "After"
    ) -> Dict:
        """
        Compare two network states

        Returns analysis with:
        - Changes in each dimension
        - Overall drift
        - Severity assessment
        - Likely causes
        """

        changes = {
            "love": StateChange(
                dimension="Love",
                before=before.love,
                after=after.love,
                change=after.love - before.love,
                change_pct=((after.love - before.love) / before.love * 100) if before.love > 0 else 0,
                severity=self._assess_severity(before.love, after.love)
            ),
            "justice": StateChange(
                dimension="Justice",
                before=before.justice,
                after=after.justice,
                change=after.justice - before.justice,
                change_pct=((after.justice - before.justice) / before.justice * 100) if before.justice > 0 else 0,
                severity=self._assess_severity(before.justice, after.justice)
            ),
            "power": StateChange(
                dimension="Power",
                before=before.power,
                after=after.power,
                change=after.power - before.power,
                change_pct=((after.power - before.power) / before.power * 100) if before.power > 0 else 0,
                severity=self._assess_severity(before.power, after.power)
            ),
            "wisdom": StateChange(
                dimension="Wisdom",
                before=before.wisdom,
                after=after.wisdom,
                change=after.wisdom - before.wisdom,
                change_pct=((after.wisdom - before.wisdom) / before.wisdom * 100) if before.wisdom > 0 else 0,
                severity=self._assess_severity(before.wisdom, after.wisdom)
            )
        }

        # Overall drift magnitude
        total_drift = sum(abs(c.change) for c in changes.values())

        # Identify major changes
        major_changes = [c for c in changes.values() if c.severity in ["MAJOR", "SIGNIFICANT"]]

        # Determine likely causes
        causes = self._infer_causes(changes)

        return {
            "before_label": before_label,
            "after_label": after_label,
            "changes": changes,
            "total_drift": total_drift,
            "major_changes": major_changes,
            "likely_causes": causes,
            "overall_assessment": self._assess_overall(changes, total_drift)
        }

    def _assess_severity(self, before: float, after: float) -> str:
        """Assess severity of change"""
        if before == 0:
            return "NONE"

        change_pct = abs((after - before) / before * 100)

        if change_pct > 50:
            return "MAJOR"
        elif change_pct > 25:
            return "SIGNIFICANT"
        elif change_pct > 10:
            return "MINOR"
        else:
            return "NONE"

    def _infer_causes(self, changes: Dict[str, StateChange]) -> List[str]:
        """Infer likely causes of changes"""
        causes = []

        love = changes["love"]
        justice = changes["justice"]
        power = changes["power"]
        wisdom = changes["wisdom"]

        # Pattern: Love down + Justice up = Over-securitization
        if love.change < -0.15 and justice.change > 0.15:
            causes.append("Network may have been over-secured (new firewall rules?)")

        # Pattern: Power down + path complexity
        if power.change < -0.2:
            causes.append("Performance degraded (increased latency or complexity)")

        # Pattern: Love + Power both down
        if love.change < -0.15 and power.change < -0.15:
            causes.append("Network connectivity and performance both impacted (infrastructure issue?)")

        # Pattern: Justice changing significantly
        if abs(justice.change) > 0.2:
            if justice.change > 0:
                causes.append("Increased security/policy enforcement")
            else:
                causes.append("Reduced security/policy enforcement")

        # Pattern: All dimensions degrading
        if all(c.change < -0.1 for c in changes.values()):
            causes.append("Widespread network degradation (systemic issue)")

        # Pattern: Wisdom loss
        if wisdom.change < -0.2:
            causes.append("Visibility reduced (monitoring gaps or packet loss)")

        return causes if causes else ["No clear pattern identified"]

    def _assess_overall(self, changes: Dict[str, StateChange], total_drift: float) -> str:
        """Assess overall network change"""
        if total_drift > 1.0:
            return "CRITICAL: Major network state change detected"
        elif total_drift > 0.5:
            return "WARNING: Significant network drift"
        elif total_drift > 0.2:
            return "NOTICE: Minor network changes"
        else:
            return "STABLE: Network state unchanged"

    def display_comparison(self, analysis: Dict) -> str:
        """Display comparison in formatted output"""
        lines = []

        lines.append(self.fmt.section_header(
            f"Network State Comparison: {analysis['before_label']} → {analysis['after_label']}"
        ))

        # Overall assessment
        lines.append(f"\n{self.fmt.bold('Overall Assessment:')}")
        lines.append(f"  {analysis['overall_assessment']}")
        lines.append(f"  Total Drift: {analysis['total_drift']:.3f}\n")

        # Changes by dimension
        lines.append(self.fmt.subsection_header("Dimension Changes:"))

        for dim_key, change in analysis['changes'].items():
            arrow = "↑" if change.change > 0 else "↓" if change.change < 0 else "→"

            # Color based on severity
            if change.severity == "MAJOR":
                color = Colors.BRIGHT_RED
            elif change.severity == "SIGNIFICANT":
                color = Colors.YELLOW
            elif change.severity == "MINOR":
                color = Colors.CYAN
            else:
                color = Colors.WHITE

            line = (f"  {change.dimension:10} "
                   f"{change.before:.2f} → {change.after:.2f}  "
                   f"({change.change:+.2f}, {change.change_pct:+.1f}%)  {arrow}")

            if change.severity != "NONE":
                line += f"  [{change.severity}]"

            lines.append(self.fmt.color(line, color))

        # Major changes
        if analysis['major_changes']:
            lines.append(f"\n{self.fmt.subsection_header('Major Changes:')}")
            for change in analysis['major_changes']:
                direction = "increased" if change.change > 0 else "decreased"
                lines.append(f"  • {change.dimension} {direction} by {abs(change.change_pct):.1f}%")

        # Likely causes
        lines.append(f"\n{self.fmt.subsection_header('Likely Causes:')}")
        for cause in analysis['likely_causes']:
            lines.append(f"  • {cause}")

        return "\n".join(lines)

    def load_state_from_file(self, filepath: Path) -> Tuple[Coordinates, str, datetime]:
        """Load network state from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)

        coords = Coordinates(
            love=data['coordinates']['love'],
            justice=data['coordinates']['justice'],
            power=data['coordinates']['power'],
            wisdom=data['coordinates']['wisdom']
        )

        label = data.get('label', filepath.stem)
        timestamp = datetime.fromisoformat(data['timestamp'])

        return coords, label, timestamp

    def compare_files(self, before_file: Path, after_file: Path) -> Dict:
        """Compare network states from two files"""
        before_coords, before_label, before_time = self.load_state_from_file(before_file)
        after_coords, after_label, after_time = self.load_state_from_file(after_file)

        # Use timestamps if labels not specified
        if before_label == before_file.stem:
            before_label = before_time.strftime("%Y-%m-%d %H:%M")
        if after_label == after_file.stem:
            after_label = after_time.strftime("%Y-%m-%d %H:%M")

        return self.compare_states(before_coords, after_coords, before_label, after_label)


if __name__ == "__main__":
    # Demo diff mode
    from .semantic_engine import Coordinates

    analyzer = DiffAnalyzer()

    # Scenario: Network became over-secured
    before = Coordinates(love=0.85, justice=0.35, power=0.70, wisdom=0.90)
    after = Coordinates(love=0.45, justice=0.75, power=0.55, wisdom=0.60)

    analysis = analyzer.compare_states(before, after, "Yesterday", "Today")
    print(analyzer.display_comparison(analysis))
