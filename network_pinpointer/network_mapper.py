#!/usr/bin/env python3
"""
Network Mapper - Semantic Analysis of Network Infrastructure

Maps network devices, services, and topology to LJPW space.
Detects network "architectural smells" and provides recommendations.
"""

import os
import json
import ipaddress
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Dict, List, Tuple, Optional
from statistics import mean
from datetime import datetime

from .semantic_engine import NetworkSemanticEngine, Coordinates
from .diagnostics import NetworkDiagnostics


@dataclass
class DeviceAnalysis:
    """Semantic analysis of a network device"""

    host: str
    ip_address: str
    coordinates: Coordinates
    reachable: bool
    open_ports: List[int]
    services: List[str]
    avg_latency: float
    dominant_dimension: str
    device_type: str  # "server", "router", "workstation", "unknown"
    semantic_purpose: str


@dataclass
class NetworkSmell:
    """Detected network configuration problem"""

    smell_type: str
    affected_host: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    description: str
    impact: float  # 0-1 score
    recommendation: str


@dataclass
class NetworkOpportunity:
    """Network optimization opportunity"""

    host: str
    opportunity_type: str
    potential_improvement: float  # 0-1 score
    description: str
    suggested_actions: List[str] = field(default_factory=list)


@dataclass
class TopologyCluster:
    """Cluster of devices with similar semantic purpose"""

    cluster_name: str
    dominant_dimension: str
    devices: List[DeviceAnalysis]
    avg_coordinates: Coordinates
    cohesion_score: float  # How semantically similar devices are


class NetworkMapper:
    """Advanced network topology semantic analyzer"""

    def __init__(
        self, semantic_engine: NetworkSemanticEngine, quiet: bool = False
    ):
        self.engine = semantic_engine
        self.diagnostics = NetworkDiagnostics(semantic_engine)
        self.device_analyses: Dict[str, DeviceAnalysis] = {}
        self.network_smells: List[NetworkSmell] = []
        self.network_opportunities: List[NetworkOpportunity] = []
        self.topology_clusters: Dict[str, TopologyCluster] = {}
        self.quiet = quiet

    def scan_network(
        self, network_range: str, common_ports: Optional[List[int]] = None
    ) -> Dict:
        """
        Scan a network range and analyze semantically

        Args:
            network_range: CIDR notation (e.g., "192.168.1.0/24")
            common_ports: List of ports to scan (default: common services)
        """
        if not self.quiet:
            print(f"🔍 Scanning network: {network_range}")
            print("=" * 70)

        if common_ports is None:
            # Common service ports
            common_ports = [
                21,
                22,
                23,
                25,
                53,
                80,
                110,
                143,
                443,
                445,
                3306,
                3389,
                5432,
                8080,
                8443,
            ]

        # Parse network range
        try:
            network = ipaddress.ip_network(network_range, strict=False)
        except ValueError as e:
            if not self.quiet:
                print(f"❌ Invalid network range: {e}")
            return {"error": str(e)}

        # Scan each host
        hosts_scanned = 0
        hosts_reachable = 0

        for ip in network.hosts():
            ip_str = str(ip)
            hosts_scanned += 1

            if not self.quiet and hosts_scanned % 10 == 0:
                print(f"  Scanned {hosts_scanned} hosts...", end="\r")

            # Quick connectivity check first
            if not self.diagnostics.check_connectivity(ip_str, timeout=0.5):
                continue

            hosts_reachable += 1

            # Ping the host
            ping_result = self.diagnostics.ping(ip_str, count=2, timeout=2)

            # Scan ports
            port_results = self.diagnostics.scan_ports(
                ip_str, common_ports, timeout=0.5
            )
            open_ports = [p.port for p in port_results if p.is_open]
            services = [
                p.service_name for p in port_results if p.is_open and p.service_name
            ]

            # Analyze device semantically
            device_analysis = self._analyze_device(
                ip_str, ping_result, open_ports, services
            )
            self.device_analyses[ip_str] = device_analysis

        if not self.quiet:
            print(f"\n✅ Scanned {hosts_scanned} hosts, {hosts_reachable} reachable")
            print("=" * 70)

        # Perform advanced analysis
        self._cluster_topology()
        self._detect_network_smells()
        self._identify_opportunities()

        return self._generate_report()

    def _analyze_device(
        self, ip: str, ping_result, open_ports: List[int], services: List[str]
    ) -> DeviceAnalysis:
        """Analyze a single device semantically"""
        # Build semantic description
        service_desc = " ".join(services) if services else "unknown"
        port_desc = f"ports {' '.join(map(str, open_ports[:5]))}" if open_ports else ""

        description = f"network device {ip} service {service_desc} {port_desc}"

        semantic_result = self.engine.analyze_operation(description)

        # Classify device type based on open ports
        device_type = self._classify_device_type(open_ports, services)

        # Determine semantic purpose
        semantic_purpose = self._determine_semantic_purpose(
            semantic_result.coordinates, device_type, services
        )

        return DeviceAnalysis(
            host=ip,
            ip_address=ip,
            coordinates=semantic_result.coordinates,
            reachable=ping_result.success,
            open_ports=open_ports,
            services=services,
            avg_latency=ping_result.avg_latency,
            dominant_dimension=semantic_result.dominant_dimension,
            device_type=device_type,
            semantic_purpose=semantic_purpose,
        )

    def _classify_device_type(
        self, open_ports: List[int], services: List[str]
    ) -> str:
        """Classify device based on ports and services"""
        # Server indicators
        server_ports = {80, 443, 8080, 8443, 3306, 5432, 25, 110, 143}
        # Router/network device indicators
        router_ports = {23, 22, 161, 162}
        # Workstation indicators
        workstation_ports = {445, 3389, 5900}

        if any(p in server_ports for p in open_ports):
            return "server"
        elif any(p in router_ports for p in open_ports):
            return "router"
        elif any(p in workstation_ports for p in open_ports):
            return "workstation"
        else:
            return "unknown"

    def _determine_semantic_purpose(
        self, coords: Coordinates, device_type: str, services: List[str]
    ) -> str:
        """Determine the semantic purpose of a device"""
        l, j, p, w = coords.love, coords.justice, coords.power, coords.wisdom

        # Dominant dimension determines primary purpose
        if l > max(j, p, w):
            if "http" in services or "https" in services:
                return "Web Service (Connectivity)"
            else:
                return "Communication Hub (Love)"
        elif j > max(l, p, w):
            if "ssh" in services or any("security" in s for s in services):
                return "Security Gateway (Justice)"
            else:
                return "Policy Enforcement (Justice)"
        elif p > max(l, j, w):
            if device_type == "server":
                return "Application Server (Power)"
            else:
                return "Control System (Power)"
        elif w > max(l, j, p):
            if "monitor" in " ".join(services).lower():
                return "Monitoring System (Wisdom)"
            else:
                return "Information Service (Wisdom)"
        else:
            return "Mixed Purpose"

    def _cluster_topology(self):
        """Group devices by semantic similarity"""
        if not self.device_analyses:
            return

        # Group by dominant dimension
        by_dimension = defaultdict(list)
        for device in self.device_analyses.values():
            by_dimension[device.dominant_dimension].append(device)

        # Create clusters
        for dimension, devices in by_dimension.items():
            if not devices:
                continue

            # Calculate average coordinates
            avg_l = mean([d.coordinates.love for d in devices])
            avg_j = mean([d.coordinates.justice for d in devices])
            avg_p = mean([d.coordinates.power for d in devices])
            avg_w = mean([d.coordinates.wisdom for d in devices])

            avg_coords = Coordinates(avg_l, avg_j, avg_p, avg_w)

            # Calculate cohesion (how similar devices are)
            distances = [
                self.engine.vocabulary.get_distance(d.coordinates, avg_coords)
                for d in devices
            ]
            avg_distance = mean(distances) if distances else 0
            cohesion = max(0.0, 1.0 - (avg_distance / 1.732))

            # Determine cluster name
            cluster_name = f"{dimension} Cluster"

            self.topology_clusters[dimension] = TopologyCluster(
                cluster_name=cluster_name,
                dominant_dimension=dimension,
                devices=devices,
                avg_coordinates=avg_coords,
                cohesion_score=cohesion,
            )

    def _detect_network_smells(self):
        """Detect network configuration problems"""
        if not self.device_analyses:
            return

        for ip, device in self.device_analyses.items():
            # Smell 1: Too many open ports (security risk)
            if len(device.open_ports) > 10:
                self.network_smells.append(
                    NetworkSmell(
                        smell_type="Excessive Open Ports",
                        affected_host=ip,
                        severity="HIGH" if len(device.open_ports) > 20 else "MEDIUM",
                        description=f"Device has {len(device.open_ports)} open ports (threshold: 10)",
                        impact=min(1.0, len(device.open_ports) / 30),
                        recommendation="Review and close unnecessary ports. Apply principle of least privilege.",
                    )
                )

            # Smell 2: High latency (performance issue)
            if device.avg_latency > 100:
                self.network_smells.append(
                    NetworkSmell(
                        smell_type="High Latency",
                        affected_host=ip,
                        severity="CRITICAL"
                        if device.avg_latency > 500
                        else "MEDIUM",
                        description=f"Average latency: {device.avg_latency:.1f}ms (threshold: 100ms)",
                        impact=min(1.0, device.avg_latency / 1000),
                        recommendation="Investigate network path. Check for congestion or routing issues.",
                    )
                )

            # Smell 3: Unclear purpose (semantic confusion)
            if device.semantic_purpose == "Mixed Purpose":
                l, j, p, w = device.coordinates
                spread = max(l, j, p, w) - min(l, j, p, w)

                if spread < 0.3:
                    self.network_smells.append(
                        NetworkSmell(
                            smell_type="Unclear Purpose",
                            affected_host=ip,
                            severity="LOW",
                            description=f"Device has no clear semantic purpose (spread: {spread:.2f})",
                            impact=0.4,
                            recommendation="Clarify device role in network architecture documentation.",
                        )
                    )

            # Smell 4: Dangerous services exposed
            dangerous_ports = {23, 21, 445, 139}  # Telnet, FTP, SMB
            exposed_dangerous = [p for p in device.open_ports if p in dangerous_ports]

            if exposed_dangerous:
                self.network_smells.append(
                    NetworkSmell(
                        smell_type="Insecure Services",
                        affected_host=ip,
                        severity="CRITICAL",
                        description=f"Dangerous ports exposed: {exposed_dangerous}",
                        impact=0.9,
                        recommendation="Disable insecure protocols. Use SSH/SFTP/encrypted alternatives.",
                    )
                )

    def _identify_opportunities(self):
        """Identify network optimization opportunities"""
        if not self.device_analyses:
            return

        for ip, device in self.device_analyses.items():
            # Opportunity 1: Modernize services
            if 80 in device.open_ports and 443 not in device.open_ports:
                self.network_opportunities.append(
                    NetworkOpportunity(
                        host=ip,
                        opportunity_type="Security Upgrade",
                        potential_improvement=0.7,
                        description="HTTP service without HTTPS",
                        suggested_actions=[
                            "Enable HTTPS/TLS encryption",
                            "Redirect HTTP to HTTPS",
                            "Obtain SSL certificate",
                        ],
                    )
                )

            # Opportunity 2: Consolidate services
            if len(device.open_ports) > 5 and device.device_type == "server":
                self.network_opportunities.append(
                    NetworkOpportunity(
                        host=ip,
                        opportunity_type="Service Consolidation",
                        potential_improvement=0.6,
                        description=f"Server running {len(device.open_ports)} services",
                        suggested_actions=[
                            "Consider containerization",
                            "Separate concerns across multiple hosts",
                            "Use reverse proxy for HTTP services",
                        ],
                    )
                )

            # Opportunity 3: Improve semantic clarity
            l, j, p, w = device.coordinates
            if max(l, j, p, w) < 0.5:
                self.network_opportunities.append(
                    NetworkOpportunity(
                        host=ip,
                        opportunity_type="Purpose Clarification",
                        potential_improvement=0.5,
                        description="Device purpose unclear from network perspective",
                        suggested_actions=[
                            "Document device role in architecture",
                            "Configure descriptive hostname",
                            "Update DHCP/DNS records",
                        ],
                    )
                )

    def _generate_report(self) -> Dict:
        """Generate comprehensive network analysis report"""
        if not self.device_analyses:
            return {"error": "No devices analyzed"}

        total_devices = len(self.device_analyses)
        avg_latency = mean([d.avg_latency for d in self.device_analyses.values()])

        return {
            "total_devices": total_devices,
            "clusters": self.topology_clusters,
            "avg_latency": avg_latency,
            "network_smells": self.network_smells,
            "network_opportunities": self.network_opportunities,
        }

    def print_report(self, report: Dict):
        """Print human-readable network analysis report"""
        print("\n")
        print("=" * 70)
        print("NETWORK SEMANTIC TOPOLOGY MAP")
        print("=" * 70)

        # Overall metrics
        print(f"\n📊 OVERALL METRICS")
        print(f"   Total devices discovered: {report['total_devices']}")
        print(f"   Average network latency: {report['avg_latency']:.1f}ms")

        # Clusters
        clusters = report["clusters"]
        if clusters:
            print(f"\n🗺️  TOPOLOGY CLUSTERS")
            for dimension, cluster in clusters.items():
                icon = {
                    "Love": "💛",
                    "Justice": "⚖️",
                    "Power": "⚡",
                    "Wisdom": "📚",
                }.get(dimension, "●")

                print(
                    f"\n{icon} {cluster.cluster_name} ({len(cluster.devices)} devices)"
                )
                print(f"   Cohesion: {cluster.cohesion_score:.0%}")
                print(f"   Avg Coordinates: {cluster.avg_coordinates}")

                # Show sample devices
                for device in cluster.devices[:3]:
                    print(f"     • {device.host:15s} - {device.semantic_purpose}")
                    print(
                        f"       Ports: {len(device.open_ports)} open | Latency: {device.avg_latency:.1f}ms"
                    )

                if len(cluster.devices) > 3:
                    print(f"     ... and {len(cluster.devices) - 3} more devices")

        # Network smells
        smells = report.get("network_smells", [])
        if smells:
            print(f"\n🚨 NETWORK CONFIGURATION ISSUES ({len(smells)} detected)")
            print("=" * 70)

            by_severity = defaultdict(list)
            for smell in smells:
                by_severity[smell.severity].append(smell)

            for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
                issues = by_severity.get(severity, [])
                if not issues:
                    continue

                print(f"\n{severity} ({len(issues)} issues):")
                for smell in issues[:3]:
                    print(f"  • {smell.smell_type}: {smell.affected_host}")
                    print(f"    {smell.description}")
                    print(f"    → {smell.recommendation}")

                if len(issues) > 3:
                    print(f"  ... and {len(issues) - 3} more {severity} issues")

        # Opportunities
        opportunities = report.get("network_opportunities", [])
        if opportunities:
            print(f"\n💡 OPTIMIZATION OPPORTUNITIES (Top 5)")
            print("=" * 70)

            top_opps = sorted(
                opportunities, key=lambda x: x.potential_improvement, reverse=True
            )[:5]

            for i, opp in enumerate(top_opps, 1):
                print(f"\n{i}. {opp.host} - {opp.opportunity_type}")
                print(
                    f"   Potential improvement: {opp.potential_improvement:.0%}"
                )
                print(f"   {opp.description}")
                if opp.suggested_actions:
                    print(f"   Suggested actions:")
                    for action in opp.suggested_actions:
                        print(f"     → {action}")

        print("\n" + "=" * 70)

    def export_topology_json(self, output_path: str = "network_topology.json"):
        """Export network topology to JSON"""
        data = {
            "scan_timestamp": datetime.now().isoformat(),
            "total_devices": len(self.device_analyses),
            "devices": [],
            "clusters": {},
        }

        # Export devices
        for ip, device in self.device_analyses.items():
            data["devices"].append(
                {
                    "ip": ip,
                    "coordinates": {
                        "L": device.coordinates.love,
                        "J": device.coordinates.justice,
                        "P": device.coordinates.power,
                        "W": device.coordinates.wisdom,
                    },
                    "device_type": device.device_type,
                    "semantic_purpose": device.semantic_purpose,
                    "open_ports": device.open_ports,
                    "services": device.services,
                    "latency": device.avg_latency,
                }
            )

        # Export clusters
        for dimension, cluster in self.topology_clusters.items():
            data["clusters"][dimension] = {
                "name": cluster.cluster_name,
                "device_count": len(cluster.devices),
                "cohesion": cluster.cohesion_score,
                "avg_coordinates": {
                    "L": cluster.avg_coordinates.love,
                    "J": cluster.avg_coordinates.justice,
                    "P": cluster.avg_coordinates.power,
                    "W": cluster.avg_coordinates.wisdom,
                },
            }

        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        if not self.quiet:
            print(f"✅ Exported topology to {output_path}")
