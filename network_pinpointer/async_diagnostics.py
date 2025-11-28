"""
Async Network Diagnostic Tools

Provides asynchronous versions of network diagnostic functions using asyncio.
Maps results to LJPW semantic space.
"""

import asyncio
import platform
import re
import socket
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple

from .semantic_engine import NetworkSemanticEngine, Coordinates
from .diagnostics import PingResult, TracerouteResult, PortScanResult, TracerouteHop

class AsyncNetworkDiagnostics:
    """Asynchronous network diagnostic tools"""
    
    def __init__(self, semantic_engine: NetworkSemanticEngine):
        self.engine = semantic_engine
        self.system = platform.system()
        
    async def scan_port(self, host: str, port: int, timeout: float = 1.0) -> PortScanResult:
        """
        Async port scan
        """
        is_open = False
        service_name = "unknown"
        
        try:
            future = asyncio.open_connection(host, port)
            reader, writer = await asyncio.wait_for(future, timeout=timeout)
            is_open = True
            
            # Try to get service name (blocking call, but fast usually)
            try:
                service_name = socket.getservbyport(port)
            except OSError:
                service_name = "unknown"
                
            writer.close()
            await writer.wait_closed()
            
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
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

    async def scan_ports(self, host: str, ports: List[int], timeout: float = 1.0) -> List[PortScanResult]:
        """Scan multiple ports concurrently"""
        tasks = [self.scan_port(host, port, timeout) for port in ports]
        return await asyncio.gather(*tasks)

    async def ping(self, host: str, count: int = 4, timeout: int = 5) -> PingResult:
        """
        Async ping
        """
        # Determine ping command based on OS
        if self.system == "Windows":
            cmd = ["ping", "-n", str(count), "-w", str(timeout * 1000), host]
        else:
            cmd = ["ping", "-c", str(count), "-W", str(timeout), host]
            
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout + 5)
            except asyncio.TimeoutError:
                process.kill()
                raise asyncio.TimeoutError
                
            output = stdout.decode()
            success = process.returncode == 0
            
            # Parse results (reuse logic from sync version if possible, or duplicate)
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

                if packets_sent > 0:
                    packet_loss = ((packets_sent - packets_received) / packets_sent * 100)

                # Parse average latency
                if self.system == "Windows":
                    match = re.search(r"Average = (\d+)ms", output)
                else:
                    match = re.search(r"min/avg/max[/\w]* = [\d.]+/([\d.]+)/", output)

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
            
        except asyncio.TimeoutError:
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

    async def resolve_hostname(self, hostname: str) -> Optional[str]:
        """Async DNS resolution with caching"""
        from .caching import SemanticCache
        cache = SemanticCache()
        
        cached_ip = cache.get_dns(hostname)
        if cached_ip:
            return cached_ip
            
        try:
            loop = asyncio.get_running_loop()
            ip = await loop.run_in_executor(None, socket.gethostbyname, hostname)
            cache.put_dns(hostname, ip)
            return ip
        except (socket.gaierror, OSError):
            return None

    async def reverse_dns(self, ip: str) -> Optional[str]:
        """Async Reverse DNS"""
        try:
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, socket.gethostbyaddr, ip)
            return result[0]
        except (socket.herror, socket.gaierror, OSError):
            return None
