#!/usr/bin/env python3
"""
Service Archetypes - Predefined LJPW Patterns for Network Services

Defines common network service archetypes with their semantic signatures,
enabling automatic classification and purpose inference.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from .semantic_engine import Coordinates


@dataclass
class ServiceArchetype:
    """Predefined semantic pattern for network services"""
    
    name: str
    description: str
    ljpw_signature: Dict[str, Tuple[float, float]]  # dimension: (min, max)
    typical_services: List[str]
    typical_ports: List[int]
    purpose: str
    characteristics: List[str]
    examples: List[str]
    confidence_threshold: float = 0.7
    
    def matches(self, coords: Coordinates) -> float:
        """
        Calculate confidence that given coordinates match this archetype.
        
        Returns confidence score 0.0-1.0
        """
        l, j, p, w = coords.love, coords.justice, coords.power, coords.wisdom
        
        # Check if coordinates fall within signature ranges
        matches = 0
        total = 0
        
        for dim, (min_val, max_val) in self.ljpw_signature.items():
            total += 1
            if dim.lower() == 'love':
                if min_val <= l <= max_val:
                    matches += 1
            elif dim.lower() == 'justice':
                if min_val <= j <= max_val:
                    matches += 1
            elif dim.lower() == 'power':
                if min_val <= p <= max_val:
                    matches += 1
            elif dim.lower() == 'wisdom':
                if min_val <= w <= max_val:
                    matches += 1
        
        # Calculate base confidence from dimension matching
        base_confidence = matches / total if total > 0 else 0.0
        
        # Bonus for strong matches (coordinates near center of range)
        bonus = 0.0
        for dim, (min_val, max_val) in self.ljpw_signature.items():
            center = (min_val + max_val) / 2
            range_size = max_val - min_val
            
            if dim.lower() == 'love':
                distance = abs(l - center)
            elif dim.lower() == 'justice':
                distance = abs(j - center)
            elif dim.lower() == 'power':
                distance = abs(p - center)
            elif dim.lower() == 'wisdom':
                distance = abs(w - center)
            else:
                continue
            
            # Closer to center = higher bonus
            if range_size > 0:
                bonus += (1.0 - (distance / (range_size / 2))) * 0.1
        
        confidence = min(1.0, base_confidence + (bonus / 4))
        return confidence


# Define standard archetypes
ARCHETYPES = [
    ServiceArchetype(
        name="The Public Gateway",
        description="High-availability public service optimized for connectivity",
        ljpw_signature={
            'love': (0.6, 1.0),      # High connectivity
            'justice': (0.2, 0.5),   # Moderate security
            'power': (0.5, 0.9),     # Good performance
            'wisdom': (0.1, 0.4),    # Low monitoring exposure
        },
        typical_services=['HTTP', 'HTTPS', 'CDN'],
        typical_ports=[80, 443, 8080, 8443],
        purpose="Public content delivery and service access",
        characteristics=[
            "High availability focus",
            "Optimized for public connectivity",
            "Balanced security posture",
            "Designed for scale and performance",
        ],
        examples=["google.com", "cloudflare.com", "cdn.example.com"],
    ),
    
    ServiceArchetype(
        name="The Security Sentinel",
        description="Access control and security enforcement system",
        ljpw_signature={
            'love': (0.0, 0.3),      # Low connectivity
            'justice': (0.7, 1.0),   # High security
            'power': (0.3, 0.6),     # Moderate control
            'wisdom': (0.2, 0.5),    # Some monitoring
        },
        typical_services=['SSH', 'VPN', 'Firewall'],
        typical_ports=[22, 1194, 1723],
        purpose="Security enforcement and access control",
        characteristics=[
            "Strict access policies",
            "Minimal exposed services",
            "Authentication required",
            "Security-first design",
        ],
        examples=["firewall.corp.local", "bastion.example.com", "vpn-gateway"],
    ),
    
    ServiceArchetype(
        name="The Data Vault",
        description="Database and data storage system",
        ljpw_signature={
            'love': (0.2, 0.5),      # Limited connectivity
            'justice': (0.4, 0.7),   # Moderate-high security
            'power': (0.6, 1.0),     # High performance
            'wisdom': (0.1, 0.4),    # Low monitoring exposure
        },
        typical_services=['MySQL', 'PostgreSQL', 'MongoDB', 'Redis'],
        typical_ports=[3306, 5432, 27017, 6379],
        purpose="Data storage, management, and retrieval",
        characteristics=[
            "Restricted access patterns",
            "High performance requirements",
            "Data integrity focus",
            "Backend service orientation",
        ],
        examples=["db.example.com", "postgres-primary", "redis-cache"],
    ),
    
    ServiceArchetype(
        name="The Performance Engine",
        description="Application server and compute node",
        ljpw_signature={
            'love': (0.4, 0.7),      # Moderate connectivity
            'justice': (0.2, 0.5),   # Moderate security
            'power': (0.7, 1.0),     # Very high performance
            'wisdom': (0.1, 0.3),    # Low monitoring
        },
        typical_services=['Application Server', 'Compute Node', 'API'],
        typical_ports=[8080, 8443, 9000, 3000],
        purpose="Processing, execution, and computation",
        characteristics=[
            "High computational capacity",
            "Optimized for throughput",
            "Resource-intensive operations",
            "Backend processing focus",
        ],
        examples=["app-server-01", "compute-node", "api.example.com"],
    ),
    
    ServiceArchetype(
        name="The Monitoring Hub",
        description="Monitoring, logging, and observability system",
        ljpw_signature={
            'love': (0.3, 0.6),      # Moderate connectivity
            'justice': (0.2, 0.5),   # Moderate security
            'power': (0.2, 0.5),     # Moderate performance
            'wisdom': (0.7, 1.0),    # Very high monitoring
        },
        typical_services=['SNMP', 'Prometheus', 'Grafana', 'Syslog'],
        typical_ports=[161, 162, 514, 9090, 3000],
        purpose="Information gathering, monitoring, and analysis",
        characteristics=[
            "Observability focused",
            "Metrics and logs collection",
            "Diagnostic capabilities",
            "Information aggregation",
        ],
        examples=["monitoring.example.com", "prometheus", "grafana-dashboard"],
    ),
    
    ServiceArchetype(
        name="The Hybrid Service",
        description="Multi-function server with balanced capabilities",
        ljpw_signature={
            'love': (0.4, 0.6),      # Balanced
            'justice': (0.4, 0.6),   # Balanced
            'power': (0.4, 0.6),     # Balanced
            'wisdom': (0.4, 0.6),    # Balanced
        },
        typical_services=['Multiple Services'],
        typical_ports=[22, 80, 443, 3306, 8080],
        purpose="Multi-purpose server with diverse functions",
        characteristics=[
            "Balanced across all dimensions",
            "Multiple service types",
            "General-purpose orientation",
            "Flexible configuration",
        ],
        examples=["all-in-one.example.com", "dev-server", "utility-box"],
    ),
    
    ServiceArchetype(
        name="The Stealth Node",
        description="Minimal exposure or inactive system",
        ljpw_signature={
            'love': (0.0, 0.2),      # Very low
            'justice': (0.0, 0.3),   # Very low
            'power': (0.0, 0.2),     # Very low
            'wisdom': (0.0, 0.2),    # Very low
        },
        typical_services=['Minimal or None'],
        typical_ports=[],
        purpose="Hidden, inactive, or highly restricted system",
        characteristics=[
            "Minimal network presence",
            "Few or no open ports",
            "Possibly offline or dormant",
            "Intentionally hidden",
        ],
        examples=["honeypot", "offline-backup", "air-gapped-system"],
    ),
    
    ServiceArchetype(
        name="The Over-Secured Fortress",
        description="Heavily restricted system with maximum security",
        ljpw_signature={
            'love': (0.0, 0.2),      # Very low connectivity
            'justice': (0.8, 1.0),   # Very high security
            'power': (0.3, 0.6),     # Moderate control
            'wisdom': (0.1, 0.3),    # Low monitoring exposure
        },
        typical_services=['Minimal Secure Services'],
        typical_ports=[22],  # Often just SSH
        purpose="Maximum security with minimal accessibility",
        characteristics=[
            "Extremely restrictive policies",
            "Minimal attack surface",
            "Hardened configuration",
            "Security over accessibility",
        ],
        examples=["secure-vault", "hardened-bastion", "compliance-server"],
    ),
]


def match_archetypes(coords: Coordinates, min_confidence: float = 0.5) -> List[Tuple[ServiceArchetype, float]]:
    """
    Match coordinates against all archetypes and return matches above threshold.
    
    Args:
        coords: LJPW coordinates to match
        min_confidence: Minimum confidence threshold (0.0-1.0)
    
    Returns:
        List of (archetype, confidence) tuples, sorted by confidence descending
    """
    matches = []
    
    for archetype in ARCHETYPES:
        confidence = archetype.matches(coords)
        if confidence >= min_confidence:
            matches.append((archetype, confidence))
    
    # Sort by confidence descending
    matches.sort(key=lambda x: x[1], reverse=True)
    
    return matches


def get_archetype_by_name(name: str) -> ServiceArchetype:
    """Get archetype by name"""
    for archetype in ARCHETYPES:
        if archetype.name.lower() == name.lower():
            return archetype
    return None
