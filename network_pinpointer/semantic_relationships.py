#!/usr/bin/env python3
"""
Semantic Relationships - 4D Space Relationship Analysis

Analyzes relationships between systems in LJPW 4D space:
- Semantic distance calculation
- Similar system detection
- Outlier identification
- Semantic clustering
- Compatibility scoring
"""

import math
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Set
from collections import defaultdict

from .semantic_engine import Coordinates
from .semantic_probe import SemanticProfile


@dataclass
class SemanticRelationship:
    """Relationship between two systems in semantic space"""
    source: str
    target: str
    distance: float
    relationship_type: str  # "SIMILAR", "COMPLEMENTARY", "DIFFERENT", "INCOMPATIBLE"
    compatibility_score: float  # 0.0-1.0
    description: str


@dataclass
class SemanticCluster:
    """A cluster of semantically similar systems"""
    cluster_id: int
    name: str
    systems: List[str] = field(default_factory=list)
    centroid: Optional[Coordinates] = None
    radius: float = 0.0
    cohesion: float = 0.0  # 0.0-1.0, how tight the cluster is
    dominant_dimension: str = "unknown"
    characteristics: List[str] = field(default_factory=list)


@dataclass
class OutlierAnalysis:
    """Analysis of a semantic outlier"""
    system: str
    coords: Coordinates
    isolation_score: float  # 0.0-1.0, higher = more isolated
    nearest_neighbor: Optional[str] = None
    nearest_distance: float = float('inf')
    cluster_assignment: Optional[int] = None
    reasons: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


class SemanticRelationshipAnalyzer:
    """Analyze relationships between systems in 4D LJPW space"""
    
    # Distance thresholds for relationship classification
    VERY_SIMILAR = 0.2
    SIMILAR = 0.5
    DIFFERENT = 1.0
    VERY_DIFFERENT = 1.5
    
    def __init__(self):
        self.profiles: Dict[str, SemanticProfile] = {}
    
    def add_profile(self, profile: SemanticProfile):
        """Add a system profile for analysis"""
        if profile.ljpw_coordinates:
            self.profiles[profile.target] = profile
    
    def add_profiles(self, profiles: List[SemanticProfile]):
        """Add multiple profiles"""
        for profile in profiles:
            self.add_profile(profile)
    
    # ==================== SEMANTIC DISTANCE ====================
    
    def calculate_distance(self, coords1: Coordinates, coords2: Coordinates) -> float:
        """
        Calculate Euclidean distance in 4D LJPW space.
        
        Returns distance (0.0 = identical, 2.0 = maximum difference)
        """
        return math.sqrt(
            (coords1.love - coords2.love) ** 2 +
            (coords1.justice - coords2.justice) ** 2 +
            (coords1.power - coords2.power) ** 2 +
            (coords1.wisdom - coords2.wisdom) ** 2
        )
    
    def get_distance_between_systems(self, system1: str, system2: str) -> Optional[float]:
        """Get semantic distance between two systems"""
        if system1 not in self.profiles or system2 not in self.profiles:
            return None
        
        coords1 = self.profiles[system1].ljpw_coordinates
        coords2 = self.profiles[system2].ljpw_coordinates
        
        if not coords1 or not coords2:
            return None
        
        return self.calculate_distance(coords1, coords2)
    
    # ==================== SIMILAR SYSTEMS ====================
    
    def find_similar_systems(
        self, 
        target: str, 
        threshold: float = SIMILAR,
        limit: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Find systems similar to target.
        
        Args:
            target: Target system name
            threshold: Maximum distance to consider similar
            limit: Maximum number of results
        
        Returns:
            List of (system_name, distance) tuples, sorted by distance
        """
        if target not in self.profiles:
            return []
        
        target_coords = self.profiles[target].ljpw_coordinates
        if not target_coords:
            return []
        
        similarities = []
        
        for system_name, profile in self.profiles.items():
            if system_name == target:
                continue
            
            if not profile.ljpw_coordinates:
                continue
            
            distance = self.calculate_distance(target_coords, profile.ljpw_coordinates)
            
            if distance <= threshold:
                similarities.append((system_name, distance))
        
        # Sort by distance (closest first)
        similarities.sort(key=lambda x: x[1])
        
        return similarities[:limit]
    
    def find_most_similar_pair(self) -> Optional[Tuple[str, str, float]]:
        """Find the two most similar systems in the network"""
        min_distance = float('inf')
        best_pair = None
        
        systems = list(self.profiles.keys())
        
        for i, sys1 in enumerate(systems):
            for sys2 in systems[i+1:]:
                distance = self.get_distance_between_systems(sys1, sys2)
                
                if distance is not None and distance < min_distance:
                    min_distance = distance
                    best_pair = (sys1, sys2, distance)
        
        return best_pair
    
    def get_similarity_matrix(self) -> Dict[str, Dict[str, float]]:
        """
        Create distance matrix for all systems.
        
        Returns:
            Nested dict: matrix[system1][system2] = distance
        """
        matrix = {}
        systems = list(self.profiles.keys())
        
        for sys1 in systems:
            matrix[sys1] = {}
            for sys2 in systems:
                if sys1 == sys2:
                    matrix[sys1][sys2] = 0.0
                else:
                    distance = self.get_distance_between_systems(sys1, sys2)
                    matrix[sys1][sys2] = distance if distance is not None else float('inf')
        
        return matrix
    
    # ==================== OUTLIER DETECTION ====================
    
    def detect_outliers(
        self, 
        threshold: float = 1.0,
        min_neighbors: int = 1
    ) -> List[OutlierAnalysis]:
        """
        Detect semantic outliers - systems that are isolated in LJPW space.
        
        Args:
            threshold: Distance threshold for considering a neighbor
            min_neighbors: Minimum neighbors to not be an outlier
        
        Returns:
            List of outlier analyses
        """
        outliers = []
        
        for system_name, profile in self.profiles.items():
            if not profile.ljpw_coordinates:
                continue
            
            # Find neighbors within threshold
            neighbors = self.find_similar_systems(system_name, threshold=threshold, limit=100)
            
            # Calculate isolation score
            if len(neighbors) == 0:
                isolation_score = 1.0
                nearest_neighbor = None
                nearest_distance = float('inf')
            else:
                isolation_score = 1.0 - (len(neighbors) / len(self.profiles))
                nearest_neighbor = neighbors[0][0]
                nearest_distance = neighbors[0][1]
            
            # Determine if outlier
            if len(neighbors) < min_neighbors:
                reasons = self._identify_outlier_reasons(profile, neighbors)
                recommendations = self._generate_outlier_recommendations(profile, reasons)
                
                outliers.append(OutlierAnalysis(
                    system=system_name,
                    coords=profile.ljpw_coordinates,
                    isolation_score=isolation_score,
                    nearest_neighbor=nearest_neighbor,
                    nearest_distance=nearest_distance,
                    cluster_assignment=None,
                    reasons=reasons,
                    recommendations=recommendations
                ))
        
        # Sort by isolation score (most isolated first)
        outliers.sort(key=lambda x: x.isolation_score, reverse=True)
        
        return outliers
    
    def _identify_outlier_reasons(
        self, 
        profile: SemanticProfile, 
        neighbors: List[Tuple[str, float]]
    ) -> List[str]:
        """Identify why a system is an outlier"""
        reasons = []
        coords = profile.ljpw_coordinates
        
        # Check for extreme values
        if coords.love > 0.9:
            reasons.append("Extremely high Love (accessibility) - very public")
        elif coords.love < 0.1:
            reasons.append("Extremely low Love - very isolated")
        
        if coords.justice > 0.9:
            reasons.append("Extremely high Justice - very secure/restricted")
        elif coords.justice < 0.1:
            reasons.append("Extremely low Justice - minimal security")
        
        if coords.power > 0.9:
            reasons.append("Extremely high Power - very high performance")
        elif coords.power < 0.1:
            reasons.append("Extremely low Power - minimal processing")
        
        if coords.wisdom > 0.9:
            reasons.append("Extremely high Wisdom - heavily monitored")
        elif coords.wisdom < 0.1:
            reasons.append("Extremely low Wisdom - no monitoring")
        
        # Check for unique archetype
        if profile.matched_archetypes:
            archetype = profile.matched_archetypes[0][0].name
            reasons.append(f"Unique archetype: {archetype}")
        
        # Check if no neighbors
        if len(neighbors) == 0:
            reasons.append("No semantically similar systems found")
        
        return reasons
    
    def _generate_outlier_recommendations(
        self, 
        profile: SemanticProfile, 
        reasons: List[str]
    ) -> List[str]:
        """Generate recommendations for outliers"""
        recommendations = []
        
        if "No semantically similar systems found" in reasons:
            recommendations.append("Verify this system's configuration is intentional")
            recommendations.append("Consider if this system should exist")
        
        if "minimal security" in str(reasons).lower():
            recommendations.append("Review security posture - appears vulnerable")
        
        if "very isolated" in str(reasons).lower():
            recommendations.append("Verify system is accessible to required services")
        
        if "no monitoring" in str(reasons).lower():
            recommendations.append("Add monitoring and observability")
        
        recommendations.append("Review system against architecture documentation")
        
        return recommendations
    
    # ==================== CLUSTERING ====================
    
    def cluster_systems(
        self, 
        max_distance: float = 0.5,
        min_cluster_size: int = 2
    ) -> List[SemanticCluster]:
        """
        Cluster systems using simple distance-based clustering.
        
        Uses a greedy algorithm:
        1. Start with unclustered systems
        2. For each system, find all neighbors within max_distance
        3. Create cluster if enough neighbors
        4. Repeat until all systems processed
        
        Args:
            max_distance: Maximum distance for systems in same cluster
            min_cluster_size: Minimum systems to form a cluster
        
        Returns:
            List of semantic clusters
        """
        clusters = []
        unclustered = set(self.profiles.keys())
        cluster_id = 0
        
        while unclustered:
            # Pick a seed system
            seed = next(iter(unclustered))
            
            # Find all neighbors within distance
            neighbors = self.find_similar_systems(seed, threshold=max_distance, limit=100)
            cluster_members = {seed}
            
            for neighbor, distance in neighbors:
                if neighbor in unclustered:
                    cluster_members.add(neighbor)
            
            # Create cluster if large enough
            if len(cluster_members) >= min_cluster_size:
                cluster = self._create_cluster(cluster_id, list(cluster_members))
                clusters.append(cluster)
                cluster_id += 1
                
                # Remove from unclustered
                unclustered -= cluster_members
            else:
                # Single system, remove from unclustered
                unclustered.remove(seed)
        
        return clusters
    
    def _create_cluster(self, cluster_id: int, members: List[str]) -> SemanticCluster:
        """Create a semantic cluster from members"""
        # Calculate centroid
        all_coords = [
            self.profiles[member].ljpw_coordinates 
            for member in members 
            if self.profiles[member].ljpw_coordinates
        ]
        
        if not all_coords:
            return SemanticCluster(
                cluster_id=cluster_id,
                name=f"Cluster {cluster_id}",
                systems=members
            )
        
        centroid = Coordinates(
            love=sum(c.love for c in all_coords) / len(all_coords),
            justice=sum(c.justice for c in all_coords) / len(all_coords),
            power=sum(c.power for c in all_coords) / len(all_coords),
            wisdom=sum(c.wisdom for c in all_coords) / len(all_coords)
        )
        
        # Calculate radius (max distance from centroid)
        radius = max(
            self.calculate_distance(centroid, coords)
            for coords in all_coords
        )
        
        # Calculate cohesion (inverse of average distance from centroid)
        avg_distance = sum(
            self.calculate_distance(centroid, coords)
            for coords in all_coords
        ) / len(all_coords)
        
        cohesion = 1.0 - min(1.0, avg_distance)
        
        # Determine dominant dimension
        dims = {
            'Love': centroid.love,
            'Justice': centroid.justice,
            'Power': centroid.power,
            'Wisdom': centroid.wisdom
        }
        dominant_dimension = max(dims, key=dims.get)
        
        # Generate cluster name based on dominant dimension
        cluster_names = {
            'Love': 'Public Services',
            'Justice': 'Security Systems',
            'Power': 'Performance Systems',
            'Wisdom': 'Monitoring Systems'
        }
        name = cluster_names.get(dominant_dimension, f"Cluster {cluster_id}")
        
        # Generate characteristics
        characteristics = self._generate_cluster_characteristics(centroid, dominant_dimension)
        
        return SemanticCluster(
            cluster_id=cluster_id,
            name=name,
            systems=members,
            centroid=centroid,
            radius=radius,
            cohesion=cohesion,
            dominant_dimension=dominant_dimension,
            characteristics=characteristics
        )
    
    def _generate_cluster_characteristics(
        self, 
        centroid: Coordinates, 
        dominant: str
    ) -> List[str]:
        """Generate characteristics for a cluster"""
        characteristics = []
        
        if dominant == 'Love':
            if centroid.love > 0.7:
                characteristics.append("High accessibility - public-facing services")
            if centroid.justice > 0.4:
                characteristics.append("Balanced security posture")
        
        elif dominant == 'Justice':
            if centroid.justice > 0.7:
                characteristics.append("Strong security controls")
            if centroid.love < 0.3:
                characteristics.append("Restricted access")
        
        elif dominant == 'Power':
            if centroid.power > 0.7:
                characteristics.append("High-performance systems")
            if centroid.love < 0.5:
                characteristics.append("Backend processing focus")
        
        elif dominant == 'Wisdom':
            if centroid.wisdom > 0.7:
                characteristics.append("Monitoring and observability focus")
            if centroid.power < 0.5:
                characteristics.append("Information gathering over processing")
        
        # Overall balance
        variance = sum([
            (centroid.love - 0.5) ** 2,
            (centroid.justice - 0.5) ** 2,
            (centroid.power - 0.5) ** 2,
            (centroid.wisdom - 0.5) ** 2
        ]) / 4
        
        if variance < 0.05:
            characteristics.append("Well-balanced across all dimensions")
        
        return characteristics
    
    # ==================== RELATIONSHIP ANALYSIS ====================
    
    def analyze_relationship(self, system1: str, system2: str) -> Optional[SemanticRelationship]:
        """Analyze relationship between two systems"""
        distance = self.get_distance_between_systems(system1, system2)
        
        if distance is None:
            return None
        
        # Classify relationship
        if distance < self.VERY_SIMILAR:
            relationship_type = "VERY_SIMILAR"
            description = "Systems are very similar - potential redundancy or clustering"
        elif distance < self.SIMILAR:
            relationship_type = "SIMILAR"
            description = "Systems are similar - likely same tier or purpose"
        elif distance < self.DIFFERENT:
            relationship_type = "COMPLEMENTARY"
            description = "Systems are different but may work together"
        elif distance < self.VERY_DIFFERENT:
            relationship_type = "DIFFERENT"
            description = "Systems are quite different - different tiers or purposes"
        else:
            relationship_type = "INCOMPATIBLE"
            description = "Systems are very different - unlikely to interact"
        
        # Calculate compatibility (inverse of distance, normalized)
        compatibility_score = max(0.0, 1.0 - (distance / 2.0))
        
        return SemanticRelationship(
            source=system1,
            target=system2,
            distance=distance,
            relationship_type=relationship_type,
            compatibility_score=compatibility_score,
            description=description
        )
    
    def get_network_summary(self) -> Dict:
        """Get summary statistics for the network"""
        if not self.profiles:
            return {}
        
        # Calculate centroid
        all_coords = [
            p.ljpw_coordinates 
            for p in self.profiles.values() 
            if p.ljpw_coordinates
        ]
        
        if not all_coords:
            return {}
        
        centroid = Coordinates(
            love=sum(c.love for c in all_coords) / len(all_coords),
            justice=sum(c.justice for c in all_coords) / len(all_coords),
            power=sum(c.power for c in all_coords) / len(all_coords),
            wisdom=sum(c.wisdom for c in all_coords) / len(all_coords)
        )
        
        # Calculate diameter (max distance between any two systems)
        max_distance = 0.0
        systems = list(self.profiles.keys())
        
        for i, sys1 in enumerate(systems):
            for sys2 in systems[i+1:]:
                distance = self.get_distance_between_systems(sys1, sys2)
                if distance and distance > max_distance:
                    max_distance = distance
        
        # Calculate average distance from centroid (radius)
        avg_distance_from_centroid = sum(
            self.calculate_distance(centroid, coords)
            for coords in all_coords
        ) / len(all_coords)
        
        return {
            'total_systems': len(self.profiles),
            'centroid': centroid,
            'diameter': max_distance,
            'radius': avg_distance_from_centroid,
            'density': 1.0 - min(1.0, avg_distance_from_centroid),
        }
