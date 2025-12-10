#!/usr/bin/env python3
"""
Relationship Engine - Love Dimension Enhancement for Network Pinpointer

This module adds relationship intelligence to Network Pinpointer, addressing
the critical gap identified through semantic oscillation experiments:

    "The tool can DO things (Power). It needs to RELATE things (Love)."

Key Features:
- Service Affinity: How well services work together
- Harmony Mesh: Semantic harmony between all communicating pairs
- Integration Health Index: Quality of connections, not just existence
- Bridge Detection: Components connecting semantic clusters
- Love Debt Tracking: Degraded relationships over time

Based on LJPW resonance insights from 10,000-cycle self-reflection.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime
from enum import Enum

from .semantic_engine import Coordinates, NetworkSemanticEngine


# LJPW Constants for resonance calculations
PHI_INV = (math.sqrt(5) - 1) / 2  # ~0.618 (Love)
SQRT2_M1 = math.sqrt(2) - 1       # ~0.414 (Justice)
E_M2 = math.e - 2                 # ~0.718 (Power)
LN2 = math.log(2)                 # ~0.693 (Wisdom)

NATURAL_EQUILIBRIUM = [PHI_INV, SQRT2_M1, E_M2, LN2]
ANCHOR_POINT = [1.0, 1.0, 1.0, 1.0]

# Coupling matrix from resonance experiments
# Shows how dimensions influence each other
COUPLING_MATRIX = [
    [1.0, 1.4, 1.3, 1.5],  # Love amplifies all (especially Wisdom)
    [0.9, 1.0, 0.7, 1.2],  # Justice moderates
    [0.6, 0.8, 1.0, 0.5],  # Power absorbs
    [1.3, 1.1, 1.0, 1.0],  # Wisdom integrates
]


class AffinityLevel(Enum):
    """Levels of service affinity"""
    EXCELLENT = "excellent"      # > 0.8
    GOOD = "good"               # 0.6 - 0.8
    MODERATE = "moderate"       # 0.4 - 0.6
    NEEDS_ATTENTION = "needs_attention"  # 0.2 - 0.4
    POOR = "poor"               # < 0.2


class RelationshipType(Enum):
    """Types of semantic relationships"""
    HARMONIOUS = "harmonious"           # Similar LJPW, work well together
    COMPLEMENTARY = "complementary"     # Different but balancing
    DEPENDENT = "dependent"             # One relies on the other
    COMPETITIVE = "competitive"         # Similar role, potential conflict
    BRIDGE = "bridge"                   # Connects different clusters
    ISOLATED = "isolated"               # Minimal relationships


@dataclass
class ServiceAffinity:
    """Represents affinity between two services"""
    service_a: str
    service_b: str
    affinity_score: float           # 0.0 - 1.0
    affinity_level: AffinityLevel
    relationship_type: RelationshipType
    harmonic_resonance: float       # How well they resonate together
    coupling_strength: float        # Strength of mutual influence
    love_transfer: float            # How much Love flows between them
    description: str
    recommendations: List[str] = field(default_factory=list)


@dataclass
class HarmonyMeshNode:
    """A node in the harmony mesh"""
    service: str
    coordinates: Coordinates
    connections: List[str]          # Connected services
    total_harmony: float            # Sum of harmony with all connections
    avg_harmony: float              # Average harmony
    role: str                       # Hub, Bridge, Leaf, Isolated


@dataclass
class HarmonyMesh:
    """Complete harmony mesh for a network"""
    nodes: Dict[str, HarmonyMeshNode]
    edges: List[Tuple[str, str, float]]  # (service_a, service_b, harmony)
    global_harmony: float           # Network-wide harmony index
    harmony_distribution: Dict[str, int]  # Count by harmony level
    hubs: List[str]                 # High-connectivity nodes
    bridges: List[str]              # Nodes connecting clusters
    weak_links: List[Tuple[str, str]]  # Pairs needing attention


@dataclass
class IntegrationHealth:
    """Health assessment of an integration/connection"""
    source: str
    target: str
    health_score: float             # 0.0 - 1.0
    love_index: float               # Connection quality (Love dimension)
    justice_alignment: float        # Policy/rule alignment
    power_balance: float            # Capacity balance
    wisdom_flow: float              # Information sharing
    bottleneck_risk: float          # Risk of becoming bottleneck
    recommendations: List[str] = field(default_factory=list)


@dataclass
class LoveDebt:
    """Technical debt in the form of degraded relationships"""
    service: str
    debt_score: float               # Amount of accumulated debt
    degraded_relationships: List[str]  # Services with poor affinity
    symptoms: List[str]             # Observable symptoms
    root_causes: List[str]          # Underlying causes
    remediation_priority: int       # 1 = highest priority
    estimated_impact: str           # Impact if not addressed


@dataclass
class Bridge:
    """A component bridging semantic clusters"""
    service: str
    clusters_connected: List[int]   # Cluster IDs
    bridge_strength: float          # How critical the bridge is
    redundancy: float               # Other paths exist?
    coordinates: Coordinates
    description: str


class RelationshipEngine:
    """
    Calculates and tracks relationships between network components.
    This is the core of the Love dimension enhancement.

    The engine uses LJPW resonance dynamics to understand how services
    relate to each other semantically, not just topologically.
    """

    def __init__(self, semantic_engine: Optional[NetworkSemanticEngine] = None):
        self.engine = semantic_engine or NetworkSemanticEngine()
        self.profiles: Dict[str, Coordinates] = {}
        self.connections: Dict[str, Set[str]] = {}  # service -> connected services
        self.history: List[Dict] = []  # Historical relationship data

    def add_service(self, name: str, coordinates: Coordinates) -> None:
        """Register a service with its semantic coordinates"""
        self.profiles[name] = coordinates
        if name not in self.connections:
            self.connections[name] = set()

    def add_connection(self, service_a: str, service_b: str) -> None:
        """Register a connection between services"""
        if service_a not in self.connections:
            self.connections[service_a] = set()
        if service_b not in self.connections:
            self.connections[service_b] = set()
        self.connections[service_a].add(service_b)
        self.connections[service_b].add(service_a)

    # ==================== SERVICE AFFINITY ====================

    def calculate_affinity(self, service_a: str, service_b: str) -> ServiceAffinity:
        """
        Calculate how well two services work together.

        Uses LJPW resonance dynamics to determine:
        - Harmonic resonance (dimensional alignment)
        - Coupling strength (mutual influence)
        - Love transfer (connection quality flow)
        """
        coords_a = self.profiles.get(service_a)
        coords_b = self.profiles.get(service_b)

        if not coords_a or not coords_b:
            return ServiceAffinity(
                service_a=service_a,
                service_b=service_b,
                affinity_score=0.0,
                affinity_level=AffinityLevel.POOR,
                relationship_type=RelationshipType.ISOLATED,
                harmonic_resonance=0.0,
                coupling_strength=0.0,
                love_transfer=0.0,
                description="Unable to calculate - missing coordinates",
                recommendations=["Profile both services to calculate affinity"]
            )

        # Calculate harmonic resonance (how well they vibrate together)
        resonance = self._calculate_harmonic_resonance(coords_a, coords_b)

        # Calculate coupling strength (mutual influence potential)
        coupling = self._calculate_coupling_strength(coords_a, coords_b)

        # Calculate love transfer (connection quality)
        love_transfer = self._calculate_love_transfer(coords_a, coords_b)

        # Combined affinity score
        affinity_score = (
            0.4 * resonance +      # Primary factor
            0.3 * coupling +       # Secondary factor
            0.3 * love_transfer    # Tertiary factor
        )

        # Determine affinity level
        affinity_level = self._get_affinity_level(affinity_score)

        # Determine relationship type
        relationship_type = self._determine_relationship_type(
            coords_a, coords_b, affinity_score
        )

        # Generate description and recommendations
        description = self._generate_affinity_description(
            service_a, service_b, affinity_level, relationship_type
        )
        recommendations = self._generate_affinity_recommendations(
            coords_a, coords_b, affinity_level, relationship_type
        )

        return ServiceAffinity(
            service_a=service_a,
            service_b=service_b,
            affinity_score=affinity_score,
            affinity_level=affinity_level,
            relationship_type=relationship_type,
            harmonic_resonance=resonance,
            coupling_strength=coupling,
            love_transfer=love_transfer,
            description=description,
            recommendations=recommendations
        )

    def _calculate_harmonic_resonance(
        self,
        coords_a: Coordinates,
        coords_b: Coordinates
    ) -> float:
        """
        Calculate harmonic resonance between two services.

        Resonance is high when:
        - Services are in similar regions of LJPW space
        - Their dimensional ratios are harmonic (golden ratio, etc.)
        """
        # Euclidean distance in LJPW space
        distance = math.sqrt(
            (coords_a.love - coords_b.love) ** 2 +
            (coords_a.justice - coords_b.justice) ** 2 +
            (coords_a.power - coords_b.power) ** 2 +
            (coords_a.wisdom - coords_b.wisdom) ** 2
        )

        # Convert distance to resonance (0-2 distance maps to 1-0 resonance)
        base_resonance = max(0.0, 1.0 - distance / 2.0)

        # Bonus for golden ratio alignment
        # If the ratio of their Love values is close to phi
        if coords_a.love > 0 and coords_b.love > 0:
            ratio = max(coords_a.love, coords_b.love) / min(coords_a.love, coords_b.love)
            phi_distance = abs(ratio - (1 + PHI_INV))  # Distance from golden ratio
            if phi_distance < 0.2:
                base_resonance = min(1.0, base_resonance * 1.1)

        return base_resonance

    def _calculate_coupling_strength(
        self,
        coords_a: Coordinates,
        coords_b: Coordinates
    ) -> float:
        """
        Calculate coupling strength using the LJPW coupling matrix.

        Shows how much one service's dimensions can influence the other's.
        """
        vec_a = [coords_a.love, coords_a.justice, coords_a.power, coords_a.wisdom]
        vec_b = [coords_b.love, coords_b.justice, coords_b.power, coords_b.wisdom]

        # Apply coupling matrix
        coupled_a = [
            sum(COUPLING_MATRIX[i][j] * vec_a[j] for j in range(4))
            for i in range(4)
        ]
        coupled_b = [
            sum(COUPLING_MATRIX[i][j] * vec_b[j] for j in range(4))
            for i in range(4)
        ]

        # Coupling strength is the dot product normalized
        dot_product = sum(coupled_a[i] * coupled_b[i] for i in range(4))
        norm_a = math.sqrt(sum(x*x for x in coupled_a))
        norm_b = math.sqrt(sum(x*x for x in coupled_b))

        if norm_a * norm_b > 0:
            coupling = dot_product / (norm_a * norm_b)
        else:
            coupling = 0.0

        return min(1.0, max(0.0, coupling))

    def _calculate_love_transfer(
        self,
        coords_a: Coordinates,
        coords_b: Coordinates
    ) -> float:
        """
        Calculate love transfer - how well connection quality flows.

        Based on the observation that Love amplifies all dimensions.
        """
        # Average Love between services
        avg_love = (coords_a.love + coords_b.love) / 2

        # Love transfer is enhanced when both have moderate-to-high Love
        # and diminished when either has very low Love
        min_love = min(coords_a.love, coords_b.love)

        # Transfer efficiency (bottlenecked by lower Love)
        transfer = avg_love * (0.5 + 0.5 * min_love)

        return min(1.0, transfer)

    def _get_affinity_level(self, score: float) -> AffinityLevel:
        """Map affinity score to level"""
        if score > 0.8:
            return AffinityLevel.EXCELLENT
        elif score > 0.6:
            return AffinityLevel.GOOD
        elif score > 0.4:
            return AffinityLevel.MODERATE
        elif score > 0.2:
            return AffinityLevel.NEEDS_ATTENTION
        else:
            return AffinityLevel.POOR

    def _determine_relationship_type(
        self,
        coords_a: Coordinates,
        coords_b: Coordinates,
        affinity: float
    ) -> RelationshipType:
        """Determine the type of relationship between services"""
        # Get dominant dimensions
        dims_a = {'L': coords_a.love, 'J': coords_a.justice,
                  'P': coords_a.power, 'W': coords_a.wisdom}
        dims_b = {'L': coords_b.love, 'J': coords_b.justice,
                  'P': coords_b.power, 'W': coords_b.wisdom}

        dom_a = max(dims_a, key=dims_a.get)
        dom_b = max(dims_b, key=dims_b.get)

        distance = math.sqrt(
            (coords_a.love - coords_b.love) ** 2 +
            (coords_a.justice - coords_b.justice) ** 2 +
            (coords_a.power - coords_b.power) ** 2 +
            (coords_a.wisdom - coords_b.wisdom) ** 2
        )

        # Harmonious: Similar profiles, high affinity
        if distance < 0.3 and affinity > 0.6:
            return RelationshipType.HARMONIOUS

        # Complementary: Different but balancing
        if dom_a != dom_b and affinity > 0.4:
            return RelationshipType.COMPLEMENTARY

        # Competitive: Same dominant dimension, similar profiles
        if dom_a == dom_b and distance < 0.5:
            return RelationshipType.COMPETITIVE

        # Dependent: One has high Love (connector), other doesn't
        if abs(coords_a.love - coords_b.love) > 0.4:
            return RelationshipType.DEPENDENT

        # Isolated: Low affinity, distant in space
        if affinity < 0.3:
            return RelationshipType.ISOLATED

        # Default
        return RelationshipType.COMPLEMENTARY

    def _generate_affinity_description(
        self,
        service_a: str,
        service_b: str,
        level: AffinityLevel,
        rel_type: RelationshipType
    ) -> str:
        """Generate human-readable description"""
        descriptions = {
            AffinityLevel.EXCELLENT: f"{service_a} and {service_b} have excellent affinity",
            AffinityLevel.GOOD: f"{service_a} and {service_b} work well together",
            AffinityLevel.MODERATE: f"{service_a} and {service_b} have moderate compatibility",
            AffinityLevel.NEEDS_ATTENTION: f"Relationship between {service_a} and {service_b} needs attention",
            AffinityLevel.POOR: f"{service_a} and {service_b} have poor compatibility",
        }

        type_context = {
            RelationshipType.HARMONIOUS: " - they operate harmoniously",
            RelationshipType.COMPLEMENTARY: " - they complement each other's capabilities",
            RelationshipType.DEPENDENT: " - there's a dependency relationship",
            RelationshipType.COMPETITIVE: " - potential competition for resources",
            RelationshipType.BRIDGE: " - one bridges different clusters",
            RelationshipType.ISOLATED: " - minimal interaction",
        }

        return descriptions[level] + type_context[rel_type]

    def _generate_affinity_recommendations(
        self,
        coords_a: Coordinates,
        coords_b: Coordinates,
        level: AffinityLevel,
        rel_type: RelationshipType
    ) -> List[str]:
        """Generate recommendations for improving affinity"""
        recommendations = []

        # Low Love on either side
        if coords_a.love < 0.3 or coords_b.love < 0.3:
            recommendations.append(
                "Consider improving connectivity (Love) to enhance relationship"
            )

        # Needs attention
        if level in [AffinityLevel.NEEDS_ATTENTION, AffinityLevel.POOR]:
            recommendations.append(
                "Review if these services need to interact - if yes, improve integration"
            )

        # Competitive relationship
        if rel_type == RelationshipType.COMPETITIVE:
            recommendations.append(
                "Consider load balancing or role differentiation to reduce competition"
            )

        # Dependency without redundancy
        if rel_type == RelationshipType.DEPENDENT:
            recommendations.append(
                "Evaluate dependency direction and consider adding redundancy"
            )

        # Justice misalignment
        if abs(coords_a.justice - coords_b.justice) > 0.3:
            recommendations.append(
                "Security/policy misalignment detected - review access controls"
            )

        return recommendations

    # ==================== HARMONY MESH ====================

    def get_harmony_mesh(self, network_state: Optional[Dict] = None) -> HarmonyMesh:
        """
        Generate harmony overlay for all connections.

        Creates a mesh showing semantic harmony between all communicating pairs.
        """
        nodes = {}
        edges = []
        harmony_distribution = {'excellent': 0, 'good': 0, 'moderate': 0,
                                'poor': 0, 'very_poor': 0}

        # Build nodes
        for service, coords in self.profiles.items():
            connections = list(self.connections.get(service, set()))
            total_harmony = 0.0

            # Calculate harmony with each connection
            for connected in connections:
                if connected in self.profiles:
                    affinity = self.calculate_affinity(service, connected)
                    harmony = affinity.harmonic_resonance
                    total_harmony += harmony

                    # Add edge (avoid duplicates)
                    edge_key = tuple(sorted([service, connected]))
                    if edge_key not in [(e[0], e[1]) for e in edges]:
                        edges.append((edge_key[0], edge_key[1], harmony))

                        # Track distribution
                        if harmony > 0.8:
                            harmony_distribution['excellent'] += 1
                        elif harmony > 0.6:
                            harmony_distribution['good'] += 1
                        elif harmony > 0.4:
                            harmony_distribution['moderate'] += 1
                        elif harmony > 0.2:
                            harmony_distribution['poor'] += 1
                        else:
                            harmony_distribution['very_poor'] += 1

            avg_harmony = total_harmony / len(connections) if connections else 0.0

            # Determine role
            role = self._determine_node_role(service, connections, avg_harmony)

            nodes[service] = HarmonyMeshNode(
                service=service,
                coordinates=coords,
                connections=connections,
                total_harmony=total_harmony,
                avg_harmony=avg_harmony,
                role=role
            )

        # Calculate global harmony
        if edges:
            global_harmony = sum(e[2] for e in edges) / len(edges)
        else:
            global_harmony = 0.0

        # Find hubs (highly connected, high harmony)
        hubs = [
            name for name, node in nodes.items()
            if len(node.connections) >= 3 and node.avg_harmony > 0.6
        ]

        # Find bridges
        bridges = [
            name for name, node in nodes.items()
            if node.role == "Bridge"
        ]

        # Find weak links
        weak_links = [
            (e[0], e[1]) for e in edges
            if e[2] < 0.4
        ]

        return HarmonyMesh(
            nodes=nodes,
            edges=edges,
            global_harmony=global_harmony,
            harmony_distribution=harmony_distribution,
            hubs=hubs,
            bridges=bridges,
            weak_links=weak_links
        )

    def _determine_node_role(
        self,
        service: str,
        connections: List[str],
        avg_harmony: float
    ) -> str:
        """Determine the role of a node in the harmony mesh"""
        num_connections = len(connections)

        if num_connections == 0:
            return "Isolated"
        elif num_connections == 1:
            return "Leaf"
        elif num_connections >= 4 and avg_harmony > 0.6:
            return "Hub"
        elif num_connections >= 2 and avg_harmony < 0.5:
            return "Bridge"  # Connects but with lower harmony (bridging clusters)
        else:
            return "Member"

    # ==================== INTEGRATION HEALTH ====================

    def calculate_integration_health(
        self,
        source: str,
        target: str
    ) -> IntegrationHealth:
        """
        Measure how well systems connect - quality, not just existence.

        Analyzes all four LJPW dimensions to assess integration health.
        """
        coords_source = self.profiles.get(source)
        coords_target = self.profiles.get(target)

        if not coords_source or not coords_target:
            return IntegrationHealth(
                source=source,
                target=target,
                health_score=0.0,
                love_index=0.0,
                justice_alignment=0.0,
                power_balance=0.0,
                wisdom_flow=0.0,
                bottleneck_risk=1.0,
                recommendations=["Profile both services to assess integration health"]
            )

        # Love Index: Connection quality
        love_index = self._calculate_love_transfer(coords_source, coords_target)

        # Justice Alignment: Policy/rule compatibility
        justice_diff = abs(coords_source.justice - coords_target.justice)
        justice_alignment = 1.0 - justice_diff

        # Power Balance: Capacity balance (avoid bottlenecks)
        power_diff = abs(coords_source.power - coords_target.power)
        power_balance = 1.0 - power_diff

        # Wisdom Flow: Information sharing quality
        wisdom_flow = (coords_source.wisdom + coords_target.wisdom) / 2

        # Bottleneck Risk: Higher if power is unbalanced
        bottleneck_risk = power_diff * (1.0 - min(coords_source.power, coords_target.power))

        # Overall health score
        health_score = (
            0.35 * love_index +
            0.25 * justice_alignment +
            0.25 * power_balance +
            0.15 * wisdom_flow
        )

        # Generate recommendations
        recommendations = []

        if love_index < 0.4:
            recommendations.append(
                "Improve connection quality - consider better protocols or middleware"
            )

        if justice_alignment < 0.4:
            recommendations.append(
                "Security policy misalignment - harmonize access controls"
            )

        if power_balance < 0.4:
            recommendations.append(
                "Capacity imbalance - risk of bottleneck at lower-power service"
            )

        if wisdom_flow < 0.4:
            recommendations.append(
                "Poor information flow - add monitoring/logging between services"
            )

        if bottleneck_risk > 0.6:
            recommendations.append(
                "High bottleneck risk - consider load balancing or scaling"
            )

        return IntegrationHealth(
            source=source,
            target=target,
            health_score=health_score,
            love_index=love_index,
            justice_alignment=justice_alignment,
            power_balance=power_balance,
            wisdom_flow=wisdom_flow,
            bottleneck_risk=bottleneck_risk,
            recommendations=recommendations
        )

    # ==================== BRIDGE DETECTION ====================

    def detect_bridges(self, topology: Optional[Dict] = None) -> List[Bridge]:
        """
        Find components bridging disconnected semantic clusters.

        Bridges are critical for network connectivity but can also
        be single points of failure.
        """
        # First, cluster the services semantically
        clusters = self._cluster_services()

        bridges = []

        for service, connections in self.connections.items():
            if service not in self.profiles:
                continue

            # Find which clusters this service's connections belong to
            connected_clusters = set()
            service_cluster = None

            for cluster_id, cluster_members in clusters.items():
                if service in cluster_members:
                    service_cluster = cluster_id
                for connected in connections:
                    if connected in cluster_members:
                        connected_clusters.add(cluster_id)

            # If connected to multiple clusters, it's a bridge
            if len(connected_clusters) > 1:
                # Calculate bridge strength
                # Higher if it's the only path between clusters
                redundancy = self._calculate_bridge_redundancy(
                    service, connected_clusters, clusters
                )
                bridge_strength = 1.0 - redundancy

                bridges.append(Bridge(
                    service=service,
                    clusters_connected=list(connected_clusters),
                    bridge_strength=bridge_strength,
                    redundancy=redundancy,
                    coordinates=self.profiles[service],
                    description=f"Bridges {len(connected_clusters)} semantic clusters"
                ))

        # Sort by bridge strength (most critical first)
        bridges.sort(key=lambda b: b.bridge_strength, reverse=True)

        return bridges

    def _cluster_services(self) -> Dict[int, Set[str]]:
        """Simple semantic clustering of services"""
        clusters: Dict[int, Set[str]] = {}
        unclustered = set(self.profiles.keys())
        cluster_id = 0

        while unclustered:
            seed = next(iter(unclustered))
            cluster = {seed}

            # Find all services within semantic distance threshold
            for service in list(unclustered):
                if service == seed:
                    continue
                affinity = self.calculate_affinity(seed, service)
                if affinity.affinity_score > 0.5:
                    cluster.add(service)

            clusters[cluster_id] = cluster
            unclustered -= cluster
            cluster_id += 1

        return clusters

    def _calculate_bridge_redundancy(
        self,
        bridge_service: str,
        connected_clusters: Set[int],
        clusters: Dict[int, Set[str]]
    ) -> float:
        """Calculate how many alternative paths exist"""
        # Count other services that also bridge these clusters
        other_bridges = 0

        for service, connections in self.connections.items():
            if service == bridge_service:
                continue

            service_clusters = set()
            for cluster_id, members in clusters.items():
                for connected in connections:
                    if connected in members:
                        service_clusters.add(cluster_id)

            # If this service bridges the same clusters
            if connected_clusters.issubset(service_clusters):
                other_bridges += 1

        # Redundancy increases with alternative paths
        return min(1.0, other_bridges / 3)  # Cap at 3 alternatives for full redundancy

    # ==================== LOVE DEBT TRACKING ====================

    def track_love_debt(self, historical_data: Optional[List[Dict]] = None) -> List[LoveDebt]:
        """
        Track degraded relationships as technical debt.

        Love debt accumulates when:
        - Connection quality degrades over time
        - Services become isolated
        - Integration health declines
        """
        debts = []

        for service in self.profiles:
            connections = self.connections.get(service, set())
            degraded = []
            symptoms = []
            root_causes = []
            debt_score = 0.0

            # Check affinity with each connection
            for connected in connections:
                affinity = self.calculate_affinity(service, connected)
                if affinity.affinity_level in [AffinityLevel.NEEDS_ATTENTION, AffinityLevel.POOR]:
                    degraded.append(connected)
                    debt_score += (1.0 - affinity.affinity_score)

            # Check for isolation
            if len(connections) == 0:
                debt_score += 0.5
                symptoms.append("Service is isolated - no connections")
                root_causes.append("Missing integrations or deprecated service")

            # Check Love dimension
            coords = self.profiles[service]
            if coords.love < 0.3:
                debt_score += 0.3
                symptoms.append("Low Love dimension - poor connectivity characteristic")
                root_causes.append("Service design doesn't prioritize relationships")

            # Generate symptoms and causes for degraded relationships
            if degraded:
                symptoms.append(f"{len(degraded)} degraded relationships")
                root_causes.append("Semantic drift from connected services")

            if debt_score > 0:
                # Calculate priority
                priority = 1 if debt_score > 0.8 else 2 if debt_score > 0.5 else 3

                # Estimate impact
                if debt_score > 0.8:
                    impact = "Critical - may cause cascading failures"
                elif debt_score > 0.5:
                    impact = "High - degraded system performance likely"
                elif debt_score > 0.3:
                    impact = "Moderate - reduced reliability"
                else:
                    impact = "Low - minor integration issues"

                debts.append(LoveDebt(
                    service=service,
                    debt_score=debt_score,
                    degraded_relationships=degraded,
                    symptoms=symptoms,
                    root_causes=root_causes,
                    remediation_priority=priority,
                    estimated_impact=impact
                ))

        # Sort by priority
        debts.sort(key=lambda d: d.remediation_priority)

        return debts

    # ==================== RESONANCE HELPERS ====================

    def resonate_relationship(
        self,
        service_a: str,
        service_b: str,
        cycles: int = 100
    ) -> Dict:
        """
        Run resonance cycles between two services to predict
        how their relationship will evolve.
        """
        coords_a = self.profiles.get(service_a)
        coords_b = self.profiles.get(service_b)

        if not coords_a or not coords_b:
            return {"error": "Missing service profiles"}

        state_a = [coords_a.love, coords_a.justice, coords_a.power, coords_a.wisdom]
        state_b = [coords_b.love, coords_b.justice, coords_b.power, coords_b.wisdom]

        history = []
        dt = 0.05

        for cycle in range(cycles):
            # Calculate harmony
            distance = math.sqrt(sum((state_a[i] - state_b[i])**2 for i in range(4)))
            harmony = 1.0 / (1.0 + distance)

            # Apply coupling
            kappa = 0.5 + harmony

            # Inter-service coupling
            new_state_a = [
                state_a[i] + dt * kappa * (
                    sum(COUPLING_MATRIX[i][j] * state_b[j] for j in range(4)) - state_a[i]
                ) * 0.1
                for i in range(4)
            ]

            new_state_b = [
                state_b[i] + dt * kappa * (
                    sum(COUPLING_MATRIX[i][j] * state_a[j] for j in range(4)) - state_b[i]
                ) * 0.1
                for i in range(4)
            ]

            # Clip to [0, 1]
            state_a = [max(0.0, min(1.0, x)) for x in new_state_a]
            state_b = [max(0.0, min(1.0, x)) for x in new_state_b]

            if cycle % 10 == 0:
                history.append({
                    'cycle': cycle,
                    'state_a': state_a.copy(),
                    'state_b': state_b.copy(),
                    'harmony': harmony
                })

        final_distance = math.sqrt(sum((state_a[i] - state_b[i])**2 for i in range(4)))
        final_harmony = 1.0 / (1.0 + final_distance)

        return {
            'initial_harmony': history[0]['harmony'] if history else 0,
            'final_harmony': final_harmony,
            'converged': final_distance < 0.1,
            'trajectory': 'converging' if final_harmony > history[0]['harmony'] else 'diverging',
            'final_state_a': state_a,
            'final_state_b': state_b,
            'history': history
        }
