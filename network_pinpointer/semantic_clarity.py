#!/usr/bin/env python3
"""
Semantic Clarity Analyzer - Description Richness Analysis

Demonstrates how description richness affects semantic clarity:
- More descriptive text → Higher semantic clarity
- Richer descriptions → Better dimensional balance
- Comprehensive descriptions → More accurate LJPW representation

This module proves the "Semantic Clarity Principle" - that the LJPW
framework naturally rewards comprehensive understanding.
"""

import math
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional

from .semantic_engine import NetworkSemanticEngine, Coordinates, NetworkSemanticResult


@dataclass
class DescriptionLevel:
    """Analysis of a single description level"""
    level: int
    name: str
    description: str
    word_count: int
    coords: Coordinates
    clarity: float
    concepts: int
    harmony: float
    balance: float
    entropy: float
    information_content: float


@dataclass
class ClarityProgression:
    """Analysis of clarity progression across description levels"""
    base_concept: str
    levels: List[DescriptionLevel] = field(default_factory=list)
    clarity_trend: List[float] = field(default_factory=list)
    balance_trend: List[float] = field(default_factory=list)
    harmony_trend: List[float] = field(default_factory=list)
    entropy_trend: List[float] = field(default_factory=list)
    insights: List[str] = field(default_factory=list)
    hypothesis_confirmed: bool = False


class SemanticClarityAnalyzer:
    """Analyze how description richness affects semantic clarity"""
    
    def __init__(self, semantic_engine: NetworkSemanticEngine):
        self.engine = semantic_engine
    
    def analyze_description_levels(
        self, 
        base_concept: str,
        enrichment_levels: List[List[str]],
        level_names: Optional[List[str]] = None
    ) -> ClarityProgression:
        """
        Analyze same concept with increasing description levels.
        
        Args:
            base_concept: Core concept (e.g., "web server")
            enrichment_levels: Lists of additional descriptive terms for each level
            level_names: Optional names for each level (e.g., "Minimal", "Basic", etc.)
        
        Returns:
            ClarityProgression showing how metrics improve with description richness
        """
        if level_names is None:
            level_names = [
                "Minimal", "Basic", "Moderate", "Detailed", "Rich", 
                "Comprehensive", "Exhaustive"
            ][:len(enrichment_levels) + 1]
        
        progression = ClarityProgression(base_concept=base_concept)
        
        # Level 0: Just the base concept
        desc = base_concept
        level_data = self._analyze_single_level(0, level_names[0], desc)
        progression.levels.append(level_data)
        
        # Subsequent levels: Add enrichments
        for level_idx, terms in enumerate(enrichment_levels, 1):
            desc = base_concept + " " + " ".join(terms)
            level_data = self._analyze_single_level(
                level_idx, 
                level_names[level_idx] if level_idx < len(level_names) else f"Level {level_idx}",
                desc
            )
            progression.levels.append(level_data)
        
        # Extract trends
        progression.clarity_trend = [l.clarity for l in progression.levels]
        progression.balance_trend = [l.balance for l in progression.levels]
        progression.harmony_trend = [l.harmony for l in progression.levels]
        progression.entropy_trend = [l.entropy for l in progression.levels]
        
        # Generate insights
        progression.insights = self._generate_insights(progression.levels)
        
        # Check if hypothesis is confirmed
        progression.hypothesis_confirmed = self._check_hypothesis(progression.levels)
        
        return progression
    
    def _analyze_single_level(self, level: int, name: str, description: str) -> DescriptionLevel:
        """Analyze a single description level"""
        result = self.engine.analyze_operation(description)
        
        return DescriptionLevel(
            level=level,
            name=name,
            description=description,
            word_count=len(description.split()),
            coords=result.coordinates,
            clarity=result.semantic_clarity,
            concepts=result.concept_count,
            harmony=result.harmony_score,
            balance=self._calculate_balance(result.coordinates),
            entropy=self._calculate_entropy(result.coordinates),
            information_content=self._calculate_information_content(result)
        )
    
    def _calculate_balance(self, coords: Coordinates) -> float:
        """
        Calculate dimensional balance (0-1).
        
        Higher = more balanced across all dimensions
        Lower = concentrated in few dimensions
        """
        dims = [coords.love, coords.justice, coords.power, coords.wisdom]
        mean_dim = sum(dims) / 4
        variance = sum((d - mean_dim)**2 for d in dims) / 4
        
        # Max variance is 0.25 (one dim = 1, others = 0)
        # Balance = 1 - normalized_variance
        balance = 1.0 - (variance / 0.25)
        return max(0.0, min(1.0, balance))
    
    def _calculate_entropy(self, coords: Coordinates) -> float:
        """
        Calculate Shannon entropy of dimension distribution (0-1).
        
        Higher = more evenly distributed (multi-faceted)
        Lower = concentrated (specialized)
        """
        dims = [coords.love, coords.justice, coords.power, coords.wisdom]
        
        # Normalize to probabilities
        total = sum(dims)
        if total == 0:
            return 0.0
        
        probs = [d / total for d in dims]
        
        # Shannon entropy
        entropy = -sum(p * math.log2(p) if p > 0 else 0 for p in probs)
        
        # Max entropy for 4 dimensions is log2(4) = 2
        normalized_entropy = entropy / 2.0
        
        return normalized_entropy
    
    def _calculate_information_content(self, result: NetworkSemanticResult) -> float:
        """
        Calculate semantic information content.
        
        Combines concept count, clarity, and harmony into a single metric
        representing how much semantic information is captured.
        """
        return result.concept_count * result.semantic_clarity * (1.0 + result.harmony_score)
    
    def _generate_insights(self, levels: List[DescriptionLevel]) -> List[str]:
        """Generate insights from progression analysis"""
        insights = []
        
        if len(levels) < 2:
            return insights
        
        first = levels[0]
        last = levels[-1]
        
        # Clarity improvement
        clarity_delta = last.clarity - first.clarity
        if clarity_delta > 0.2:
            insights.append(
                f"✅ Semantic clarity improved significantly (+{clarity_delta:.0%})"
            )
        elif clarity_delta > 0.1:
            insights.append(
                f"✅ Semantic clarity improved moderately (+{clarity_delta:.0%})"
            )
        
        # Balance improvement
        balance_delta = last.balance - first.balance
        if balance_delta > 0.2:
            insights.append(
                f"✅ Dimensional balance improved significantly (+{balance_delta:.0%})"
            )
        elif balance_delta > 0.1:
            insights.append(
                f"✅ Dimensional balance improved moderately (+{balance_delta:.0%})"
            )
        
        # Harmony improvement
        harmony_delta = last.harmony - first.harmony
        if harmony_delta > 0.3:
            insights.append(
                f"✅ Harmony score improved significantly (+{harmony_delta:.0%})"
            )
        
        # Entropy (multi-faceted nature)
        entropy_delta = last.entropy - first.entropy
        if entropy_delta > 0.2:
            insights.append(
                f"✅ System revealed as more multi-faceted (+{entropy_delta:.0%} entropy)"
            )
        
        # Check if all dimensions are now represented
        dims_represented = sum([
            1 for d in [last.coords.love, last.coords.justice, 
                       last.coords.power, last.coords.wisdom]
            if d > 0.1
        ])
        
        if dims_represented == 4 and sum([
            1 for d in [first.coords.love, first.coords.justice,
                       first.coords.power, first.coords.wisdom]
            if d > 0.1
        ]) < 4:
            insights.append(
                "✅ All four LJPW dimensions now represented"
            )
        
        # Concept growth
        if last.concepts > 0 and first.concepts > 0:
            concept_growth = last.concepts / first.concepts
            if concept_growth > 5:
                insights.append(
                    f"✅ Concept count grew {concept_growth:.1f}x"
                )
            elif concept_growth > 2:
                insights.append(
                    f"✅ Concept count doubled ({concept_growth:.1f}x)"
                )
        
        # Information content growth
        if (last.information_content > first.information_content * 3 and 
            first.information_content > 0):
            growth = last.information_content / first.information_content
            insights.append(
                f"✅ Semantic information content grew {growth:.1f}x"
            )
        
        # Final state assessment
        if last.clarity > 0.8 and last.balance > 0.8:
            insights.append(
                "✅ Achieved high clarity and balance - comprehensive understanding"
            )
        
        return insights
    
    def _check_hypothesis(self, levels: List[DescriptionLevel]) -> bool:
        """
        Check if the Semantic Clarity Principle is confirmed.
        
        Hypothesis: More description → Higher clarity, balance, and harmony
        """
        if len(levels) < 2:
            return False
        
        # Check if trends are generally increasing
        clarity_increasing = levels[-1].clarity > levels[0].clarity
        balance_increasing = levels[-1].balance > levels[0].balance
        concepts_increasing = levels[-1].concepts > levels[0].concepts
        
        # At least 2 of 3 should be increasing
        return sum([clarity_increasing, balance_increasing, concepts_increasing]) >= 2
    
    def score_description_quality(self, description: str) -> Dict:
        """
        Score how well a description captures semantic meaning.
        
        Returns quality score (0-1) and breakdown of factors.
        """
        result = self.engine.analyze_operation(description)
        
        # Calculate component scores
        clarity_score = result.semantic_clarity
        balance_score = self._calculate_balance(result.coordinates)
        
        # Completeness based on concept count
        # Assume 15-20 concepts is "complete" for most systems
        completeness_score = min(1.0, result.concept_count / 15)
        
        # Entropy (multi-faceted nature)
        entropy_score = self._calculate_entropy(result.coordinates)
        
        # Weighted average for overall quality
        quality = (
            clarity_score * 0.35 +
            balance_score * 0.25 +
            completeness_score * 0.25 +
            entropy_score * 0.15
        )
        
        # Determine grade
        if quality >= 0.9:
            grade = 'A'
        elif quality >= 0.8:
            grade = 'B'
        elif quality >= 0.7:
            grade = 'C'
        elif quality >= 0.6:
            grade = 'D'
        else:
            grade = 'F'
        
        return {
            'quality': quality,
            'grade': grade,
            'clarity': clarity_score,
            'balance': balance_score,
            'completeness': completeness_score,
            'entropy': entropy_score,
            'word_count': len(description.split()),
            'concept_count': result.concept_count
        }
    
    def recommend_enrichments(
        self, 
        current_desc: str, 
        target_clarity: float = 0.8
    ) -> Dict:
        """
        Recommend terms to add for better semantic clarity.
        
        Returns recommendations for improving description quality.
        """
        result = self.engine.analyze_operation(current_desc)
        
        if result.semantic_clarity >= target_clarity:
            return {
                'needs_improvement': False,
                'message': f"Description already has good clarity ({result.semantic_clarity:.0%})",
                'recommendations': []
            }
        
        recommendations = []
        
        # Identify missing/weak dimensions
        coords = result.coordinates
        
        if coords.love < 0.2:
            recommendations.append({
                'dimension': 'Love (Connectivity)',
                'current': coords.love,
                'suggestion': 'Add connectivity terms',
                'examples': ['public', 'accessible', 'network', 'connect', 'communicate', 'integrate']
            })
        
        if coords.justice < 0.2:
            recommendations.append({
                'dimension': 'Justice (Security)',
                'current': coords.justice,
                'suggestion': 'Add security terms',
                'examples': ['secure', 'encrypted', 'firewall', 'authenticate', 'authorize', 'validate']
            })
        
        if coords.power < 0.2:
            recommendations.append({
                'dimension': 'Power (Performance)',
                'current': coords.power,
                'suggestion': 'Add performance terms',
                'examples': ['optimized', 'fast', 'efficient', 'scalable', 'performance', 'throughput']
            })
        
        if coords.wisdom < 0.2:
            recommendations.append({
                'dimension': 'Wisdom (Monitoring)',
                'current': coords.wisdom,
                'suggestion': 'Add monitoring terms',
                'examples': ['monitored', 'logging', 'metrics', 'alerts', 'diagnostic', 'observability']
            })
        
        # Check concept count
        if result.concept_count < 10:
            recommendations.append({
                'dimension': 'Overall',
                'current': result.concept_count,
                'suggestion': 'Add more descriptive terms',
                'examples': ['Consider adding technical details', 'protocols', 'technologies', 'capabilities']
            })
        
        return {
            'needs_improvement': True,
            'current_clarity': result.semantic_clarity,
            'target_clarity': target_clarity,
            'gap': target_clarity - result.semantic_clarity,
            'recommendations': recommendations
        }
    
    def compare_descriptions(self, desc1: str, desc2: str) -> Dict:
        """
        Compare two descriptions of the same concept.
        
        Shows which description captures more semantic information.
        """
        quality1 = self.score_description_quality(desc1)
        quality2 = self.score_description_quality(desc2)
        
        winner = 1 if quality1['quality'] > quality2['quality'] else 2
        
        return {
            'description1': {
                'text': desc1,
                'quality': quality1
            },
            'description2': {
                'text': desc2,
                'quality': quality2
            },
            'winner': winner,
            'quality_difference': abs(quality1['quality'] - quality2['quality']),
            'analysis': self._generate_comparison_analysis(quality1, quality2)
        }
    
    def _generate_comparison_analysis(self, q1: Dict, q2: Dict) -> List[str]:
        """Generate analysis comparing two descriptions"""
        analysis = []
        
        # Overall quality
        if abs(q1['quality'] - q2['quality']) < 0.05:
            analysis.append("Descriptions are roughly equivalent in quality")
        else:
            better = "First" if q1['quality'] > q2['quality'] else "Second"
            analysis.append(f"{better} description has higher overall quality")
        
        # Clarity
        if abs(q1['clarity'] - q2['clarity']) > 0.1:
            better = "First" if q1['clarity'] > q2['clarity'] else "Second"
            analysis.append(f"{better} has better semantic clarity")
        
        # Balance
        if abs(q1['balance'] - q2['balance']) > 0.1:
            better = "First" if q1['balance'] > q2['balance'] else "Second"
            analysis.append(f"{better} has better dimensional balance")
        
        # Completeness
        if abs(q1['completeness'] - q2['completeness']) > 0.1:
            better = "First" if q1['completeness'] > q2['completeness'] else "Second"
            analysis.append(f"{better} is more complete")
        
        return analysis
