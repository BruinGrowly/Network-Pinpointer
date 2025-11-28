#!/usr/bin/env python3
"""
Semantic Probe - Comprehensive LJPW Discovery and Profiling

Performs multi-dimensional network discovery and provides deep semantic
analysis of targets, revealing their LJPW "identity" and purpose.
"""

import socket
import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Tuple, Dict
from statistics import mean

from .semantic_engine import NetworkSemanticEngine, Coordinates
from .diagnostics import NetworkDiagnostics, PingResult, PortScanResult
from .service_archetypes import ServiceArchetype, match_archetypes
from .semantic_metrics import SemanticMetrics


@dataclass
class SemanticProfile:
    """Complete semantic fingerprint of a network target"""
    
    # Target information
    target: str
    ip_address: str
    timestamp: datetime
    scan_duration: float = 0.0
    
    # Discovery results
    ping_result: Optional[PingResult] = None
    dns_name: Optional[str] = None
    reverse_dns: Optional[str] = None
    open_ports: List[PortScanResult] = field(default_factory=list)
    ttl: Optional[int] = None
    
    # Semantic analysis
    ljpw_coordinates: Coordinates = None
    dominant_dimension: str = "unknown"
    harmony_score: float = 0.0
    semantic_clarity: float = 0.0
    
    # Classification
    inferred_purpose: str = "unknown"
    matched_archetypes: List[Tuple[ServiceArchetype, float]] = field(default_factory=list)
    service_classification: str = "unknown"
    security_posture: str = "unknown"
    
    # Recommendations
    recommendations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    # Semantic metrics (dimensional combinations)
    semantic_metrics: Optional[Dict] = None
    
    # Semantic mass and dynamics
    semantic_mass: float = 0.0
    semantic_density: float = 0.0
    semantic_influence: float = 0.0


class SemanticProbe:
    """Comprehensive semantic discovery and profiling tool"""
    
    # Common ports to scan (grouped by service type)
    QUICK_PORTS = [22, 80, 443, 3389]  # SSH, HTTP, HTTPS, RDP
    STANDARD_PORTS = [21, 22, 23, 25, 53, 80, 443, 3306, 3389, 5432, 8080, 8443]
    DEEP_PORTS = [
        21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995,
        1433, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 9090, 27017
    ]
    
    def __init__(self, semantic_engine: NetworkSemanticEngine):
        self.engine = semantic_engine
        self.diagnostics = NetworkDiagnostics(semantic_engine)
    
    def probe(
        self, 
        target: str, 
        quick: bool = False, 
        deep: bool = False
    ) -> SemanticProfile:
        """
        Perform comprehensive semantic probe of target.
        
        Args:
            target: Target host (IP or hostname)
            quick: Quick scan (ping + DNS + top 4 ports)
            deep: Deep scan (all common ports + extended analysis)
        
        Returns:
            Complete semantic profile
        """
        start_time = datetime.now()
        
        # Determine port list
        if quick:
            ports = self.QUICK_PORTS
        elif deep:
            ports = self.DEEP_PORTS
        else:
            ports = self.STANDARD_PORTS
        
        # Initialize profile
        profile = SemanticProfile(
            target=target,
            ip_address="",
            timestamp=start_time,
        )
        
        # Step 1: DNS Resolution
        profile.ip_address = self._resolve_target(target)
        if not profile.ip_address:
            profile.warnings.append("Failed to resolve target hostname")
            return profile
        
        # Step 2: Reverse DNS
        profile.reverse_dns = self._reverse_dns(profile.ip_address)
        profile.dns_name = target if target != profile.ip_address else profile.reverse_dns
        
        # Step 3: Ping
        profile.ping_result = self._ping_target(target)
        if profile.ping_result:
            profile.ttl = self._extract_ttl(profile.ping_result)
        
        # Step 4: Port Scanning
        profile.open_ports = self._scan_ports(profile.ip_address, ports)
        
        # Step 5: Semantic Analysis
        self._analyze_semantics(profile)
        
        # Step 5.5: Calculate Semantic Metrics (dimensional combinations)
        self._calculate_metrics(profile)
        
        # Step 5.6: Calculate Semantic Mass
        self._calculate_mass(profile)
        
        # Step 6: Archetype Matching
        self._match_archetypes(profile)
        
        # Step 7: Classification
        self._classify_service(profile)
        
        # Step 8: Security Assessment
        self._assess_security(profile)
        
        # Step 9: Generate Recommendations
        self._generate_recommendations(profile)
        
        # Calculate scan duration
        end_time = datetime.now()
        profile.scan_duration = (end_time - start_time).total_seconds()
        
        return profile

    async def probe_async(
        self, 
        target: str, 
        quick: bool = False, 
        deep: bool = False
    ) -> SemanticProfile:
        """
        Perform comprehensive ASYNC semantic probe of target.
        """
        from .async_diagnostics import AsyncNetworkDiagnostics
        async_diag = AsyncNetworkDiagnostics(self.engine)
        
        start_time = datetime.now()
        
        # Determine port list
        if quick:
            ports = self.QUICK_PORTS
        elif deep:
            ports = self.DEEP_PORTS
        else:
            ports = self.STANDARD_PORTS
        
        # Initialize profile
        profile = SemanticProfile(
            target=target,
            ip_address="",
            timestamp=start_time,
        )
        
        # Step 1: DNS Resolution (Async)
        profile.ip_address = await async_diag.resolve_hostname(target)
        if not profile.ip_address:
            profile.warnings.append("Failed to resolve target hostname")
            return profile
            
        # Parallel Execution: Reverse DNS, Ping, Port Scan
        # We can run these concurrently
        
        async def get_reverse_dns():
            return await async_diag.reverse_dns(profile.ip_address)
            
        async def run_ping():
            return await async_diag.ping(target)
            
        async def run_port_scan():
            return await async_diag.scan_ports(profile.ip_address, ports)
            
        # Execute parallel tasks
        results = await asyncio.gather(
            get_reverse_dns(),
            run_ping(),
            run_port_scan(),
            return_exceptions=True
        )
        
        # Unpack results
        rdns_res = results[0]
        ping_res = results[1]
        ports_res = results[2]
        
        # Handle Reverse DNS
        if not isinstance(rdns_res, Exception) and rdns_res:
            profile.reverse_dns = rdns_res
            profile.dns_name = target if target != profile.ip_address else profile.reverse_dns
            
        # Handle Ping
        if not isinstance(ping_res, Exception):
            profile.ping_result = ping_res
            if profile.ping_result:
                profile.ttl = self._extract_ttl(profile.ping_result)
                
        # Handle Ports
        if not isinstance(ports_res, Exception):
            profile.open_ports = ports_res
            
        # Step 5: Semantic Analysis (Sync logic is fine here as it's CPU bound)
        self._analyze_semantics(profile)
        
        # Step 5.5: Calculate Semantic Metrics
        self._calculate_metrics(profile)
        
        # Step 5.6: Calculate Semantic Mass
        self._calculate_mass(profile)
        
        # Step 6: Archetype Matching
        self._match_archetypes(profile)
        
        # Step 7: Classification
        self._classify_service(profile)
        
        # Step 8: Security Assessment
        self._assess_security(profile)
        
        # Step 9: Generate Recommendations
        self._generate_recommendations(profile)
        
        # Calculate scan duration
        end_time = datetime.now()
        profile.scan_duration = (end_time - start_time).total_seconds()
        
        return profile

    def _resolve_target(self, target: str) -> Optional[str]:
        """Resolve target to IP address"""
        try:
            return socket.gethostbyname(target)
        except socket.gaierror:
            return None
    
    def _reverse_dns(self, ip: str) -> Optional[str]:
        """Perform reverse DNS lookup"""
        return self.diagnostics.reverse_dns(ip)
    
    def _ping_target(self, target: str) -> Optional[PingResult]:
        """Ping target"""
        try:
            return self.diagnostics.ping(target, count=4, timeout=5)
        except Exception:
            return None
    
    def _extract_ttl(self, ping_result: PingResult) -> Optional[int]:
        """Extract TTL from ping result (simplified - would need platform-specific parsing)"""
        # This is a placeholder - real implementation would parse ping output
        return None
    
    def _scan_ports(self, ip: str, ports: List[int]) -> List[PortScanResult]:
        """Scan specified ports"""
        return self.diagnostics.scan_ports(ip, ports, timeout=1.0)
    
    def _analyze_semantics(self, profile: SemanticProfile):
        """Analyze and aggregate semantic coordinates"""
        # Collect all coordinate sources
        coord_sources = []
        
        # Add ping coordinates (if available)
        if profile.ping_result and profile.ping_result.success:
            coord_sources.append(profile.ping_result.semantic_coords)
        
        # Add port scan coordinates (weighted by service importance)
        for port_result in profile.open_ports:
            if port_result.is_open:
                coord_sources.append(port_result.semantic_coords)
        
        # If no sources, create default
        if not coord_sources:
            profile.ljpw_coordinates = Coordinates(0.0, 0.0, 0.0, 0.0)
            profile.dominant_dimension = "unknown"
            profile.harmony_score = 0.0
            profile.semantic_clarity = 0.0
            return
        
        # Aggregate coordinates (weighted average)
        avg_l = mean(c.love for c in coord_sources)
        avg_j = mean(c.justice for c in coord_sources)
        avg_p = mean(c.power for c in coord_sources)
        avg_w = mean(c.wisdom for c in coord_sources)
        
        profile.ljpw_coordinates = Coordinates(avg_l, avg_j, avg_p, avg_w)
        
        # Determine dominant dimension
        dims = {
            'Love': avg_l,
            'Justice': avg_j,
            'Power': avg_p,
            'Wisdom': avg_w,
        }
        profile.dominant_dimension = max(dims, key=dims.get)
        
        # Calculate harmony (distance from anchor)
        anchor = Coordinates(1.0, 1.0, 1.0, 1.0)
        distance = self.engine.vocabulary.get_distance(anchor, profile.ljpw_coordinates)
        profile.harmony_score = max(0.0, 1.0 - (distance / 2.0))
        
        # Calculate semantic clarity
        profile.semantic_clarity = self.engine.vocabulary.get_semantic_clarity(
            profile.ljpw_coordinates
        )
    
    def _calculate_metrics(self, profile: SemanticProfile):
        """Calculate semantic metrics from dimensional combinations"""
        if not profile.ljpw_coordinates:
            return
        
        from .semantic_metrics import SemanticMetrics
        metrics = SemanticMetrics(profile.ljpw_coordinates)
        profile.semantic_metrics = metrics.get_summary()
    
    def _calculate_mass(self, profile: SemanticProfile):
        """
        Calculate semantic mass and related metrics.
        
        Semantic Mass = concept_count * semantic_clarity * (1 + harmony_score)
        
        This represents the "semantic significance" of the system.
        """
        if not profile.ljpw_coordinates:
            return
        
        # Count semantic concepts
        concept_count = len(profile.open_ports) + 1  # +1 for base system
        
        # Calculate mass
        profile.semantic_mass = (
            concept_count * 
            profile.semantic_clarity * 
            (1.0 + profile.harmony_score)
        )
        
        # Calculate density (mass per dimensional volume)
        coords = profile.ljpw_coordinates
        dimensional_volume = (coords.love + coords.justice + coords.power + coords.wisdom) / 4.0
        
        if dimensional_volume > 0:
            profile.semantic_density = profile.semantic_mass / dimensional_volume
        else:
            profile.semantic_density = 0.0
        
        # Influence is mass * clarity (how much this system affects others)
        profile.semantic_influence = profile.semantic_mass * profile.semantic_clarity
    
    def _match_archetypes(self, profile: SemanticProfile):
        """Match profile against known archetypes"""
        if profile.ljpw_coordinates:
            profile.matched_archetypes = match_archetypes(
                profile.ljpw_coordinates,
                min_confidence=0.5
            )
    
    def _classify_service(self, profile: SemanticProfile):
        """Classify the service type based on open ports and coordinates"""
        if not profile.open_ports:
            profile.service_classification = "No Services Detected"
            profile.inferred_purpose = "Inactive or highly restricted system"
            return
        
        # Analyze open ports
        open_port_numbers = [p.port for p in profile.open_ports if p.is_open]
        
        # Web services
        if 80 in open_port_numbers or 443 in open_port_numbers:
            if 443 in open_port_numbers and 80 not in open_port_numbers:
                profile.service_classification = "Secure Web Service"
            else:
                profile.service_classification = "Web Service"
            profile.inferred_purpose = "Web content delivery or API service"
        
        # Database services
        elif any(p in open_port_numbers for p in [3306, 5432, 27017, 6379]):
            profile.service_classification = "Database Service"
            profile.inferred_purpose = "Data storage and management"
        
        # SSH only
        elif open_port_numbers == [22]:
            profile.service_classification = "SSH Server"
            profile.inferred_purpose = "Remote administration or bastion host"
        
        # Multiple services
        elif len(open_port_numbers) > 5:
            profile.service_classification = "Multi-Service Host"
            profile.inferred_purpose = "General-purpose or development server"
        
        # Use archetype if available
        elif profile.matched_archetypes:
            primary = profile.matched_archetypes[0][0]
            profile.service_classification = primary.name
            profile.inferred_purpose = primary.purpose
        
        else:
            profile.service_classification = "Unknown Service Type"
            profile.inferred_purpose = "Unable to determine primary purpose"
    
    def _assess_security(self, profile: SemanticProfile):
        """Assess security posture"""
        if not profile.ljpw_coordinates:
            profile.security_posture = "UNKNOWN"
            return
        
        j = profile.ljpw_coordinates.justice
        l = profile.ljpw_coordinates.love
        
        # High justice, low love = very secure
        if j > 0.7 and l < 0.3:
            profile.security_posture = "VERY_SECURE"
        # High justice, moderate love = secure
        elif j > 0.6:
            profile.security_posture = "SECURE"
        # Balanced
        elif 0.3 <= j <= 0.6 and 0.3 <= l <= 0.7:
            profile.security_posture = "BALANCED"
        # High love, low justice = open
        elif l > 0.7 and j < 0.3:
            profile.security_posture = "OPEN"
        # Very low justice = potentially vulnerable
        elif j < 0.2:
            profile.security_posture = "POTENTIALLY_VULNERABLE"
        else:
            profile.security_posture = "MODERATE"
    
    def _generate_recommendations(self, profile: SemanticProfile):
        """Generate recommendations based on profile"""
        if not profile.ljpw_coordinates:
            return
        
        l, j, p, w = profile.ljpw_coordinates
        open_ports = [p.port for p in profile.open_ports if p.is_open]
        
        # Check for insecure services
        dangerous_ports = {21: 'FTP', 23: 'Telnet', 80: 'HTTP'}
        for port, service in dangerous_ports.items():
            if port in open_ports:
                if port == 80 and 443 in open_ports:
                    profile.recommendations.append(
                        f"Consider HTTPS-only (port 443) and redirect HTTP traffic"
                    )
                else:
                    profile.warnings.append(
                        f"Insecure service detected: {service} (port {port})"
                    )
                    profile.recommendations.append(
                        f"Replace {service} with secure alternative"
                    )
        
        # High love, low justice
        if l > 0.7 and j < 0.3:
            profile.recommendations.append(
                "Consider implementing additional security measures (high accessibility, low security)"
            )
        
        # Low love, very high justice
        if l < 0.2 and j > 0.8:
            profile.recommendations.append(
                "System may be over-secured - verify accessibility meets requirements"
            )
        
        # Low harmony
        if profile.harmony_score < 0.5:
            profile.recommendations.append(
                "Low harmony detected - review configuration for semantic coherence"
            )
        
        # Many open ports
        if len(open_ports) > 10:
            profile.warnings.append(
                f"Many open ports detected ({len(open_ports)}) - potential attack surface"
            )
            profile.recommendations.append(
                "Review and close unnecessary ports (principle of least privilege)"
            )
        
        # Good configuration
        if profile.harmony_score > 0.7 and 0.3 <= j <= 0.6:
            profile.recommendations.append(
                "Well-configured system with good balance of accessibility and security"
            )
