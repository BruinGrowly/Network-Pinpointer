#!/usr/bin/env python3
"""
Network Diagnostic Tools with Semantic Mapping

Provides traditional network diagnostic functions (ping, traceroute, port scan)
mapped to LJPW semantic space.
"""

import subprocess
import socket
import platform
import re
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from datetime import datetime

from .semantic_engine import NetworkSemanticEngine, Coordinates


@dataclass
class PingResult:
    """Result of ping operation"""

    host: str
    success: bool
    packets_sent: int
    packets_received: int
    packet_loss: float
    avg_latency: float
    semantic_coords: Coordinates
    semantic_analysis: str
    timestamp: datetime


@dataclass
class TracerouteHop:
    """Single hop in traceroute"""

    hop_number: int
    host: str
    ip: str
    latency: float


@dataclass
class TracerouteResult:
    """Result of traceroute operation"""

    target: str
    hops: List[TracerouteHop]
    total_hops: int
    success: bool
    semantic_coords: Coordinates
    semantic_analysis: str
    timestamp: datetime


@dataclass
class PortScanResult:
    """Result of port scanning"""

    host: str
    port: int
    is_open: bool
    service_name: str
    semantic_coords: Coordinates
    timestamp: datetime


@dataclass
class NetworkInterface:
    """Network interface information"""

    name: str
    ip_address: str
    is_up: bool
    mac_address: Optional[str]
    semantic_coords: Coordinates


class NetworkDiagnostics:
    """Network diagnostic tools with semantic analysis"""

    def __init__(self, semantic_engine: NetworkSemanticEngine):
        self.engine = semantic_engine
        self.system = platform.system()

    def ping(
        self, host: str, count: int = 4, timeout: int = 5
    ) -> PingResult:
        """
        Ping a host and analyze semantically

        Maps to: High Wisdom (diagnostic), Medium Love (connectivity test)
        """
        # Determine ping command based on OS
        if self.system == "Windows":
            cmd = ["ping", "-n", str(count), "-w", str(timeout * 1000), host]
        else:
            cmd = ["ping", "-c", str(count), "-W", str(timeout), host]

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout + 5
            )
            output = result.stdout

            # Parse ping results
            success = result.returncode == 0
            packets_sent = count
            packets_received = 0
            packet_loss = 100.0
            avg_latency = 0.0

            if success:
                # Parse packets received
                if self.system == "Windows":
                    match = re.search(r"Received = (\d+)", output)
                else:
                    match = re.search(r"(\d+) received", output)

                if match:
                    packets_received = int(match.group(1))

                packet_loss = (
                    (packets_sent - packets_received) / packets_sent * 100
                )

                # Parse average latency
                if self.system == "Windows":
                    match = re.search(r"Average = (\d+)ms", output)
                else:
                    match = re.search(
                        r"min/avg/max[/\w]* = [\d.]+/([\d.]+)/", output
                    )

                if match:
                    avg_latency = float(match.group(1))

            # Semantic analysis
            operation_desc = f"ping test connectivity diagnose monitor {host}"
            semantic_result = self.engine.analyze_operation(operation_desc)

            # Analyze result quality
            if packet_loss == 0:
                quality = "excellent connectivity"
            elif packet_loss < 25:
                quality = "good connectivity with minor loss"
            elif packet_loss < 75:
                quality = "poor connectivity with significant loss"
            else:
                quality = "critical connectivity failure"

            semantic_analysis = (
                f"Operation: {semantic_result.operation_type} "
                f"({semantic_result.dominant_dimension}-dominant) | "
                f"Quality: {quality}"
            )

            return PingResult(
                host=host,
                success=success,
                packets_sent=packets_sent,
                packets_received=packets_received,
                packet_loss=packet_loss,
                avg_latency=avg_latency,
                semantic_coords=semantic_result.coordinates,
                semantic_analysis=semantic_analysis,
                timestamp=datetime.now(),
            )

        except subprocess.TimeoutExpired:
            operation_desc = f"ping test connectivity timeout failure {host}"
            semantic_result = self.engine.analyze_operation(operation_desc)

            return PingResult(
                host=host,
                success=False,
                packets_sent=count,
                packets_received=0,
                packet_loss=100.0,
                avg_latency=0.0,
                semantic_coords=semantic_result.coordinates,
                semantic_analysis=f"Operation timeout - {semantic_result.operation_type}",
                timestamp=datetime.now(),
            )

    def traceroute(
        self, target: str, max_hops: int = 30, timeout: int = 5
    ) -> TracerouteResult:
        """
        Traceroute to target and analyze path semantically

        Maps to: High Wisdom (path analysis), High Love (route discovery)
        """
        # Determine traceroute command
        if self.system == "Windows":
            cmd = ["tracert", "-h", str(max_hops), "-w", str(timeout * 1000), target]
        else:
            cmd = ["traceroute", "-m", str(max_hops), "-w", str(timeout), target]

        hops = []
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=max_hops * timeout + 10
            )
            output = result.stdout

            # Parse traceroute output
            hop_pattern = r"^\s*(\d+)\s+(?:[\d.]+\s+ms\s+)?(?:[\d.]+\s+ms\s+)?(?:[\d.]+\s+ms\s+)?(?:\*\s+)?(?:\*\s+)?(?:\*\s+)?([^\s]+)\s+\(?([\d.]+)\)?.*?(\d+\.?\d*)\s*ms"

            for line in output.split("\n"):
                match = re.search(hop_pattern, line)
                if match:
                    hop_num = int(match.group(1))
                    hostname = match.group(2) if match.group(2) != "*" else "unknown"
                    ip = match.group(3) if match.group(3) else "unknown"
                    latency = (
                        float(match.group(4)) if match.group(4) else 0.0
                    )

                    hops.append(
                        TracerouteHop(
                            hop_number=hop_num, host=hostname, ip=ip, latency=latency
                        )
                    )

            success = len(hops) > 0
            total_hops = len(hops)

            # Semantic analysis
            operation_desc = (
                f"traceroute path analysis route discovery network topology {target}"
            )
            semantic_result = self.engine.analyze_operation(operation_desc)

            semantic_analysis = (
                f"Operation: {semantic_result.operation_type} "
                f"({semantic_result.dominant_dimension}-dominant) | "
                f"Hops: {total_hops}"
            )

            return TracerouteResult(
                target=target,
                hops=hops,
                total_hops=total_hops,
                success=success,
                semantic_coords=semantic_result.coordinates,
                semantic_analysis=semantic_analysis,
                timestamp=datetime.now(),
            )

        except subprocess.TimeoutExpired:
            operation_desc = f"traceroute timeout failure {target}"
            semantic_result = self.engine.analyze_operation(operation_desc)

            return TracerouteResult(
                target=target,
                hops=[],
                total_hops=0,
                success=False,
                semantic_coords=semantic_result.coordinates,
                semantic_analysis=f"Operation timeout - {semantic_result.operation_type}",
                timestamp=datetime.now(),
            )

    def scan_port(
        self, host: str, port: int, timeout: float = 1.0
    ) -> PortScanResult:
        """
        Scan a single port and analyze semantically

        Maps to: Medium Wisdom (discovery), Medium Justice (policy check)
        """
        is_open = False
        service_name = "unknown"

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            is_open = result == 0
            sock.close()

            # Try to get service name
            try:
                service_name = socket.getservbyport(port)
            except OSError:
                service_name = "unknown"

        except socket.error:
            is_open = False

        # Semantic analysis
        state = "open" if is_open else "closed"
        operation_desc = (
            f"port scan check service discover {service_name} {state} {port}"
        )
        semantic_result = self.engine.analyze_operation(operation_desc)

        return PortScanResult(
            host=host,
            port=port,
            is_open=is_open,
            service_name=service_name,
            semantic_coords=semantic_result.coordinates,
            timestamp=datetime.now(),
        )

    def scan_ports(
        self, host: str, ports: List[int], timeout: float = 1.0
    ) -> List[PortScanResult]:
        """Scan multiple ports"""
        results = []
        for port in ports:
            results.append(self.scan_port(host, port, timeout))
        return results

    def get_network_interfaces(self) -> List[NetworkInterface]:
        """
        Get network interface information

        Maps to: High Wisdom (information), High Love (interface connectivity)
        """
        interfaces = []

        try:
            if self.system == "Windows":
                cmd = ["ipconfig", "/all"]
            else:
                cmd = ["ifconfig"]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            output = result.stdout

            # Parse interface information (simplified)
            # This is a basic implementation - production would use netifaces or psutil
            current_interface = None
            current_ip = None
            current_mac = None
            is_up = False

            for line in output.split("\n"):
                # Detect new interface
                if not line.startswith(" ") and not line.startswith("\t") and ":" in line:
                    # Save previous interface
                    if current_interface:
                        operation_desc = f"network interface {current_interface} connectivity"
                        semantic_result = self.engine.analyze_operation(operation_desc)

                        interfaces.append(
                            NetworkInterface(
                                name=current_interface,
                                ip_address=current_ip or "unknown",
                                is_up=is_up,
                                mac_address=current_mac,
                                semantic_coords=semantic_result.coordinates,
                            )
                        )

                    # Start new interface
                    current_interface = line.split(":")[0].strip()
                    current_ip = None
                    current_mac = None
                    is_up = False

                # Parse IP address
                ip_match = re.search(r"inet (?:addr:)?([\d.]+)", line)
                if ip_match:
                    current_ip = ip_match.group(1)
                    is_up = True

                # Parse MAC address
                mac_match = re.search(
                    r"(?:ether|HWaddr|Physical Address)[:\s]+([\da-fA-F:]+)", line
                )
                if mac_match:
                    current_mac = mac_match.group(1)

            # Save last interface
            if current_interface:
                operation_desc = f"network interface {current_interface} connectivity"
                semantic_result = self.engine.analyze_operation(operation_desc)

                interfaces.append(
                    NetworkInterface(
                        name=current_interface,
                        ip_address=current_ip or "unknown",
                        is_up=is_up,
                        mac_address=current_mac,
                        semantic_coords=semantic_result.coordinates,
                    )
                )

        except Exception as e:
            print(f"Error getting network interfaces: {e}")

        return interfaces

    def resolve_hostname(self, hostname: str) -> Optional[str]:
        """
        Resolve hostname to IP address

        Maps to: High Wisdom (information lookup), Low Power (query)
        """
        try:
            ip = socket.gethostbyname(hostname)
            return ip
        except socket.gaierror:
            return None

    def reverse_dns(self, ip: str) -> Optional[str]:
        """
        Reverse DNS lookup

        Maps to: High Wisdom (information lookup), Low Power (query)
        """
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            return hostname
        except (socket.herror, socket.gaierror):
            return None

    def check_connectivity(
        self, host: str = "8.8.8.8", port: int = 53, timeout: float = 3.0
    ) -> bool:
        """
        Quick connectivity check

        Maps to: High Love (connectivity), Medium Wisdom (test)
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except socket.error:
            return False
