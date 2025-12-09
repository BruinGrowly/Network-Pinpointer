#!/usr/bin/env python3
"""
Simple Output Translator

Converts LJPW semantic analysis into plain, actionable language
that network admins actually care about.
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class SimpleInsight:
    """A single plain-language insight"""
    icon: str
    message: str
    severity: str  # info, warning, critical, success


def translate_coordinates(love: float, justice: float, power: float, wisdom: float) -> List[SimpleInsight]:
    """Convert LJPW coordinates to plain-language insights"""
    insights = []

    # Connectivity (Love)
    if love >= 0.7:
        insights.append(SimpleInsight("✓", "Good connectivity", "success"))
    elif love >= 0.4:
        insights.append(SimpleInsight("~", "Moderate connectivity", "info"))
    elif love > 0:
        insights.append(SimpleInsight("⚠", "Limited connectivity - may have reachability issues", "warning"))
    else:
        insights.append(SimpleInsight("✗", "No connectivity detected", "critical"))

    # Security (Justice)
    if justice >= 0.7:
        insights.append(SimpleInsight("🔒", "Strong security controls in place", "success"))
    elif justice >= 0.4:
        insights.append(SimpleInsight("🔐", "Moderate security", "info"))
    elif justice > 0.1:
        insights.append(SimpleInsight("⚠", "Light security - verify this is intentional", "warning"))
    # No security isn't necessarily bad for public services

    # Performance (Power)
    if power >= 0.7:
        insights.append(SimpleInsight("⚡", "High performance capability", "success"))
    elif power >= 0.4:
        insights.append(SimpleInsight("~", "Normal performance", "info"))
    elif power > 0 and power < 0.2:
        insights.append(SimpleInsight("🐢", "May have performance limitations", "warning"))

    # Visibility (Wisdom)
    if wisdom >= 0.7:
        insights.append(SimpleInsight("👁", "Good monitoring/visibility", "success"))
    elif wisdom >= 0.4:
        insights.append(SimpleInsight("~", "Some visibility", "info"))
    elif wisdom < 0.2 and (love > 0.3 or power > 0.3):
        insights.append(SimpleInsight("⚠", "Low visibility - consider adding monitoring", "warning"))

    return insights


def get_system_type(love: float, justice: float, power: float, wisdom: float) -> str:
    """Determine what type of system this appears to be in plain language"""

    # Find dominant dimension
    dims = {'connectivity': love, 'security': justice, 'performance': power, 'monitoring': wisdom}
    dominant = max(dims, key=dims.get)
    dominant_val = dims[dominant]

    if dominant_val < 0.2:
        return "Minimal presence (possibly offline or highly restricted)"

    # Check for common patterns
    if justice > 0.6 and love < 0.3:
        return "Security appliance (firewall, IDS, or access control)"

    if love > 0.6 and power > 0.4:
        return "Application server (web, API, or database)"

    if wisdom > 0.6:
        return "Monitoring or management system"

    if love > 0.7:
        return "Connectivity-focused (gateway, proxy, or load balancer)"

    if power > 0.6:
        return "High-performance system (compute or data processing)"

    if justice > 0.5:
        return "Policy enforcement point"

    # Balanced
    if all(v > 0.3 for v in [love, justice, power, wisdom]):
        return "Well-rounded infrastructure system"

    return f"Primarily {dominant}-focused system"


def get_health_summary(love: float, justice: float, power: float, wisdom: float,
                       ping_success: bool = None, open_ports: int = None) -> Tuple[str, str]:
    """Get a simple health summary: (status_icon, one_line_summary)"""

    issues = []

    if ping_success is False:
        return ("🔴", "Unreachable - check network path and firewall rules")

    if love < 0.1 and power < 0.1:
        return ("🔴", "System appears down or completely blocked")

    if love < 0.2:
        issues.append("connectivity issues")

    if open_ports == 0:
        issues.append("no open ports")

    if wisdom < 0.1 and (love > 0.3 or power > 0.3):
        issues.append("no monitoring detected")

    if issues:
        return ("🟡", f"Potential issues: {', '.join(issues)}")

    if love > 0.5 and (ping_success is True or ping_success is None):
        return ("🟢", "System appears healthy")

    return ("🟢", "No obvious issues detected")


def format_simple_output(
    target: str,
    coordinates: Tuple[float, float, float, float],
    ping_success: bool = None,
    latency_ms: float = None,
    open_ports: List[int] = None,
    show_what_it_is: bool = True
) -> str:
    """Format a complete simple output for a target"""

    love, justice, power, wisdom = coordinates
    lines = []

    # Header
    lines.append(f"\n{'='*50}")
    lines.append(f"  {target}")
    lines.append(f"{'='*50}")

    # Health summary
    status_icon, summary = get_health_summary(
        love, justice, power, wisdom,
        ping_success,
        len(open_ports) if open_ports else None
    )
    lines.append(f"\n{status_icon} Status: {summary}")

    # Basic facts (if available)
    if ping_success is not None:
        if ping_success and latency_ms:
            lines.append(f"   Ping: {latency_ms:.0f}ms")
        elif not ping_success:
            lines.append(f"   Ping: Failed")

    if open_ports is not None:
        if open_ports:
            ports_str = ", ".join(str(p) for p in open_ports[:5])
            if len(open_ports) > 5:
                ports_str += f" (+{len(open_ports)-5} more)"
            lines.append(f"   Open ports: {ports_str}")
        else:
            lines.append(f"   Open ports: None detected")

    # What type of system
    if show_what_it_is:
        system_type = get_system_type(love, justice, power, wisdom)
        lines.append(f"\n📋 Appears to be: {system_type}")

    # Key insights
    insights = translate_coordinates(love, justice, power, wisdom)
    if insights:
        lines.append(f"\n📊 Key observations:")
        for insight in insights:
            lines.append(f"   {insight.icon} {insight.message}")

    lines.append("")
    return "\n".join(lines)


def format_ping_simple(host: str, success: bool, latency: float, packet_loss: float,
                       coordinates: Tuple[float, float, float, float]) -> str:
    """Simple output for ping command"""
    lines = []

    if success:
        if latency < 50:
            lines.append(f"🟢 {host} is reachable ({latency:.0f}ms) - Fast response")
        elif latency < 200:
            lines.append(f"🟢 {host} is reachable ({latency:.0f}ms) - Normal latency")
        else:
            lines.append(f"🟡 {host} is reachable ({latency:.0f}ms) - High latency")

        if packet_loss > 0:
            lines.append(f"   ⚠ {packet_loss:.0f}% packet loss detected")
    else:
        lines.append(f"🔴 {host} is unreachable")
        lines.append(f"   Possible causes:")
        lines.append(f"   • Host is down")
        lines.append(f"   • Firewall blocking ICMP")
        lines.append(f"   • Network path issue")

    return "\n".join(lines)


def format_scan_simple(host: str, open_ports: List[Tuple[int, str]],
                       total_scanned: int) -> str:
    """Simple output for scan command"""
    lines = []

    if not open_ports:
        lines.append(f"🔒 {host}: No open ports found (scanned {total_scanned})")
        lines.append(f"   This could mean:")
        lines.append(f"   • Host is well-secured")
        lines.append(f"   • Host is down")
        lines.append(f"   • Firewall is blocking")
    else:
        lines.append(f"📡 {host}: {len(open_ports)} open port(s)")
        lines.append("")

        # Group by common categories
        web_ports = []
        db_ports = []
        admin_ports = []
        other_ports = []

        for port, service in open_ports:
            if port in [80, 443, 8080, 8443]:
                web_ports.append((port, service))
            elif port in [3306, 5432, 27017, 6379, 1433]:
                db_ports.append((port, service))
            elif port in [22, 23, 3389, 5900]:
                admin_ports.append((port, service))
            else:
                other_ports.append((port, service))

        if web_ports:
            lines.append("   🌐 Web services:")
            for port, svc in web_ports:
                lines.append(f"      {port} ({svc})")

        if db_ports:
            lines.append("   💾 Databases:")
            for port, svc in db_ports:
                lines.append(f"      {port} ({svc})")

        if admin_ports:
            lines.append("   🔧 Remote access:")
            for port, svc in admin_ports:
                lines.append(f"      {port} ({svc})")

        if other_ports:
            lines.append("   📦 Other:")
            for port, svc in other_ports[:5]:
                lines.append(f"      {port} ({svc})")
            if len(other_ports) > 5:
                lines.append(f"      ... and {len(other_ports)-5} more")

    return "\n".join(lines)


def format_analyze_simple(operation: str, dominant: str,
                          coordinates: Tuple[float, float, float, float]) -> str:
    """Simple output for analyze command"""

    love, justice, power, wisdom = coordinates

    # Map to plain categories
    category_map = {
        'Love': ('connectivity', '🔗'),
        'Justice': ('security/policy', '🔒'),
        'Power': ('performance/control', '⚡'),
        'Wisdom': ('monitoring/diagnostics', '👁'),
    }

    category, icon = category_map.get(dominant, ('general', '•'))

    lines = []
    lines.append(f"\n\"{operation}\"")
    lines.append(f"")
    lines.append(f"{icon} This is primarily a {category} operation")

    # Secondary aspects
    aspects = []
    if love > 0.3 and dominant != 'Love':
        aspects.append("involves connectivity")
    if justice > 0.3 and dominant != 'Justice':
        aspects.append("has security implications")
    if power > 0.3 and dominant != 'Power':
        aspects.append("affects performance")
    if wisdom > 0.3 and dominant != 'Wisdom':
        aspects.append("provides visibility")

    if aspects:
        lines.append(f"   Also {', '.join(aspects)}")

    return "\n".join(lines)
