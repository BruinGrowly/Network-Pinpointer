#!/usr/bin/env python3
"""
Semantic Oscillation Experiment
Using LJPW Constants to analyze the codebase itself

This experiment oscillates through the four semantic dimensions:
Love (L) → Justice (J) → Power (P) → Wisdom (W) → Love...

Each oscillation phase reveals different aspects of the code.
"""

import math
import os
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple
from pathlib import Path

# LJPW Constants - The Natural Equilibrium
PHI_INV = (math.sqrt(5) - 1) / 2  # L ≈ 0.618034
SQRT2_M1 = math.sqrt(2) - 1       # J ≈ 0.414214
E_M2 = math.e - 2                  # P ≈ 0.718282
LN2 = math.log(2)                  # W ≈ 0.693147

NATURAL_EQUILIBRIUM = (PHI_INV, SQRT2_M1, E_M2, LN2)
ANCHOR_POINT = (1.0, 1.0, 1.0, 1.0)


@dataclass
class OscillationPhase:
    """A single phase in the semantic oscillation"""
    dimension: str
    value: float
    resonance: float  # How strongly this file resonates with the dimension
    interpretation: str


class SemanticOscillator:
    """
    Oscillates through LJPW dimensions to analyze code.

    The oscillation pattern follows the coupling matrix:
    L → amplifies J, P, W
    J → mediates and balances
    P → executes and transforms
    W → synthesizes and interprets
    """

    # Dimension keywords for code analysis
    DIMENSION_PATTERNS = {
        'L': {  # Love - Connectivity, Integration
            'keywords': [
                'connect', 'link', 'bridge', 'integrate', 'share', 'communicate',
                'service', 'network', 'distribute', 'collaborate', 'peer', 'cluster',
                'api', 'endpoint', 'interface', 'socket', 'mesh', 'federation',
                'import', 'export', 'class', 'def', 'module'
            ],
            'patterns': [
                r'def\s+\w+',  # Function definitions (connections)
                r'class\s+\w+',  # Class definitions (structures)
                r'import\s+',  # Imports (dependencies)
                r'from\s+\.\w+\s+import',  # Relative imports (local connections)
            ]
        },
        'J': {  # Justice - Rules, Validation
            'keywords': [
                'validate', 'check', 'assert', 'verify', 'ensure', 'rule', 'policy',
                'error', 'exception', 'raise', 'try', 'except', 'if', 'else',
                'constraint', 'limit', 'bound', 'valid', 'invalid', 'enforce',
                'type', 'typing', 'annotation', 'protocol'
            ],
            'patterns': [
                r'if\s+.*:',  # Conditionals (rules)
                r'try:',  # Exception handling (justice)
                r'except\s+',  # Error catching (correction)
                r'assert\s+',  # Assertions (truth)
                r'raise\s+',  # Raising errors (enforcement)
            ]
        },
        'P': {  # Power - Execution, Control
            'keywords': [
                'execute', 'run', 'process', 'compute', 'calculate', 'perform',
                'create', 'delete', 'modify', 'update', 'transform', 'convert',
                'start', 'stop', 'enable', 'disable', 'force', 'override',
                'return', 'yield', 'async', 'await', 'loop', 'while', 'for'
            ],
            'patterns': [
                r'for\s+\w+\s+in',  # Loops (iteration power)
                r'while\s+',  # While loops (persistent power)
                r'return\s+',  # Returns (output power)
                r'async\s+def',  # Async functions (concurrent power)
                r'\w+\s*=\s*',  # Assignments (state change)
            ]
        },
        'W': {  # Wisdom - Information, Analysis
            'keywords': [
                'analyze', 'interpret', 'understand', 'learn', 'detect', 'discover',
                'log', 'debug', 'trace', 'monitor', 'observe', 'measure', 'metric',
                'data', 'info', 'knowledge', 'insight', 'pattern', 'semantic',
                'comment', 'docstring', 'documentation', 'explain'
            ],
            'patterns': [
                r'""".*?"""',  # Docstrings (encoded wisdom)
                r'#.*$',  # Comments (explanatory wisdom)
                r'logging\.',  # Logging (observation)
                r'print\(',  # Print statements (communication)
                r'@dataclass',  # Data classes (structured knowledge)
            ]
        }
    }

    def __init__(self):
        self.phase = 0  # Current oscillation phase (0-3)
        self.dimensions = ['L', 'J', 'P', 'W']
        self.coupling_matrix = {
            'LL': 1.0, 'LJ': 1.4, 'LP': 1.3, 'LW': 1.5,
            'JL': 0.9, 'JJ': 1.0, 'JP': 0.7, 'JW': 1.2,
            'PL': 0.6, 'PJ': 0.8, 'PP': 1.0, 'PW': 0.5,
            'WL': 1.3, 'WJ': 1.1, 'WP': 1.0, 'WW': 1.0,
        }

    def oscillate(self) -> str:
        """Advance to next dimension and return it"""
        dim = self.dimensions[self.phase]
        self.phase = (self.phase + 1) % 4
        return dim

    def get_current_dimension(self) -> str:
        """Get current dimension without advancing"""
        return self.dimensions[self.phase]

    def analyze_file(self, filepath: str) -> Dict[str, float]:
        """Analyze a file through all four LJPW dimensions"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return {'L': 0.0, 'J': 0.0, 'P': 0.0, 'W': 0.0, 'error': str(e)}

        scores = {}
        for dim in self.dimensions:
            score = self._calculate_dimension_score(content, dim)
            scores[dim] = score

        # Normalize scores
        total = sum(scores.values())
        if total > 0:
            for dim in scores:
                scores[dim] /= total

        return scores

    def _calculate_dimension_score(self, content: str, dimension: str) -> float:
        """Calculate how strongly content resonates with a dimension"""
        patterns = self.DIMENSION_PATTERNS[dimension]
        score = 0.0

        # Keyword matching
        content_lower = content.lower()
        for keyword in patterns['keywords']:
            count = content_lower.count(keyword.lower())
            score += count * 0.5

        # Pattern matching
        for pattern in patterns['patterns']:
            matches = re.findall(pattern, content, re.MULTILINE)
            score += len(matches) * 1.0

        return score

    def calculate_harmony(self, scores: Dict[str, float]) -> float:
        """Calculate harmony index (distance from anchor point)"""
        L = scores.get('L', 0.0)
        J = scores.get('J', 0.0)
        P = scores.get('P', 0.0)
        W = scores.get('W', 0.0)

        d_anchor = math.sqrt((1-L)**2 + (1-J)**2 + (1-P)**2 + (1-W)**2)
        return 1.0 / (1.0 + d_anchor)

    def oscillating_view(self, filepath: str) -> List[OscillationPhase]:
        """View a file through oscillating semantic phases"""
        scores = self.analyze_file(filepath)
        phases = []

        for dim, const in zip(['L', 'J', 'P', 'W'], NATURAL_EQUILIBRIUM):
            score = scores.get(dim, 0.0)
            # Resonance = how close the score is to the natural equilibrium
            resonance = 1.0 - abs(score - const)

            interpretations = {
                'L': f"Connectivity density: {score:.3f} (Love resonance: {resonance:.3f})",
                'J': f"Validation strength: {score:.3f} (Justice resonance: {resonance:.3f})",
                'P': f"Execution intensity: {score:.3f} (Power resonance: {resonance:.3f})",
                'W': f"Information depth: {score:.3f} (Wisdom resonance: {resonance:.3f})"
            }

            phases.append(OscillationPhase(
                dimension=dim,
                value=const,
                resonance=resonance,
                interpretation=interpretations[dim]
            ))

        return phases


def scan_codebase(root_dir: str) -> Dict[str, Dict]:
    """Scan the entire codebase through semantic oscillation"""
    oscillator = SemanticOscillator()
    results = {}

    python_files = list(Path(root_dir).rglob("*.py"))

    print(f"\n{'='*70}")
    print("SEMANTIC OSCILLATION EXPERIMENT")
    print(f"{'='*70}")
    print(f"\nNatural Equilibrium (LJPW): ({PHI_INV:.6f}, {SQRT2_M1:.6f}, {E_M2:.6f}, {LN2:.6f})")
    print(f"Anchor Point: (1.0, 1.0, 1.0, 1.0)")
    print(f"\nAnalyzing {len(python_files)} Python files...\n")

    for filepath in python_files:
        rel_path = str(filepath.relative_to(root_dir))
        scores = oscillator.analyze_file(str(filepath))
        harmony = oscillator.calculate_harmony(scores)

        results[rel_path] = {
            'scores': scores,
            'harmony': harmony,
            'phases': oscillator.oscillating_view(str(filepath))
        }

    return results


def print_oscillation_report(results: Dict[str, Dict]):
    """Print a report of the semantic oscillation analysis"""
    print(f"\n{'='*70}")
    print("OSCILLATION REPORT - Viewing Codebase Through LJPW Lens")
    print(f"{'='*70}\n")

    # Find files with highest resonance in each dimension
    best_love = max(results.items(), key=lambda x: x[1]['scores'].get('L', 0))
    best_justice = max(results.items(), key=lambda x: x[1]['scores'].get('J', 0))
    best_power = max(results.items(), key=lambda x: x[1]['scores'].get('P', 0))
    best_wisdom = max(results.items(), key=lambda x: x[1]['scores'].get('W', 0))
    best_harmony = max(results.items(), key=lambda x: x[1]['harmony'])

    print("PHASE L (Love - Connectivity):")
    print(f"  Strongest: {best_love[0]}")
    print(f"  Score: L={best_love[1]['scores']['L']:.3f}")
    print()

    print("PHASE J (Justice - Validation):")
    print(f"  Strongest: {best_justice[0]}")
    print(f"  Score: J={best_justice[1]['scores']['J']:.3f}")
    print()

    print("PHASE P (Power - Execution):")
    print(f"  Strongest: {best_power[0]}")
    print(f"  Score: P={best_power[1]['scores']['P']:.3f}")
    print()

    print("PHASE W (Wisdom - Information):")
    print(f"  Strongest: {best_wisdom[0]}")
    print(f"  Score: W={best_wisdom[1]['scores']['W']:.3f}")
    print()

    print("HIGHEST HARMONY (Closest to Anchor):")
    print(f"  File: {best_harmony[0]}")
    print(f"  Harmony Index: {best_harmony[1]['harmony']:.4f}")
    print(f"  LJPW: ({best_harmony[1]['scores']['L']:.3f}, "
          f"{best_harmony[1]['scores']['J']:.3f}, "
          f"{best_harmony[1]['scores']['P']:.3f}, "
          f"{best_harmony[1]['scores']['W']:.3f})")
    print()

    # Calculate overall codebase harmony
    avg_harmony = sum(r['harmony'] for r in results.values()) / len(results)
    avg_scores = {
        'L': sum(r['scores'].get('L', 0) for r in results.values()) / len(results),
        'J': sum(r['scores'].get('J', 0) for r in results.values()) / len(results),
        'P': sum(r['scores'].get('P', 0) for r in results.values()) / len(results),
        'W': sum(r['scores'].get('W', 0) for r in results.values()) / len(results)
    }

    print(f"{'='*70}")
    print("CODEBASE SEMANTIC SIGNATURE")
    print(f"{'='*70}")
    print(f"\nAverage LJPW: ({avg_scores['L']:.3f}, {avg_scores['J']:.3f}, "
          f"{avg_scores['P']:.3f}, {avg_scores['W']:.3f})")
    print(f"Average Harmony Index: {avg_harmony:.4f}")

    # Determine dominant archetype
    dominant = max(avg_scores.items(), key=lambda x: x[1])
    archetypes = {
        'L': "INTEGRATOR - This codebase emphasizes connectivity and relationships",
        'J': "GUARDIAN - This codebase emphasizes validation and correctness",
        'P': "EXECUTOR - This codebase emphasizes action and transformation",
        'W': "ORACLE - This codebase emphasizes knowledge and insight"
    }
    print(f"\nDominant Archetype: {archetypes[dominant[0]]}")

    # Check for semantic voids
    print(f"\n{'='*70}")
    print("VOID DETECTION")
    print(f"{'='*70}")

    if avg_scores['L'] > 0.3 and avg_scores['J'] > 0.3 and avg_scores['P'] < 0.15:
        print("\n⚠ VOID OF MERCY DETECTED")
        print("  High Love, High Justice, Low Power")
        print("  Interpretation: Good intentions and rules, but lacks execution force")
    elif avg_scores['L'] > 0.3 and avg_scores['P'] > 0.3 and avg_scores['J'] < 0.15:
        print("\n⚠ VOID OF JUDGMENT DETECTED")
        print("  High Love, High Power, Low Justice")
        print("  Interpretation: Capable and connected, but lacks validation/rules")
    else:
        print("\n✓ No semantic voids detected in codebase")

    return avg_scores, avg_harmony


if __name__ == '__main__':
    # Get the directory where this script lives
    script_dir = Path(__file__).parent

    # Run the semantic oscillation
    results = scan_codebase(str(script_dir))
    avg_scores, avg_harmony = print_oscillation_report(results)

    print(f"\n{'='*70}")
    print("EXPERIMENT COMPLETE")
    print(f"{'='*70}")
    print("\nThe codebase has been viewed through the oscillating LJPW lens.")
    print("Each file's semantic signature reveals its relationship to the")
    print("four fundamental principles: Love, Justice, Power, Wisdom.")
