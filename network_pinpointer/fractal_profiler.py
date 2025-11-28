#!/usr/bin/env python3
"""
Fractal Semantic Profiler

Generates semantic profiles at multiple scales:
- Packet scale (microscopic)
- Port scale (small)
- Service scale (medium)
- Host scale (large) - current default
- Network scale (macro)
- Infrastructure scale (mega)
- Organization scale (cosmic)

Each scale has LJPW coordinates that aggregate from below and decompose from above.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from enum import Enum

from .semantic_engine import Coordinates, NetworkSemanticEngine
from .semantic_probe import SemanticProfile, SemanticProbe


class Scale(Enum):
    """Fractal scale levels"""
    PACKET = "packet"
    PORT = "port"
    SERVICE = "service"
    HOST = "host"
    NETWORK = "network"
    INFRASTRUCTURE = "infrastructure"
    ORGANIZATION = "organization"


@dataclass
class ScaleProfile:
    """Semantic profile at a specific scale"""
    scale: Scale
    target: str
    timestamp: datetime
    coordinates: Coordinates
    semantic_clarity: float
    harmony_score: float
    semantic_mass: float
    description: str
    metadata: Dict = field(default_factory=dict)
    sub_profiles: List['ScaleProfile'] = field(default_factory=list)


class FractalSemanticProfiler:
    """Generate semantic profiles at multiple fractal scales"""
    
    def __init__(self, engine: NetworkSemanticEngine):
        self.engine = engine
        self.probe = SemanticProbe(engine)
    
    def profile_at_scale(self, target: str, scale: Scale, **kwargs) -> ScaleProfile:
        """
        Generate semantic profile at specified scale.
        
        Args:
            target: Target to profile
            scale: Scale level
            **kwargs: Scale-specific parameters
        
        Returns:
            ScaleProfile at the specified scale
        """
        if scale == Scale.PACKET:
            return self._profile_packet_scale(target, **kwargs)
        elif scale == Scale.PORT:
            return self._profile_port_scale(target, **kwargs)
        elif scale == Scale.SERVICE:
            return self._profile_service_scale(target, **kwargs)
        elif scale == Scale.HOST:
            return self._profile_host_scale(target, **kwargs)
        elif scale == Scale.NETWORK:
            return self._profile_network_scale(target, **kwargs)
        elif scale == Scale.INFRASTRUCTURE:
            return self._profile_infrastructure_scale(target, **kwargs)
        elif scale == Scale.ORGANIZATION:
            return self._profile_organization_scale(target, **kwargs)
        else:
            raise ValueError(f"Unknown scale: {scale}")
    
    def _profile_packet_scale(self, target: str, **kwargs) -> ScaleProfile:
        """
        Profile at packet scale (microscopic).
        
        Analyzes individual packets for LJPW properties:
        - L: Source/dest addressing, routing
        - J: Protocol compliance, checksums, encryption
        - P: Payload size, priority flags, QoS
        - W: Metadata, timing, sequence numbers
        """
        # For now, return a placeholder
        # Full implementation would use scapy for packet capture
        
        description = f"packet analysis for {target}"
        result = self.engine.analyze_operation(description)
        
        return ScaleProfile(
            scale=Scale.PACKET,
            target=target,
            timestamp=datetime.now(),
            coordinates=result.coordinates,
            semantic_clarity=result.semantic_clarity,
            harmony_score=result.harmony_score,
            semantic_mass=result.concept_count * result.semantic_clarity * (1 + result.harmony_score),
            description=description,
            metadata={
                'note': 'Packet-scale profiling requires packet capture (scapy)',
                'concept_count': result.concept_count,
            }
        )
    
    def _profile_port_scale(self, target: str, port: int = None, **kwargs) -> ScaleProfile:
        """
        Profile at port scale (small).
        
        Deep analysis of individual ports:
        - L: Connection count, accessibility
        - J: Encryption, authentication requirements
        - P: Throughput, response time
        - W: Banner info, service fingerprint
        """
        if port is None:
            raise ValueError("Port number required for port-scale profiling")
        
        # Build description from port analysis
        description_parts = [f"port {port}"]
        
        # Common port services
        port_services = {
            21: "ftp file transfer",
            22: "ssh secure shell encrypted",
            23: "telnet remote access",
            25: "smtp email",
            53: "dns domain name",
            80: "http web server public accessible",
            443: "https web server secure encrypted ssl tls",
            3306: "mysql database server",
            5432: "postgresql database server",
            6379: "redis cache database",
            8080: "http web server alternative",
            27017: "mongodb database nosql",
        }
        
        if port in port_services:
            description_parts.append(port_services[port])
        
        # Analyze encryption
        if port in [22, 443, 465, 587, 993, 995]:
            description_parts.append("encrypted secure protected")
        
        # Analyze accessibility
        if port in [80, 443, 8080, 8443]:
            description_parts.append("public accessible external")
        
        # Analyze monitoring
        if port in [9090, 9100, 3000]:  # Prometheus, node_exporter, Grafana
            description_parts.append("monitoring metrics observability")
        
        description = " ".join(description_parts)
        result = self.engine.analyze_operation(description)
        
        return ScaleProfile(
            scale=Scale.PORT,
            target=f"{target}:{port}",
            timestamp=datetime.now(),
            coordinates=result.coordinates,
            semantic_clarity=result.semantic_clarity,
            harmony_score=result.harmony_score,
            semantic_mass=result.concept_count * result.semantic_clarity * (1 + result.harmony_score),
            description=description,
            metadata={
                'port': port,
                'concept_count': result.concept_count,
            }
        )
    
    def _profile_service_scale(self, target: str, service: str = None, **kwargs) -> ScaleProfile:
        """
        Profile at service scale (medium).
        
        Analyzes individual services:
        - L: API endpoints, integrations
        - J: Security policies, validation
        - P: Performance, scalability
        - W: Observability, metrics
        """
        if service is None:
            service = "unknown service"
        
        description = f"{service} service on {target}"
        result = self.engine.analyze_operation(description)
        
        return ScaleProfile(
            scale=Scale.SERVICE,
            target=f"{target}/{service}",
            timestamp=datetime.now(),
            coordinates=result.coordinates,
            semantic_clarity=result.semantic_clarity,
            harmony_score=result.harmony_score,
            semantic_mass=result.concept_count * result.semantic_clarity * (1 + result.harmony_score),
            description=description,
            metadata={
                'service': service,
                'concept_count': result.concept_count,
            }
        )
    
    def _profile_host_scale(self, target: str, **kwargs) -> ScaleProfile:
        """
        Profile at host scale (large) - current default.
        
        Uses existing SemanticProbe for comprehensive host profiling.
        """
        quick = kwargs.get('quick', True)
        profile = self.probe.probe(target, quick=quick)
        
        return ScaleProfile(
            scale=Scale.HOST,
            target=target,
            timestamp=profile.timestamp,
            coordinates=profile.ljpw_coordinates,
            semantic_clarity=profile.semantic_clarity,
            harmony_score=profile.harmony_score,
            semantic_mass=profile.semantic_mass,
            description=f"host {target} with {len(profile.open_ports)} open ports",
            metadata={
                'open_ports': len(profile.open_ports),
                'inferred_purpose': profile.inferred_purpose,
                'security_posture': profile.security_posture,
            },
            sub_profiles=[
                self._profile_port_scale(target, port.port)
                for port in profile.open_ports[:5]  # Top 5 ports
            ]
        )
    
    def _profile_network_scale(self, target: str, hosts: List[str] = None, **kwargs) -> ScaleProfile:
        """
        Profile at network scale (macro).
        
        Aggregates host profiles into network profile:
        - L: Connectivity topology, routing
        - J: Security architecture, boundaries
        - P: Infrastructure capacity, bottlenecks
        - W: Monitoring coverage, visibility
        """
        if hosts is None:
            hosts = []
        
        # Profile each host
        host_profiles = []
        for host in hosts[:10]:  # Limit to 10 hosts for now
            try:
                host_profile = self._profile_host_scale(host, quick=True)
                host_profiles.append(host_profile)
            except Exception:
                continue
        
        # Aggregate coordinates
        if host_profiles:
            aggregated_coords = self.aggregate_coordinates([p.coordinates for p in host_profiles])
            avg_clarity = sum(p.semantic_clarity for p in host_profiles) / len(host_profiles)
            avg_harmony = sum(p.harmony_score for p in host_profiles) / len(host_profiles)
            total_mass = sum(p.semantic_mass for p in host_profiles)
        else:
            # Fallback to description-based analysis
            description = f"network {target} infrastructure topology"
            result = self.engine.analyze_operation(description)
            aggregated_coords = result.coordinates
            avg_clarity = result.semantic_clarity
            avg_harmony = result.harmony_score
            total_mass = result.concept_count * result.semantic_clarity * (1 + result.harmony_score)
        
        return ScaleProfile(
            scale=Scale.NETWORK,
            target=target,
            timestamp=datetime.now(),
            coordinates=aggregated_coords,
            semantic_clarity=avg_clarity,
            harmony_score=avg_harmony,
            semantic_mass=total_mass,
            description=f"network {target} with {len(host_profiles)} hosts",
            metadata={
                'host_count': len(host_profiles),
                'total_mass': total_mass,
            },
            sub_profiles=host_profiles
        )
    
    def _profile_infrastructure_scale(self, target: str, networks: List[str] = None, **kwargs) -> ScaleProfile:
        """
        Profile at infrastructure scale (mega).
        
        Aggregates network profiles into infrastructure profile.
        """
        description = f"infrastructure {target} datacenter cloud platform"
        result = self.engine.analyze_operation(description)
        
        return ScaleProfile(
            scale=Scale.INFRASTRUCTURE,
            target=target,
            timestamp=datetime.now(),
            coordinates=result.coordinates,
            semantic_clarity=result.semantic_clarity,
            harmony_score=result.harmony_score,
            semantic_mass=result.concept_count * result.semantic_clarity * (1 + result.harmony_score),
            description=description,
            metadata={
                'network_count': len(networks) if networks else 0,
                'concept_count': result.concept_count,
            }
        )
    
    def _profile_organization_scale(self, target: str, **kwargs) -> ScaleProfile:
        """
        Profile at organization scale (cosmic).
        
        Highest level - entire organizational IT landscape.
        """
        description = f"organization {target} enterprise IT infrastructure network security"
        result = self.engine.analyze_operation(description)
        
        return ScaleProfile(
            scale=Scale.ORGANIZATION,
            target=target,
            timestamp=datetime.now(),
            coordinates=result.coordinates,
            semantic_clarity=result.semantic_clarity,
            harmony_score=result.harmony_score,
            semantic_mass=result.concept_count * result.semantic_clarity * (1 + result.harmony_score),
            description=description,
            metadata={
                'concept_count': result.concept_count,
            }
        )
    
    def aggregate_coordinates(self, coords_list: List[Coordinates], weights: Optional[List[float]] = None) -> Coordinates:
        """
        Aggregate coordinates from smaller scale to larger scale (bottom-up).
        
        Uses weighted average based on semantic mass if weights provided,
        otherwise uses simple average.
        
        Args:
            coords_list: List of coordinates to aggregate
            weights: Optional list of weights (semantic mass) for each coordinate.
                     If None, uses uniform weighting.
        """
        if not coords_list:
            return Coordinates(0, 0, 0, 0)
        
        if weights is None:
            # Simple average (uniform weighting)
            weights = [1.0] * len(coords_list)
        
        # Normalize weights
        total_weight = sum(weights)
        if total_weight == 0:
            # Fallback to uniform if all weights are zero
            weights = [1.0] * len(coords_list)
            total_weight = len(coords_list)
        
        # Weighted average
        avg_l = sum(c.love * w for c, w in zip(coords_list, weights)) / total_weight
        avg_j = sum(c.justice * w for c, w in zip(coords_list, weights)) / total_weight
        avg_p = sum(c.power * w for c, w in zip(coords_list, weights)) / total_weight
        avg_w = sum(c.wisdom * w for c, w in zip(coords_list, weights)) / total_weight
        
        return Coordinates(avg_l, avg_j, avg_p, avg_w)
    
    def decompose_coordinates(
        self, 
        parent_coords: Coordinates, 
        target_scale: Scale,
        context: str = ""
    ) -> Coordinates:
        """
        Decompose coordinates from larger scale to smaller scale (top-down).
        
        Predicts expected coordinates at smaller scale based on parent.
        Applies context-based adjustments when context is provided.
        
        Args:
            parent_coords: Parent scale coordinates
            target_scale: Target scale to decompose to
            context: Optional context string for adjustment (e.g., "security", "performance")
        
        Returns:
            Predicted coordinates at target scale
        """
        # Start with parent coordinates as baseline
        coords = parent_coords
        
        # Apply context-based adjustments if context provided
        if context:
            context_lower = context.lower()
            # Security context: increase Justice
            if 'security' in context_lower or 'auth' in context_lower or 'encrypt' in context_lower:
                coords = Coordinates(
                    coords.love * 0.9,  # Slightly reduce connectivity
                    min(1.0, coords.justice * 1.2),  # Increase security
                    coords.power * 0.95,
                    coords.wisdom * 1.05
                )
            # Performance context: increase Power
            elif 'performance' in context_lower or 'speed' in context_lower or 'throughput' in context_lower:
                coords = Coordinates(
                    coords.love * 1.05,
                    coords.justice * 0.95,
                    min(1.0, coords.power * 1.2),  # Increase performance
                    coords.wisdom * 0.95
                )
            # Monitoring context: increase Wisdom
            elif 'monitor' in context_lower or 'diagnostic' in context_lower or 'log' in context_lower:
                coords = Coordinates(
                    coords.love * 0.95,
                    coords.justice * 0.95,
                    coords.power * 0.95,
                    min(1.0, coords.wisdom * 1.2)  # Increase monitoring
                )
            # Connectivity context: increase Love
            elif 'connect' in context_lower or 'network' in context_lower or 'communication' in context_lower:
                coords = Coordinates(
                    min(1.0, coords.love * 1.2),  # Increase connectivity
                    coords.justice * 0.95,
                    coords.power * 1.05,
                    coords.wisdom * 0.95
                )
        
        # Scale-based adjustments (smaller scales may have different characteristics)
        if target_scale == Scale.PACKET:
            # Packets are more Wisdom-heavy (metadata) and Power-light (small units)
            coords = Coordinates(
                coords.love * 0.9,
                coords.justice * 1.0,
                coords.power * 0.8,
                min(1.0, coords.wisdom * 1.1)
            )
        elif target_scale == Scale.PORT:
            # Ports are more Justice-heavy (access control)
            coords = Coordinates(
                coords.love * 0.95,
                min(1.0, coords.justice * 1.1),
                coords.power * 0.95,
                coords.wisdom * 1.0
            )
        
        # Ensure coordinates stay in valid range [0, 1]
        coords = Coordinates(
            max(0.0, min(1.0, coords.love)),
            max(0.0, min(1.0, coords.justice)),
            max(0.0, min(1.0, coords.power)),
            max(0.0, min(1.0, coords.wisdom))
        )
        
        return coords
    
    def check_scale_consistency(
        self, 
        child_profile: ScaleProfile, 
        parent_profile: ScaleProfile
    ) -> Dict:
        """
        Check consistency between scales.
        
        Verifies that aggregated child coordinates match parent coordinates.
        """
        # Calculate distance between child and expected
        expected = self.decompose_coordinates(
            parent_profile.coordinates,
            child_profile.scale,
            child_profile.description
        )
        
        distance = self._calculate_distance(child_profile.coordinates, expected)
        
        return {
            'consistent': distance < 0.3,
            'distance': distance,
            'child_coords': child_profile.coordinates,
            'expected_coords': expected,
            'parent_coords': parent_profile.coordinates,
        }
    
    def _calculate_distance(self, c1: Coordinates, c2: Coordinates) -> float:
        """Calculate Euclidean distance between coordinates"""
        import math
        return math.sqrt(
            (c1.love - c2.love) ** 2 +
            (c1.justice - c2.justice) ** 2 +
            (c1.power - c2.power) ** 2 +
            (c1.wisdom - c2.wisdom) ** 2
        )
