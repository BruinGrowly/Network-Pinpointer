#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Network Semantic Engine - LJPW Framework for Network Infrastructure

Maps network operations, states, and configurations to Love, Justice, Power, Wisdom space.
Enhanced with mathematical baselines from information theory.
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
    Complete semantic analysis result for network operations.

    Enhanced with mathematical baselines from information theory.
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


class NetworkVocabularyManager:
    """Network-specific vocabulary mapping to LJPW space"""

    def __init__(self, custom_vocabulary: Optional[Dict[str, str]] = None):
        self._keyword_map: Dict[str, Dimension] = {}
        self._word_cache: Dict[str, Tuple[Coordinates, int]] = {}
        self._ice_dimension_map: Dict[Dimension, Dimension] = {}
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

    def analyze_text(self, text: str) -> Tuple[Coordinates, int]:
        """Analyze text and return LJPW coordinates"""
        cache_key = text.lower().strip()
        if cache_key in self._word_cache:
            return self._word_cache[cache_key]

        words = re.findall(r"\b\w+\b", cache_key)
        counts = {dim: 0.0 for dim in Dimension}
        concept_count = 0

        for word in words:
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

        # Calculate mathematical baselines metrics
        L, J, P, W = coords.love, coords.justice, coords.power, coords.wisdom
        baselines = LJPWBaselines()

        # Get full diagnostic from mathematical baselines
        diagnostic = baselines.full_diagnostic(L, J, P, W)

        return NetworkSemanticResult(
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
            improvement_suggestions=diagnostic['improvements']
        )

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
