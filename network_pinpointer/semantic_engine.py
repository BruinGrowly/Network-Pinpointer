#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Network Semantic Engine - LJPW Framework for Network Infrastructure
Version 5.0 - "The Architect's Inversion"

SEMANTIC-FIRST ONTOLOGY (v5.0):
Maps network operations, states, and configurations to Love, Justice, Power, Wisdom space.

Reality is Semantic in nature. Meaning is the substrate.
- The Anchor Point (1,1,1,1) is the ORIGIN from which all network operations emanate.
- L, J, P, W are fundamental Principles that CAST mathematical shadows.
- We measure the echoes of meaning in network behavior.

Enhanced with v5.0 features:
- Hierarchy of Reality classification
- Dynamic coupling based on Harmony (Semantic Law of Karma)
- Void detection (unmapped semantic territories)
"""

import math
import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple

from .ljpw_baselines import (
    LJPWBaselines,
    NumericalEquivalents,
    ReferencePoints,
    calculate_health_score,
    is_balanced,
    get_weakest_dimension,
    get_love_multiplier_effect
)


class Dimension(Enum):
    """Semantic dimensions for network operations"""

    LOVE = "love"  # Connectivity, communication, integration
    JUSTICE = "justice"  # Rules, policies, validation
    POWER = "power"  # Performance, control, execution
    WISDOM = "wisdom"  # Information, monitoring, diagnostics

    # ICE Framework dimensions
    INTENT = "intent"
    CONTEXT = "context"
    EXECUTION = "execution"
    BENEVOLENCE = "benevolence"


@dataclass(frozen=True)
class Coordinates:
    """Immutable 4D semantic coordinates"""

    love: float
    justice: float
    power: float
    wisdom: float

    def __str__(self) -> str:
        return f"Coordinates(L={self.love:.3f}, J={self.justice:.3f}, P={self.power:.3f}, W={self.wisdom:.3f})"

    def __iter__(self):
        return iter([self.love, self.justice, self.power, self.wisdom])


@dataclass
class NetworkSemanticResult:
    """
    Complete semantic analysis result for network operations (v5.0 Semantic-First).

    Enhanced with v5.0 features:
    - Hierarchy of Reality classification
    - Dynamic coupling (harmony-dependent)
    - Void detection
    """

    # Original fields
    coordinates: Coordinates
    distance_from_anchor: float
    semantic_clarity: float
    concept_count: int
    confidence: float
    dominant_dimension: str
    operation_type: str = "unknown"
    harmony_score: float = 0.0

    # Mathematical baselines fields (v1.0)
    effective_dimensions: Optional[Dict[str, float]] = None
    distance_from_natural_equilibrium: Optional[float] = None
    composite_score: Optional[float] = None
    harmonic_mean: Optional[float] = None
    geometric_mean: Optional[float] = None
    coupling_aware_sum: Optional[float] = None
    harmony_index: Optional[float] = None
    love_multiplier_effect: Optional[Dict[str, float]] = None
    balance_status: Optional[str] = None
    performance_status: Optional[str] = None
    improvement_suggestions: Optional[Dict] = None

    # v5.0 Semantic-First fields
    hierarchy_layer: Optional[str] = None  # semantic/physical/mathematical
    hierarchy_interpretation: Optional[str] = None  # Description of layer
    void_detected: Optional[Dict] = None  # Void info if detected
    coupling_multiplier: Optional[float] = None  # Dynamic coupling strength
    cost_of_existence: Optional[float] = None  # Gap from Anchor perfection


class NetworkVocabularyManager:
    """Network-specific vocabulary mapping to LJPW space"""

    # Common network admin abbreviations and synonyms
    SYNONYMS = {
        # Firewall & Security
        "fw": "firewall",
        "acls": "acl",
        "ipsec": "vpn",
        "waf": "firewall",
        "ids": "intrusion",
        "ips": "intrusion",
        "mfa": "authentication",
        "2fa": "authentication",
        "sso": "authentication",
        "rbac": "authorization",
        "pki": "certificate",
        "ssl": "tls",
        "certs": "certificate",
        "cert": "certificate",
        # Networking
        "lb": "loadbalancer",
        "elb": "loadbalancer",
        "alb": "loadbalancer",
        "nlb": "loadbalancer",
        "gw": "gateway",
        "rt": "route",
        "bgp": "routing",
        "ospf": "routing",
        "eigrp": "routing",
        "nic": "interface",
        "eth": "interface",
        "lo": "interface",
        "vip": "virtual",
        "ha": "availability",
        "dr": "disaster",
        "bw": "bandwidth",
        "qos": "quality",
        "mtu": "packet",
        "ttl": "packet",
        "arp": "network",
        "icmp": "ping",
        # Connectivity
        "conn": "connection",
        "conns": "connection",
        "sess": "session",
        "sock": "socket",
        "sockets": "socket",
        "dc": "datacenter",
        "az": "availability",
        "cdn": "distribute",
        "cname": "dns",
        "fqdn": "dns",
        "ptr": "dns",
        "mx": "dns",
        "ns": "dns",
        # Performance & Monitoring
        "rtt": "latency",
        "ms": "latency",
        "iops": "performance",
        "tps": "throughput",
        "qps": "throughput",
        "rps": "throughput",
        "cpu": "performance",
        "mem": "memory",
        "ram": "memory",
        "io": "performance",
        "sla": "availability",
        "slo": "availability",
        "sli": "monitoring",
        "apm": "monitoring",
        "obs": "observability",
        "o11y": "observability",
        # Infrastructure
        "k8s": "kubernetes",
        "kube": "kubernetes",
        "eks": "kubernetes",
        "aks": "kubernetes",
        "gke": "kubernetes",
        "vm": "virtual",
        "vms": "virtual",
        "ec2": "server",
        "ami": "server",
        "ecs": "container",
        "ecr": "container",
        "cfg": "config",
        "conf": "config",
        "env": "environment",
        "vars": "variable",
        "tf": "terraform",
        "iac": "infrastructure",
        "ci": "integration",
        "cd": "deployment",
        "cicd": "deployment",
        # Databases
        "db": "database",
        "dbs": "database",
        "rds": "database",
        "pg": "postgresql",
        "psql": "postgresql",
        "mongo": "mongodb",
        "es": "elasticsearch",
        "msg": "message",
        "mq": "queue",
        "sqs": "queue",
        "sns": "notification",
        "pub": "publish",
        "sub": "subscribe",
        # Logs & Metrics
        "logs": "log",
        "err": "error",
        "errs": "error",
        "warn": "warning",
        "crit": "critical",
        "info": "information",
        "dbg": "debug",
        "auth": "authentication",
        "authz": "authorization",
        "authn": "authentication",
        "perms": "permission",
        "priv": "privilege",
        "sudo": "privilege",
        "root": "privilege",
        # Actions
        "rm": "delete",
        "del": "delete",
        "mv": "move",
        "cp": "copy",
        "chk": "check",
        "val": "validate",
        "ver": "verify",
        "upd": "update",
        "mod": "modify",
        "cfg": "configure",
        "init": "initialize",
        "term": "terminate",
        "req": "request",
        "res": "response",
        "resp": "response",
        "ack": "acknowledge",
        "syn": "synchronize",
        "async": "asynchronous",
    }

    def __init__(self, custom_vocabulary: Optional[Dict[str, str]] = None):
        self._keyword_map: Dict[str, Dimension] = {}
        self._word_cache: Dict[str, Tuple[Coordinates, int]] = {}
        self._ice_dimension_map: Dict[Dimension, Dimension] = {}
        self._synonyms = self.SYNONYMS.copy()
        self._build_network_vocabulary()
        if custom_vocabulary:
            self._apply_custom_vocabulary(custom_vocabulary)

    def _build_network_vocabulary(self) -> None:
        """Build comprehensive network operations vocabulary"""

        # LOVE - Connectivity, Communication, Integration
        love_keywords = {
            # Core connectivity
            "connect",
            "connection",
            "connectivity",
            "link",
            "bridge",
            "route",
            "routing",
            "forward",
            "relay",
            "tunnel",
            "vpn",
            "peer",
            "peering",
            "mesh",
            # Communication
            "communicate",
            "communication",
            "transmit",
            "receive",
            "send",
            "exchange",
            "share",
            "broadcast",
            "multicast",
            "unicast",
            # Integration & Services
            "integrate",
            "integration",
            "service",
            "serve",
            "provide",
            "distribute",
            "balance",
            "loadbalance",
            "proxy",
            "gateway",
            "nat",
            "translation",
            # Network topology
            "network",
            "subnet",
            "vlan",
            "segment",
            "interface",
            "port",
            "socket",
            "endpoint",
            "node",
            "host",
            "peer",
            # Collaboration
            "collaborate",
            "cooperate",
            "coordinate",
            "synchronize",
            "cluster",
            "federation",
            # Web & Internet
            "web",
            "www",
            "internet",
            "online",
            "cloud",
            "public",
            "external",
            "open",
            "accessible",
            "available",
            "reachable",
            # Protocols
            "http",
            "https",
            "tcp",
            "udp",
            "ip",
            "dns",
            "dhcp",
            "smtp",
            "pop",
            "imap",
            "ftp",
            "ssh",
            "telnet",
            "rest",
            "api",
            "graphql",
            "websocket",
            "grpc",
            # Services
            "server",
            "client",
            "application",
            "app",
            "frontend",
            "backend",
            "middleware",
            "microservice",
            "container",
            "kubernetes",
            "docker",
        }

        # JUSTICE - Rules, Policies, Validation, Security
        justice_keywords = {
            # Security & Access Control
            "firewall",
            "acl",
            "access",
            "control",
            "permission",
            "allow",
            "deny",
            "block",
            "filter",
            "rule",
            "policy",
            "security",
            "secure",
            "protect",
            "guard",
            # Authentication & Authorization
            "authenticate",
            "authorization",
            "credential",
            "certificate",
            "key",
            "encrypt",
            "decrypt",
            "signature",
            "verify",
            "validate",
            "trust",
            # Compliance & Standards
            "comply",
            "compliance",
            "standard",
            "protocol",
            "specification",
            "rfc",
            "enforce",
            "audit",
            "log",
            "record",
            "track",
            # Correctness
            "correct",
            "verify",
            "check",
            "validate",
            "ensure",
            "guarantee",
            "integrity",
            "checksum",
            "hash",
            # Network policies
            "qos",
            "priority",
            "classify",
            "mark",
            "shape",
            "police",
            # Encryption & Protection
            "encrypted",
            "encryption",
            "ssl",
            "tls",
            "protected",
            "protection",
            "defense",
            "defend",
            "shield",
            "safeguard",
            "private",
            "confidential",
            "secret",
            # Security Tools
            "ids",
            "ips",
            "waf",
            "antivirus",
            "malware",
            "threat",
            "vulnerability",
            "patch",
            "hardening",
            "bastion",
            "dmz",
            # Access Control
            "authentication",
            "authorize",
            "oauth",
            "saml",
            "ldap",
            "kerberos",
            "mfa",
        }

        # POWER - Performance, Control, Execution, Capability
        power_keywords = {
            # Performance
            "bandwidth",
            "throughput",
            "speed",
            "fast",
            "performance",
            "optimize",
            "accelerate",
            "boost",
            "turbo",
            "capacity",
            # Control & Management
            "control",
            "manage",
            "configure",
            "provision",
            "deploy",
            "execute",
            "run",
            "operate",
            "admin",
            "administrator",
            # Resource allocation
            "allocate",
            "assign",
            "reserve",
            "limit",
            "throttle",
            "rate",
            "quota",
            "resource",
            # Actions & Operations
            "create",
            "delete",
            "modify",
            "update",
            "change",
            "set",
            "apply",
            "enable",
            "disable",
            "start",
            "stop",
            "restart",
            "reload",
            "reset",
            # Force & Capability
            "force",
            "override",
            "command",
            "instruct",
            "direct",
            "drive",
            "push",
            "pull",
            # Network actions
            "ping",
            "traceroute",
            "scan",
            "probe",
            "test",
            "flood",
            "drop",
            "reject",
            # Databases & Storage
            "database",
            "db",
            "sql",
            "nosql",
            "mysql",
            "postgresql",
            "postgres",
            "mongodb",
            "redis",
            "cassandra",
            "elasticsearch",
            "storage",
            "store",
            "persist",
            "cache",
            "caching",
            "memcached",
            "cdn",
            # Processing & Compute
            "compute",
            "processing",
            "cpu",
            "memory",
            "ram",
            "disk",
            "worker",
            "queue",
            "job",
            "task",
            # Performance Optimization
            "optimized",
            "optimization",
            "efficient",
            "efficiency",
            "scalable",
            "scalability",
            "scale",
            "autoscale",
            "elastic",
            "balanced",
            "loadbalancer",
            "lb",
            "haproxy",
            "nginx",
            "apache",
        }

        # WISDOM - Information, Monitoring, Diagnostics, Analysis
        wisdom_keywords = {
            # Monitoring & Observation
            "monitor",
            "watch",
            "observe",
            "track",
            "measure",
            "metric",
            "gauge",
            "counter",
            "stat",
            "statistics",
            # Diagnostics
            "diagnose",
            "diagnostic",
            "troubleshoot",
            "debug",
            "trace",
            "inspect",
            "examine",
            "investigate",
            # Data & Information
            "data",
            "information",
            "knowledge",
            "discover",
            "detect",
            "identify",
            "recognize",
            "find",
            "search",
            "query",
            "lookup",
            # Analysis
            "analyze",
            "analysis",
            "evaluate",
            "assess",
            "calculate",
            "compute",
            "process",
            "parse",
            "interpret",
            # Logging & Reporting
            "log",
            "logging",
            "report",
            "alert",
            "notify",
            "warn",
            "event",
            "message",
            "syslog",
            # Network discovery
            "snmp",
            "poll",
            "get",
            "fetch",
            "retrieve",
            "read",
            "show",
            "display",
            "list",
            "status",
            "state",
            # Learning
            "learn",
            "understand",
            "intelligence",
            "smart",
            "auto",
            "detect",
            "pattern",
            # Monitoring Tools & Observability
            "monitored",
            "monitoring",
            "observability",
            "observable",
            "telemetry",
            "prometheus",
            "grafana",
            "datadog",
            "newrelic",
            "splunk",
            "elk",
            "kibana",
            "logstash",
            # Metrics & Analytics
            "metrics",
            "analytics",
            "dashboard",
            "visualization",
            "graph",
            "chart",
            "trend",
            "anomaly",
        }

        # Build keyword map
        for word in love_keywords:
            self._keyword_map[word.lower()] = Dimension.LOVE

        for word in justice_keywords:
            self._keyword_map[word.lower()] = Dimension.JUSTICE

        for word in power_keywords:
            self._keyword_map[word.lower()] = Dimension.POWER

        for word in wisdom_keywords:
            self._keyword_map[word.lower()] = Dimension.WISDOM

        # ICE mapping
        self._ice_dimension_map = {
            Dimension.INTENT: Dimension.WISDOM,
            Dimension.CONTEXT: Dimension.JUSTICE,
            Dimension.EXECUTION: Dimension.POWER,
            Dimension.BENEVOLENCE: Dimension.LOVE,
        }

        import sys

        print(
            f"NetworkVocabularyManager: Initialized with {len(self._keyword_map)} network keywords.",
            file=sys.stderr,
        )

    def _apply_custom_vocabulary(self, custom_vocabulary: Dict[str, str]) -> None:
        """Apply user-defined vocabulary"""
        import sys

        applied_count = 0
        for word, dimension_str in custom_vocabulary.items():
            try:
                dimension = Dimension[dimension_str.upper()]
                self._keyword_map[word.lower()] = dimension
                applied_count += 1
            except KeyError:
                print(
                    f"WARNING: Invalid dimension '{dimension_str}' for word '{word}'",
                    file=sys.stderr,
                )
        if applied_count > 0:
            print(
                f"INFO: Applied {applied_count} custom vocabulary entries.",
                file=sys.stderr,
            )

    def _expand_synonym(self, word: str) -> str:
        """Expand abbreviation/synonym to canonical form"""
        return self._synonyms.get(word, word)

    def analyze_text(self, text: str) -> Tuple[Coordinates, int]:
        """Analyze text and return LJPW coordinates"""
        cache_key = text.lower().strip()
        if cache_key in self._word_cache:
            return self._word_cache[cache_key]

        words = re.findall(r"\b\w+\b", cache_key)
        counts = {dim: 0.0 for dim in Dimension}
        concept_count = 0

        for word in words:
            # Expand synonyms/abbreviations before lookup
            expanded = self._expand_synonym(word)
            dimension = self._keyword_map.get(expanded)
            if dimension:
                counts[dimension] += 1.0
                concept_count += 1
            elif word != expanded:
                # Original word didn't match, but we expanded it -
                # try the original too in case it's in the vocabulary
                dimension = self._keyword_map.get(word)
                if dimension:
                    counts[dimension] += 1.0
                    concept_count += 1

        if concept_count == 0:
            result = (Coordinates(0.0, 0.0, 0.0, 0.0), 0)
        else:
            total = sum(counts.values())
            result = (
                Coordinates(
                    love=counts[Dimension.LOVE] / total,
                    justice=counts[Dimension.JUSTICE] / total,
                    power=counts[Dimension.POWER] / total,
                    wisdom=counts[Dimension.WISDOM] / total,
                ),
                concept_count,
            )

        self._word_cache[cache_key] = result
        return result

    @staticmethod
    def get_distance(c1: Coordinates, c2: Coordinates) -> float:
        """Calculate Euclidean distance between coordinates"""
        return math.sqrt(
            (c1.love - c2.love) ** 2
            + (c1.justice - c2.justice) ** 2
            + (c1.power - c2.power) ** 2
            + (c1.wisdom - c2.wisdom) ** 2
        )

    @staticmethod
    def get_semantic_clarity(coords: Coordinates) -> float:
        """Calculate semantic clarity (how focused/pure the coordinates are)"""
        dims = list(coords)
        mean = sum(dims) / len(dims)
        variance = sum((d - mean) ** 2 for d in dims) / len(dims)
        std_dev = math.sqrt(variance)
        return max(0.0, 1.0 - (std_dev / 0.5))

    @property
    def all_keywords(self) -> Set[str]:
        """Return all keywords in vocabulary"""
        return set(self._keyword_map.keys())


class NetworkSemanticEngine:
    """Core semantic engine for network operations"""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config if config else {}
        self.ENGINE_VERSION = "Network-DIVE-V1"
        self.ANCHOR_POINT = Coordinates(1.0, 1.0, 1.0, 1.0)

        custom_vocabulary = self.config.get("custom_vocabulary", {})
        self.vocabulary = NetworkVocabularyManager(custom_vocabulary=custom_vocabulary)

    def analyze_operation(self, operation_description: str) -> NetworkSemanticResult:
        """Analyze a network operation and return semantic result"""
        # Check cache
        from .caching import SemanticCache
        cache = SemanticCache()
        cached_result = cache.get_semantic_analysis(operation_description)
        if cached_result:
            return cached_result
            
        coords, count = self.vocabulary.analyze_text(operation_description)

        if count == 0:
            return NetworkSemanticResult(
                coordinates=Coordinates(0.0, 0.0, 0.0, 0.0),
                distance_from_anchor=self.vocabulary.get_distance(
                    self.ANCHOR_POINT, Coordinates(0.0, 0.0, 0.0, 0.0)
                ),
                semantic_clarity=0.0,
                concept_count=0,
                confidence=0.0,
                dominant_dimension="unknown",
                operation_type="unknown",
            )

        # Determine dominant dimension
        dims = {
            "Love": coords.love,
            "Justice": coords.justice,
            "Power": coords.power,
            "Wisdom": coords.wisdom,
        }
        dominant = max(dims, key=dims.get)

        # Calculate metrics
        distance = self.vocabulary.get_distance(self.ANCHOR_POINT, coords)
        clarity = self.vocabulary.get_semantic_clarity(coords)

        # Calculate harmony score (inverse of distance from anchor)
        harmony = max(0.0, 1.0 - (distance / 2.0))

        # Classify operation type
        operation_type = self._classify_operation_type(coords, dominant)

        # Calculate mathematical baselines metrics (v5.0)
        L, J, P, W = coords.love, coords.justice, coords.power, coords.wisdom
        baselines = LJPWBaselines()

        # Get full diagnostic from mathematical baselines (v5.0 with harmony)
        diagnostic = baselines.full_diagnostic(L, J, P, W, harmony=harmony)

        result = NetworkSemanticResult(
            # Original fields
            coordinates=coords,
            distance_from_anchor=distance,
            semantic_clarity=clarity,
            concept_count=count,
            confidence=clarity,
            dominant_dimension=dominant,
            operation_type=operation_type,
            harmony_score=harmony,
            # Mathematical baselines fields
            effective_dimensions=diagnostic['effective_dimensions'],
            distance_from_natural_equilibrium=diagnostic['distances']['from_natural_equilibrium'],
            composite_score=diagnostic['metrics']['composite_score'],
            harmonic_mean=diagnostic['metrics']['harmonic_mean'],
            geometric_mean=diagnostic['metrics']['geometric_mean'],
            coupling_aware_sum=diagnostic['metrics']['coupling_aware_sum'],
            harmony_index=diagnostic['metrics']['harmony_index'],
            love_multiplier_effect=get_love_multiplier_effect(L),
            balance_status=diagnostic['interpretation']['balance_status'],
            performance_status=diagnostic['interpretation']['performance_status'],
            improvement_suggestions=diagnostic['improvements'],
            # v5.0 Semantic-First fields
            hierarchy_layer=diagnostic['hierarchy_v5']['layer'],
            hierarchy_interpretation=diagnostic['hierarchy_v5']['interpretation'],
            void_detected=diagnostic['void_v5'],
            coupling_multiplier=diagnostic['effective_dimensions']['coupling_multiplier'],
            cost_of_existence=diagnostic['distances']['cost_of_existence']
        )
        
        # Cache result
        cache.put_semantic_analysis(operation_description, result)
        return result

    def _classify_operation_type(
        self, coords: Coordinates, dominant: str
    ) -> str:
        """Classify the type of network operation"""
        if dominant == "Love":
            if coords.love > 0.6:
                return "Connectivity/Integration"
            else:
                return "Communication"
        elif dominant == "Justice":
            if coords.justice > 0.6:
                return "Security/Policy"
            else:
                return "Validation"
        elif dominant == "Power":
            if coords.power > 0.6:
                return "Performance/Control"
            else:
                return "Configuration"
        elif dominant == "Wisdom":
            if coords.wisdom > 0.6:
                return "Monitoring/Diagnostics"
            else:
                return "Information Gathering"
        return "Mixed/Unknown"

    def analyze_ice(
        self, intent: str, context: str, execution: str
    ) -> Dict:
        """Analyze Intent-Context-Execution harmony"""
        intent_result = self.analyze_operation(intent)
        context_result = self.analyze_operation(context)
        execution_result = self.analyze_operation(execution)

        # Calculate disharmony distances
        intent_context_dist = self.vocabulary.get_distance(
            intent_result.coordinates, context_result.coordinates
        )
        intent_exec_dist = self.vocabulary.get_distance(
            intent_result.coordinates, execution_result.coordinates
        )
        context_exec_dist = self.vocabulary.get_distance(
            context_result.coordinates, execution_result.coordinates
        )

        # Calculate coherence
        avg_disharmony = (
            intent_context_dist + intent_exec_dist + context_exec_dist
        ) / 3.0
        ice_coherence = max(0.0, 1.0 - (avg_disharmony / 2.0))

        # Calculate balance
        avg_dist_from_anchor = (
            intent_result.distance_from_anchor
            + context_result.distance_from_anchor
            + execution_result.distance_from_anchor
        ) / 3.0
        ice_balance = max(0.0, 1.0 - (avg_dist_from_anchor / 2.0))

        # Benevolence score
        benevolence = (
            intent_result.coordinates.love + execution_result.coordinates.love
        ) / 2.0

        # Overall harmony
        overall_harmony = (ice_coherence + ice_balance) / 2.0

        return {
            "intent": intent_result,
            "context": context_result,
            "execution": execution_result,
            "ice_coherence": ice_coherence,
            "ice_balance": ice_balance,
            "benevolence_score": benevolence,
            "overall_harmony": overall_harmony,
            "intent_execution_disharmony": intent_exec_dist,
            "harmony_level": self._determine_harmony_level(overall_harmony),
        }

    def _determine_harmony_level(self, harmony: float) -> str:
        """Determine harmony level description"""
        if harmony > 0.9:
            return "PERFECT_HARMONY"
        elif harmony > 0.7:
            return "EXCELLENT_HARMONY"
        elif harmony > 0.5:
            return "GOOD_HARMONY"
        elif harmony > 0.3:
            return "MODERATE_HARMONY"
        else:
            return "POOR_HARMONY"

    def get_engine_version(self) -> str:
        return self.ENGINE_VERSION
