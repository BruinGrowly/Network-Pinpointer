#!/usr/bin/env python3
"""
Diagnostic Recipes - Pre-built workflows for common network problems

Provides expert-level diagnostic workflows that network admins can run
with a single command.
"""

from dataclasses import dataclass
from typing import List, Dict, Callable, Optional, Any
from enum import Enum

from .semantic_engine import Coordinates
from .cli_output import get_formatter, Colors


class DiagnosticStep(Enum):
    """Types of diagnostic steps"""
    PING = "ping"
    TRACEROUTE = "traceroute"
    PORT_SCAN = "port_scan"
    DNS_LOOKUP = "dns_lookup"
    BANDWIDTH_TEST = "bandwidth_test"
    PACKET_CAPTURE = "packet_capture"
    ROUTE_CHECK = "route_check"
    SEMANTIC_ANALYSIS = "semantic_analysis"


@dataclass
class RecipeStep:
    """Single step in a diagnostic recipe"""
    name: str
    step_type: DiagnosticStep
    description: str
    params: Dict[str, Any]
    required: bool = True
    timeout: int = 30


@dataclass
class RecipeResult:
    """Result from running a diagnostic recipe"""
    recipe_name: str
    success: bool
    coordinates: Optional[Coordinates]
    findings: List[str]
    recommendations: List[str]
    raw_data: Dict[str, Any]
    confidence: float


class DiagnosticRecipe:
    """A pre-built diagnostic workflow"""

    def __init__(
        self,
        name: str,
        description: str,
        steps: List[RecipeStep],
        interpretation: str,
        target_dimensions: List[str]
    ):
        self.name = name
        self.description = description
        self.steps = steps
        self.interpretation = interpretation
        self.target_dimensions = target_dimensions

    def display_plan(self) -> str:
        """Display what this recipe will do"""
        fmt = get_formatter()
        lines = []

        lines.append(fmt.section_header(f"Recipe: {self.name}"))
        lines.append(f"\n{self.description}\n")
        lines.append(fmt.subsection_header("Diagnostic Plan:"))

        for i, step in enumerate(self.steps, 1):
            required = "(required)" if step.required else "(optional)"
            lines.append(f"  {i}. {step.name} {fmt.dim(required)}")
            lines.append(f"     {fmt.dim(step.description)}")

        lines.append(f"\n{fmt.subsection_header('Focus Areas:')}")
        lines.append(f"This recipe analyzes: {', '.join(self.target_dimensions)}")

        lines.append(f"\n{fmt.dim(f'Estimated time: {sum(s.timeout for s in self.steps)}s')}")

        return "\n".join(lines)


class RecipeLibrary:
    """Library of pre-built diagnostic recipes"""

    def __init__(self):
        self.recipes: Dict[str, DiagnosticRecipe] = {}
        self._build_recipes()

    def _build_recipes(self):
        """Build all diagnostic recipes"""

        # Recipe 1: Slow Connection
        self.recipes["slow_connection"] = DiagnosticRecipe(
            name="Slow Connection Diagnosis",
            description="Diagnose why a connection is slower than expected",
            steps=[
                RecipeStep(
                    name="Ping Latency Test",
                    step_type=DiagnosticStep.PING,
                    description="Measure basic latency and packet loss",
                    params={"count": 20, "interval": 0.2},
                    timeout=10
                ),
                RecipeStep(
                    name="Path Analysis",
                    step_type=DiagnosticStep.TRACEROUTE,
                    description="Identify path complexity and routing issues",
                    params={"max_hops": 30},
                    timeout=30
                ),
                RecipeStep(
                    name="Packet Capture Analysis",
                    step_type=DiagnosticStep.PACKET_CAPTURE,
                    description="Deep dive into packet metadata",
                    params={"count": 50, "capture_time": 10},
                    timeout=15
                ),
                RecipeStep(
                    name="Semantic Analysis",
                    step_type=DiagnosticStep.SEMANTIC_ANALYSIS,
                    description="Map findings to LJPW dimensions",
                    params={},
                    timeout=5
                )
            ],
            interpretation="Focuses on Power and Love dimensions (performance + connectivity)",
            target_dimensions=["Power", "Love", "Wisdom"]
        )

        # Recipe 2: Can't Connect
        self.recipes["cant_connect"] = DiagnosticRecipe(
            name="Connection Failure Diagnosis",
            description="Figure out why you can't connect to a service",
            steps=[
                RecipeStep(
                    name="DNS Resolution Check",
                    step_type=DiagnosticStep.DNS_LOOKUP,
                    description="Verify name resolution is working",
                    params={},
                    timeout=5
                ),
                RecipeStep(
                    name="Ping Reachability",
                    step_type=DiagnosticStep.PING,
                    description="Test if host is reachable at all",
                    params={"count": 5},
                    timeout=10
                ),
                RecipeStep(
                    name="Port Accessibility Check",
                    step_type=DiagnosticStep.PORT_SCAN,
                    description="Check if specific service ports are open",
                    params={"ports": [80, 443, 22, 3306, 5432]},
                    timeout=20
                ),
                RecipeStep(
                    name="Route Verification",
                    step_type=DiagnosticStep.TRACEROUTE,
                    description="Verify routing path exists",
                    params={"max_hops": 20},
                    timeout=25
                ),
                RecipeStep(
                    name="Semantic Analysis",
                    step_type=DiagnosticStep.SEMANTIC_ANALYSIS,
                    description="Determine if it's a Love or Justice issue",
                    params={},
                    timeout=5
                )
            ],
            interpretation="Distinguishes Love issues (no route) from Justice issues (blocked)",
            target_dimensions=["Love", "Justice", "Wisdom"]
        )

        # Recipe 3: Intermittent Issues
        self.recipes["intermittent"] = DiagnosticRecipe(
            name="Intermittent Connection Issues",
            description="Diagnose connections that work sometimes but not always",
            steps=[
                RecipeStep(
                    name="Extended Ping Test",
                    step_type=DiagnosticStep.PING,
                    description="Run longer test to catch intermittent failures",
                    params={"count": 100, "interval": 1},
                    timeout=120
                ),
                RecipeStep(
                    name="Route Stability Analysis",
                    step_type=DiagnosticStep.TRACEROUTE,
                    description="Check if routes are stable or flapping",
                    params={"iterations": 5, "delay": 5},
                    timeout=60
                ),
                RecipeStep(
                    name="Packet Loss Pattern Detection",
                    step_type=DiagnosticStep.PACKET_CAPTURE,
                    description="Identify if loss is random, periodic, or burst",
                    params={"count": 100, "capture_time": 30},
                    timeout=40
                ),
                RecipeStep(
                    name="Semantic Analysis",
                    step_type=DiagnosticStep.SEMANTIC_ANALYSIS,
                    description="Determine if it's QoS policy or actual problems",
                    params={},
                    timeout=5
                )
            ],
            interpretation="Distinguishes intentional QoS (Justice) from real issues (Power/Love)",
            target_dimensions=["Justice", "Power", "Love", "Wisdom"]
        )

        # Recipe 4: High Security Network
        self.recipes["security_audit"] = DiagnosticRecipe(
            name="Security Posture Audit",
            description="Check if network security is properly configured",
            steps=[
                RecipeStep(
                    name="Port Scan Multiple Targets",
                    step_type=DiagnosticStep.PORT_SCAN,
                    description="Check what's accessible from this location",
                    params={"common_ports": True},
                    timeout=30
                ),
                RecipeStep(
                    name="Connectivity Tests",
                    step_type=DiagnosticStep.PING,
                    description="Test connectivity to various targets",
                    params={"targets": ["internal", "external", "dmz"]},
                    timeout=20
                ),
                RecipeStep(
                    name="Semantic Analysis",
                    step_type=DiagnosticStep.SEMANTIC_ANALYSIS,
                    description="Check Justice dimension for security enforcement",
                    params={},
                    timeout=5
                )
            ],
            interpretation="Focuses on Justice dimension (security boundaries)",
            target_dimensions=["Justice", "Love"]
        )

        # Recipe 5: Performance Baseline
        self.recipes["baseline"] = DiagnosticRecipe(
            name="Network Performance Baseline",
            description="Establish baseline metrics for healthy network state",
            steps=[
                RecipeStep(
                    name="Multi-Target Latency",
                    step_type=DiagnosticStep.PING,
                    description="Test latency to multiple targets",
                    params={"targets": ["gateway", "dns", "external"], "count": 20},
                    timeout=30
                ),
                RecipeStep(
                    name="Path Complexity Mapping",
                    step_type=DiagnosticStep.TRACEROUTE,
                    description="Map typical path lengths",
                    params={"targets": ["internal", "external"]},
                    timeout=40
                ),
                RecipeStep(
                    name="Extended Capture",
                    step_type=DiagnosticStep.PACKET_CAPTURE,
                    description="Capture representative traffic sample",
                    params={"count": 200, "capture_time": 60},
                    timeout=70
                ),
                RecipeStep(
                    name="Semantic Analysis",
                    step_type=DiagnosticStep.SEMANTIC_ANALYSIS,
                    description="Calculate LJPW baseline coordinates",
                    params={"establish_baseline": True},
                    timeout=5
                )
            ],
            interpretation="Establishes expected healthy state for all dimensions",
            target_dimensions=["Love", "Justice", "Power", "Wisdom"]
        )

        # Recipe 6: Quick Health Check
        self.recipes["quick_check"] = DiagnosticRecipe(
            name="Quick Network Health Check",
            description="Fast 30-second health assessment",
            steps=[
                RecipeStep(
                    name="Gateway Ping",
                    step_type=DiagnosticStep.PING,
                    description="Quick connectivity check",
                    params={"count": 5},
                    timeout=10
                ),
                RecipeStep(
                    name="DNS Check",
                    step_type=DiagnosticStep.DNS_LOOKUP,
                    description="Verify DNS is working",
                    params={"domain": "google.com"},
                    timeout=5
                ),
                RecipeStep(
                    name="External Ping",
                    step_type=DiagnosticStep.PING,
                    description="Test external connectivity",
                    params={"target": "8.8.8.8", "count": 5},
                    timeout=10
                ),
                RecipeStep(
                    name="Semantic Analysis",
                    step_type=DiagnosticStep.SEMANTIC_ANALYSIS,
                    description="Quick LJPW assessment",
                    params={},
                    timeout=5
                )
            ],
            interpretation="Quick overview of all dimensions",
            target_dimensions=["Love", "Power", "Wisdom"]
        )

    def get_recipe(self, name: str) -> Optional[DiagnosticRecipe]:
        """Get a recipe by name"""
        return self.recipes.get(name)

    def list_recipes(self) -> List[str]:
        """List all available recipes"""
        return list(self.recipes.keys())

    def display_all_recipes(self) -> str:
        """Display all available recipes"""
        fmt = get_formatter()
        lines = []

        lines.append(fmt.section_header("Available Diagnostic Recipes"))
        lines.append("")

        for i, (key, recipe) in enumerate(self.recipes.items(), 1):
            title = fmt.bold(f'{i}. {recipe.name}')
            command = fmt.color(f'network-pinpointer run {key}', Colors.CYAN)
            dimensions = ', '.join(recipe.target_dimensions)
            analyzes_text = fmt.dim(f'Analyzes: {dimensions}')

            lines.append(title)
            lines.append(f"   Command: {command}")
            lines.append(f"   {recipe.description}")
            lines.append(f"   {analyzes_text}")
            lines.append("")

        return "\n".join(lines)

    def recommend_recipe(self, symptoms: List[str]) -> Optional[str]:
        """Recommend a recipe based on symptoms"""
        symptom_lower = [s.lower() for s in symptoms]

        # Keyword matching for recommendations
        if any(word in symptom_lower for word in ["slow", "latency", "lag", "performance"]):
            return "slow_connection"
        elif any(word in symptom_lower for word in ["can't connect", "connection refused", "timeout", "unreachable"]):
            return "cant_connect"
        elif any(word in symptom_lower for word in ["intermittent", "sometimes", "random", "flaky"]):
            return "intermittent"
        elif any(word in symptom_lower for word in ["security", "firewall", "blocked"]):
            return "security_audit"
        elif any(word in symptom_lower for word in ["baseline", "healthy", "normal"]):
            return "baseline"
        else:
            return "quick_check"


def display_recipe_menu() -> str:
    """Display interactive recipe selection menu"""
    fmt = get_formatter()
    library = RecipeLibrary()

    lines = []
    lines.append(fmt.section_header("What would you like to diagnose?"))
    lines.append("")

    recipes = [
        ("1", "slow_connection", "🐌 Connection is slower than expected"),
        ("2", "cant_connect", "🚫 Can't connect to a service"),
        ("3", "intermittent", "⚡ Connection works sometimes but not always"),
        ("4", "security_audit", "🔒 Check security configuration"),
        ("5", "baseline", "📊 Establish performance baseline"),
        ("6", "quick_check", "⚡ Quick 30-second health check"),
    ]

    for num, key, description in recipes:
        lines.append(f"  {fmt.bold(num)}. {description}")

    lines.append("")
    lines.append("Enter number (1-6) or 'q' to quit")

    return "\n".join(lines)


if __name__ == "__main__":
    # Demo the recipe library
    library = RecipeLibrary()

    print(library.display_all_recipes())

    print("\n" + "=" * 70)
    print("Recipe Plan Example:")
    print("=" * 70)

    recipe = library.get_recipe("slow_connection")
    if recipe:
        print(recipe.display_plan())
