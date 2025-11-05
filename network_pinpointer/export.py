#!/usr/bin/env python3
"""
Export System - Export diagnostic results to JSON/HTML/Markdown

Supports exporting:
- Diagnostic results
- Health reports
- Historical data
- Comparison reports
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import asdict

from .semantic_engine import Coordinates
from .root_cause_analyzer import RootCauseAnalysis, Issue


class Exporter:
    """Export diagnostic results to various formats"""

    def __init__(self, export_dir: str = "./network_reports"):
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def export_diagnostic_result(
        self,
        target: str,
        coords: Coordinates,
        analysis: Optional[RootCauseAnalysis] = None,
        metadata: Optional[Dict] = None,
        format: str = "json"
    ) -> Path:
        """
        Export diagnostic result

        Args:
            target: Target that was diagnosed
            coords: LJPW coordinates
            analysis: Root cause analysis (optional)
            metadata: Additional metadata (optional)
            format: Export format (json, html, markdown)

        Returns:
            Path to exported file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"diagnostic_{target.replace('.', '_')}_{timestamp}"

        data = self._build_diagnostic_data(target, coords, analysis, metadata)

        if format == "json":
            return self._export_json(data, filename)
        elif format == "html":
            return self._export_html(data, filename)
        elif format == "markdown":
            return self._export_markdown(data, filename)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def export_health_report(
        self,
        network_coords: Coordinates,
        baseline: Optional[Coordinates] = None,
        alerts: Optional[List] = None,
        trends: Optional[Dict] = None,
        format: str = "json"
    ) -> Path:
        """Export network health report"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"health_report_{timestamp}"

        data = {
            "report_type": "network_health",
            "timestamp": datetime.now().isoformat(),
            "coordinates": {
                "love": coords.love,
                "justice": coords.justice,
                "power": coords.power,
                "wisdom": coords.wisdom
            },
            "health_score": (network_coords.love + network_coords.justice +
                           network_coords.power + network_coords.wisdom) / 4,
            "baseline": {
                "love": baseline.love,
                "justice": baseline.justice,
                "power": baseline.power,
                "wisdom": baseline.wisdom
            } if baseline else None,
            "alerts": [asdict(a) if hasattr(a, '__dict__') else a for a in alerts] if alerts else [],
            "trends": trends or {}
        }

        if format == "json":
            return self._export_json(data, filename)
        elif format == "html":
            return self._export_health_html(data, filename)
        elif format == "markdown":
            return self._export_health_markdown(data, filename)

    def export_comparison(
        self,
        before_coords: Coordinates,
        after_coords: Coordinates,
        before_label: str = "Before",
        after_label: str = "After",
        format: str = "json"
    ) -> Path:
        """Export before/after comparison"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comparison_{timestamp}"

        data = {
            "report_type": "comparison",
            "timestamp": datetime.now().isoformat(),
            "before": {
                "label": before_label,
                "love": before_coords.love,
                "justice": before_coords.justice,
                "power": before_coords.power,
                "wisdom": before_coords.wisdom
            },
            "after": {
                "label": after_label,
                "love": after_coords.love,
                "justice": after_coords.justice,
                "power": after_coords.power,
                "wisdom": after_coords.wisdom
            },
            "changes": {
                "love": after_coords.love - before_coords.love,
                "justice": after_coords.justice - before_coords.justice,
                "power": after_coords.power - before_coords.power,
                "wisdom": after_coords.wisdom - before_coords.wisdom
            }
        }

        if format == "json":
            return self._export_json(data, filename)
        elif format == "html":
            return self._export_comparison_html(data, filename)
        elif format == "markdown":
            return self._export_comparison_markdown(data, filename)

    def _build_diagnostic_data(
        self,
        target: str,
        coords: Coordinates,
        analysis: Optional[RootCauseAnalysis],
        metadata: Optional[Dict]
    ) -> Dict:
        """Build diagnostic data structure"""

        data = {
            "report_type": "diagnostic",
            "timestamp": datetime.now().isoformat(),
            "target": target,
            "coordinates": {
                "love": coords.love,
                "justice": coords.justice,
                "power": coords.power,
                "wisdom": coords.wisdom
            },
            "health_score": (coords.love + coords.justice + coords.power + coords.wisdom) / 4,
            "metadata": metadata or {}
        }

        if analysis:
            data["analysis"] = {
                "overall_health": analysis.overall_health,
                "primary_issue": self._issue_to_dict(analysis.primary_issue) if analysis.primary_issue else None,
                "secondary_issues": [self._issue_to_dict(i) for i in analysis.secondary_issues],
                "all_issues": [self._issue_to_dict(i) for i in analysis.all_issues],
                "fix_order": analysis.fix_order
            }

        return data

    def _issue_to_dict(self, issue: Issue) -> Dict:
        """Convert Issue to dictionary"""
        return {
            "title": issue.title,
            "description": issue.description,
            "severity": issue.severity.value,
            "dimension": issue.dimension,
            "impact_percentage": issue.impact_percentage,
            "confidence": issue.confidence,
            "evidence": issue.evidence,
            "recommendations": issue.recommendations
        }

    def _export_json(self, data: Dict, filename: str) -> Path:
        """Export as JSON"""
        output_path = self.export_dir / f"{filename}.json"

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

        return output_path

    def _export_html(self, data: Dict, filename: str) -> Path:
        """Export as HTML"""
        output_path = self.export_dir / f"{filename}.html"

        html = self._generate_diagnostic_html(data)

        with open(output_path, 'w') as f:
            f.write(html)

        return output_path

    def _export_markdown(self, data: Dict, filename: str) -> Path:
        """Export as Markdown"""
        output_path = self.export_dir / f"{filename}.md"

        md = self._generate_diagnostic_markdown(data)

        with open(output_path, 'w') as f:
            f.write(md)

        return output_path

    def _generate_diagnostic_html(self, data: Dict) -> str:
        """Generate HTML for diagnostic report"""

        coords = data["coordinates"]
        analysis = data.get("analysis")

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Network Diagnostic Report - {data['target']}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #2c3e50; }}
        h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .metric {{
            margin: 15px 0;
        }}
        .metric-name {{
            font-weight: bold;
            display: inline-block;
            width: 120px;
        }}
        .bar {{
            display: inline-block;
            height: 20px;
            background: linear-gradient(90deg, #3498db, #2ecc71);
            border-radius: 4px;
            margin-left: 10px;
        }}
        .health-score {{
            font-size: 24px;
            font-weight: bold;
            color: #27ae60;
            margin: 20px 0;
        }}
        .issue {{
            background: #ecf0f1;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid #e74c3c;
            border-radius: 4px;
        }}
        .issue.critical {{ border-color: #c0392b; background: #f8d7da; }}
        .issue.high {{ border-color: #e74c3c; background: #f8d7da; }}
        .issue.medium {{ border-color: #f39c12; background: #fff3cd; }}
        .issue.low {{ border-color: #95a5a6; background: #ecf0f1; }}
        .recommendation {{
            background: #d4edda;
            padding: 10px;
            margin: 10px 0;
            border-left: 4px solid #28a745;
            border-radius: 4px;
        }}
        .timestamp {{
            color: #7f8c8d;
            font-size: 14px;
        }}
        ul {{ margin: 10px 0; padding-left: 25px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Network Diagnostic Report</h1>
        <p class="timestamp">Generated: {data['timestamp']}</p>
        <p><strong>Target:</strong> {data['target']}</p>

        <h2>Health Score</h2>
        <div class="health-score">{data['health_score']*100:.1f}%</div>

        <h2>LJPW Coordinates</h2>
        <div class="metric">
            <span class="metric-name">Love:</span>
            <span>{coords['love']:.2f}</span>
            <div class="bar" style="width: {coords['love']*300}px"></div>
        </div>
        <div class="metric">
            <span class="metric-name">Justice:</span>
            <span>{coords['justice']:.2f}</span>
            <div class="bar" style="width: {coords['justice']*300}px"></div>
        </div>
        <div class="metric">
            <span class="metric-name">Power:</span>
            <span>{coords['power']:.2f}</span>
            <div class="bar" style="width: {coords['power']*300}px"></div>
        </div>
        <div class="metric">
            <span class="metric-name">Wisdom:</span>
            <span>{coords['wisdom']:.2f}</span>
            <div class="bar" style="width: {coords['wisdom']*300}px"></div>
        </div>
"""

        if analysis and analysis.get('primary_issue'):
            primary = analysis['primary_issue']
            html += f"""
        <h2>Primary Issue</h2>
        <div class="issue {primary['severity'].lower()}">
            <h3>{primary['title']}</h3>
            <p>{primary['description']}</p>
            <p><strong>Impact:</strong> {primary['impact_percentage']:.0f}% |
               <strong>Confidence:</strong> {primary['confidence']*100:.0f}%</p>

            <h4>Evidence:</h4>
            <ul>
                {''.join(f'<li>{e}</li>' for e in primary['evidence'])}
            </ul>

            <h4>Recommendations:</h4>
            {''.join(f'<div class="recommendation">{r}</div>' for r in primary['recommendations'])}
        </div>
"""

        if analysis and analysis.get('secondary_issues'):
            html += "<h2>Additional Issues</h2>"
            for issue in analysis['secondary_issues']:
                html += f"""
        <div class="issue {issue['severity'].lower()}">
            <h3>{issue['title']}</h3>
            <p>{issue['description']}</p>
            <p><strong>Impact:</strong> {issue['impact_percentage']:.0f}% |
               <strong>Confidence:</strong> {issue['confidence']*100:.0f}%</p>
        </div>
"""

        html += """
    </div>
</body>
</html>"""

        return html

    def _generate_diagnostic_markdown(self, data: Dict) -> str:
        """Generate Markdown for diagnostic report"""

        coords = data["coordinates"]
        analysis = data.get("analysis")

        md = f"""# Network Diagnostic Report

**Target:** {data['target']}
**Generated:** {data['timestamp']}
**Health Score:** {data['health_score']*100:.1f}%

## LJPW Coordinates

| Dimension | Value | Bar |
|-----------|-------|-----|
| Love      | {coords['love']:.2f} | {'█' * int(coords['love']*20)} |
| Justice   | {coords['justice']:.2f} | {'█' * int(coords['justice']*20)} |
| Power     | {coords['power']:.2f} | {'█' * int(coords['power']*20)} |
| Wisdom    | {coords['wisdom']:.2f} | {'█' * int(coords['wisdom']*20)} |

"""

        if analysis and analysis.get('primary_issue'):
            primary = analysis['primary_issue']
            md += f"""## Primary Issue

### {primary['title']}

{primary['description']}

**Severity:** {primary['severity']}
**Impact:** {primary['impact_percentage']:.0f}% of total problem
**Confidence:** {primary['confidence']*100:.0f}%

#### Evidence:
"""
            for evidence in primary['evidence']:
                md += f"- {evidence}\n"

            md += "\n#### Recommendations:\n"
            for i, rec in enumerate(primary['recommendations'], 1):
                md += f"{i}. {rec}\n"

        return md

    def _export_health_html(self, data: Dict, filename: str) -> Path:
        """Export health report as HTML"""
        # Similar to diagnostic HTML but focused on health
        output_path = self.export_dir / f"{filename}.html"
        # Implementation similar to _generate_diagnostic_html
        with open(output_path, 'w') as f:
            f.write("<html><body><h1>Health Report</h1></body></html>")
        return output_path

    def _export_health_markdown(self, data: Dict, filename: str) -> Path:
        """Export health report as Markdown"""
        output_path = self.export_dir / f"{filename}.md"
        with open(output_path, 'w') as f:
            f.write(f"# Network Health Report\n\n")
        return output_path

    def _export_comparison_html(self, data: Dict, filename: str) -> Path:
        """Export comparison as HTML"""
        output_path = self.export_dir / f"{filename}.html"
        with open(output_path, 'w') as f:
            f.write("<html><body><h1>Comparison Report</h1></body></html>")
        return output_path

    def _export_comparison_markdown(self, data: Dict, filename: str) -> Path:
        """Export comparison as Markdown"""
        output_path = self.export_dir / f"{filename}.md"

        before = data["before"]
        after = data["after"]
        changes = data["changes"]

        md = f"""# Network Comparison Report

**Generated:** {data['timestamp']}

## Comparison: {before['label']} vs {after['label']}

| Dimension | {before['label']} | {after['label']} | Change | % Change |
|-----------|--------|-------|--------|----------|
| Love      | {before['love']:.2f} | {after['love']:.2f} | {changes['love']:+.2f} | {(changes['love']/before['love']*100):+.1f}% |
| Justice   | {before['justice']:.2f} | {after['justice']:.2f} | {changes['justice']:+.2f} | {(changes['justice']/before['justice']*100):+.1f}% |
| Power     | {before['power']:.2f} | {after['power']:.2f} | {changes['power']:+.2f} | {(changes['power']/before['power']*100):+.1f}% |
| Wisdom    | {before['wisdom']:.2f} | {after['wisdom']:.2f} | {changes['wisdom']:+.2f} | {(changes['wisdom']/before['wisdom']*100):+.1f}% |

## Analysis

"""

        # Add analysis of significant changes
        for dim in ['love', 'justice', 'power', 'wisdom']:
            change_pct = abs(changes[dim] / before[dim] * 100) if before[dim] > 0 else 0
            if change_pct > 10:
                direction = "increased" if changes[dim] > 0 else "decreased"
                md += f"- **{dim.capitalize()}** {direction} by {change_pct:.1f}%\n"

        with open(output_path, 'w') as f:
            f.write(md)

        return output_path


if __name__ == "__main__":
    # Demo export functionality
    from .semantic_engine import Coordinates

    exporter = Exporter()

    # Test diagnostic export
    coords = Coordinates(love=0.85, justice=0.35, power=0.65, wisdom=0.90)
    metadata = {"packet_loss": 0.05, "avg_ttl": 64}

    print("Exporting diagnostic result...")
    json_path = exporter.export_diagnostic_result(
        target="api.example.com",
        coords=coords,
        metadata=metadata,
        format="json"
    )
    print(f"✓ Exported to: {json_path}")

    html_path = exporter.export_diagnostic_result(
        target="api.example.com",
        coords=coords,
        metadata=metadata,
        format="html"
    )
    print(f"✓ Exported to: {html_path}")

    # Test comparison export
    before = Coordinates(love=0.85, justice=0.35, power=0.70, wisdom=0.90)
    after = Coordinates(love=0.45, justice=0.75, power=0.55, wisdom=0.60)

    print("\nExporting comparison...")
    comp_path = exporter.export_comparison(
        before_coords=before,
        after_coords=after,
        before_label="Yesterday",
        after_label="Today",
        format="markdown"
    )
    print(f"✓ Exported to: {comp_path}")
