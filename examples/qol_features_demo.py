#!/usr/bin/env python3
"""
Quality of Life Features Demo

Demonstrates all the QoL improvements to Network Pinpointer:
1. Rich CLI Output (colors, progress bars, visual displays)
2. Quick Commands (fast operations)
3. Diagnostic Recipes (pre-built workflows)
4. Root Cause Prioritization (smart issue ranking)
5. Interactive Mode (guided workflows)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from network_pinpointer.cli_output import OutputFormatter, Symbols, Colors
from network_pinpointer.semantic_engine import Coordinates
from network_pinpointer.diagnostic_recipes import RecipeLibrary
from network_pinpointer.root_cause_analyzer import RootCauseAnalyzer
from network_pinpointer.quick_commands import QuickCommands
import time


def demo_rich_output():
    """Demo 1: Rich CLI Output Formatting"""
    fmt = OutputFormatter()

    print(fmt.section_header("DEMO 1: Rich CLI Output Formatting"))

    print(fmt.subsection_header("Status Messages"))
    print(fmt.success("Network connectivity established"))
    print(fmt.error("Failed to reach 192.168.1.50"))
    print(fmt.warning("High latency detected (250ms)"))
    print(fmt.info("Running diagnostics..."))

    print(fmt.subsection_header("\nProgress Bars"))
    for i in range(0, 101, 25):
        print(f"\r{fmt.progress_bar(i, 100, prefix='Scanning network')}", end="")
        time.sleep(0.3)
    print()  # Newline

    print(fmt.subsection_header("\nLJPW Coordinate Display"))
    coords = Coordinates(love=0.85, justice=0.35, power=0.65, wisdom=0.90)
    print(fmt.coordinates_display(coords))

    print(fmt.subsection_header("\nHealth Score Display"))
    print(fmt.health_score_display(0.92))
    print(fmt.health_score_display(0.65))
    print(fmt.health_score_display(0.35))

    print(fmt.subsection_header("\nPriority Indicators"))
    for priority in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        print(f"  {fmt.priority_indicator(priority)} - {priority} severity issue")

    print(fmt.subsection_header("\nBefore/After Comparisons"))
    print(fmt.comparison("Love", 0.85, 0.45))
    print(fmt.comparison("Justice", 0.35, 0.75))
    print(fmt.comparison("Power", 0.70, 0.72))

    print(fmt.subsection_header("\nLists"))
    print(fmt.bullet_list([
        "Check network connectivity",
        "Verify DNS resolution",
        "Test port accessibility"
    ], indent=2))

    print(fmt.subsection_header("\nTable Display"))
    print(fmt.table(
        headers=["Dimension", "Value", "Status"],
        rows=[
            ["Love", "0.85", "GOOD"],
            ["Justice", "0.35", "FAIR"],
            ["Power", "0.65", "GOOD"],
            ["Wisdom", "0.90", "EXCELLENT"]
        ]
    ))

    input("\n\nPress Enter to continue to next demo...")


def demo_diagnostic_recipes():
    """Demo 2: Diagnostic Recipes System"""
    fmt = OutputFormatter()
    library = RecipeLibrary()

    print("\n" + fmt.section_header("DEMO 2: Diagnostic Recipes System"))

    print("\nDiagnostic recipes are pre-built workflows for common network problems.")
    print("Each recipe knows which tests to run and which dimensions to focus on.\n")

    print(library.display_all_recipes())

    print(fmt.subsection_header("\nRecipe Plan Example"))
    print("\nLet's see the plan for diagnosing slow connections:\n")

    recipe = library.get_recipe("slow_connection")
    print(recipe.display_plan())

    print(fmt.subsection_header("\nSmart Recipe Recommendations"))
    print("\nThe system can recommend recipes based on symptoms:\n")

    symptoms_tests = [
        (["slow", "latency"], "slow_connection"),
        (["can't connect"], "cant_connect"),
        (["intermittent", "flaky"], "intermittent"),
        (["security"], "security_audit")
    ]

    for symptoms, expected in symptoms_tests:
        recommended = library.recommend_recipe(symptoms)
        match = "✓" if recommended == expected else "✗"
        print(f"  {match} Symptoms: {symptoms} → Recommends: {recommended}")

    input("\n\nPress Enter to continue to next demo...")


def demo_root_cause_analysis():
    """Demo 3: Root Cause Prioritization"""
    fmt = OutputFormatter()
    analyzer = RootCauseAnalyzer()

    print("\n" + fmt.section_header("DEMO 3: Root Cause Prioritization"))

    print("\nThe root cause analyzer takes diagnostic results and:")
    print("  • Identifies what's wrong (root cause)")
    print("  • Ranks issues by severity and impact")
    print("  • Provides actionable recommendations")
    print("  • Determines optimal fix order\n")

    print(fmt.subsection_header("Scenario: Over-Secured Network"))
    print("\nNetwork with high security causing connectivity problems:\n")

    # Over-secured network scenario
    coords = Coordinates(love=0.25, justice=0.75, power=0.55, wisdom=0.60)
    metadata = {
        "packet_loss": 0.15,
        "route_changing": True,
        "ttl_variance": 3.5,
        "avg_hops": 12
    }

    print(f"Raw Coordinates: L={coords.love:.2f}, J={coords.justice:.2f}, "
          f"P={coords.power:.2f}, W={coords.wisdom:.2f}")
    print(f"Metadata: {metadata}\n")

    analysis = analyzer.analyze(coords, metadata)
    print(analyzer.display_analysis(analysis))

    input("\n\nPress Enter to continue to next demo...")


def demo_quick_commands():
    """Demo 4: Quick Commands (Simulated)"""
    fmt = OutputFormatter()

    print("\n" + fmt.section_header("DEMO 4: Quick Commands"))

    print("\nQuick commands provide fast, single-command operations:\n")

    commands = [
        ("pinpoint quick-check [target]", "Quick 30-second health assessment"),
        ("pinpoint ping <target>", "Enhanced ping with semantic analysis"),
        ("pinpoint health", "Show network health status"),
        ("pinpoint explain <topic>", "Learn about LJPW dimensions"),
        ("pinpoint run <recipe>", "Run a diagnostic recipe"),
        ("pinpoint interactive", "Start guided diagnostic mode")
    ]

    print(fmt.table(
        headers=["Command", "Description"],
        rows=commands,
        column_widths=[35, 45]
    ))

    print(fmt.subsection_header("\nExplain Command Example"))
    print("\nThe 'explain' command teaches users about LJPW dimensions:")
    print(f"\n{fmt.color('$ pinpoint explain love', Colors.CYAN)}\n")
    print("Would show detailed explanation of the Love dimension:")
    print("  • What it means")
    print("  • What high/low values indicate")
    print("  • What affects it")
    print("  • How to improve it")

    input("\n\nPress Enter to continue to next demo...")


def demo_all_together():
    """Demo 5: Everything Working Together"""
    fmt = OutputFormatter()

    print("\n" + fmt.section_header("DEMO 5: Complete Diagnostic Workflow"))

    print("\nA typical diagnostic session combines all features:\n")

    workflow = [
        ("User runs:", "pinpoint interactive"),
        ("System shows:", "Interactive menu with guided options"),
        ("User selects:", "Option 2: Connection is too slow"),
        ("System asks:", "Enter target IP or hostname"),
        ("User enters:", "api.example.com"),
        ("System recommends:", "slow_connection recipe"),
        ("System shows:", "Recipe plan with estimated time"),
        ("User confirms:", "y (yes, run it)"),
        ("System executes:", "Ping, traceroute, packet capture tests"),
        ("System displays:", "Rich LJPW coordinates with colors"),
        ("System analyzes:", "Root cause prioritization"),
        ("System provides:", "Ranked issues with fix recommendations"),
        ("User can:", "Explain dimensions, export results, etc.")
    ]

    for step, action in workflow:
        print(f"{fmt.bold(step):20} {action}")

    print(fmt.subsection_header("\nKey Benefits"))
    print(fmt.bullet_list([
        "No need to remember complex commands",
        "Guided workflow for non-experts",
        "Visual, easy-to-understand output",
        "Smart recommendations based on symptoms",
        "Prioritized action items (fix this first!)",
        "Educational (learn while diagnosing)"
    ], indent=2))

    print(fmt.subsection_header("\nQuality of Life Features Summary"))

    features = [
        ("Rich Output", "Colors, progress bars, visual charts", "✓ Implemented"),
        ("Quick Commands", "Fast common operations", "✓ Implemented"),
        ("Recipes", "Pre-built diagnostic workflows", "✓ Implemented"),
        ("Root Cause", "Smart issue prioritization", "✓ Implemented"),
        ("Interactive", "Guided diagnostic mode", "✓ Implemented"),
        ("Explain", "Learn LJPW on-the-fly", "✓ Implemented")
    ]

    print()
    print(fmt.table(
        headers=["Feature", "Description", "Status"],
        rows=features,
        column_widths=[15, 35, 20]
    ))


def main():
    """Run all demos"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║           NETWORK PINPOINTER - QUALITY OF LIFE FEATURES              ║
║                    Demonstration & Walkthrough                       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

This demo showcases all the UX improvements that make Network Pinpointer
easy and pleasant to use:

  1. Rich CLI Output - Beautiful, colorful, informative displays
  2. Diagnostic Recipes - Pre-built workflows for common problems
  3. Root Cause Analysis - Smart prioritization of issues
  4. Quick Commands - Fast operations for power users
  5. Complete Workflow - Everything working together

Press Enter to begin...
    """)

    input()

    try:
        demo_rich_output()
        demo_diagnostic_recipes()
        demo_root_cause_analysis()
        demo_quick_commands()
        demo_all_together()

        print("\n" + "=" * 70)
        print(OutputFormatter().section_header("Demo Complete!"))
        print("""
Thank you for exploring the Quality of Life features!

To try it yourself:
  ./pinpoint interactive         # Start guided mode
  ./pinpoint quick-check         # Quick health test
  ./pinpoint recipes             # See all available recipes
  ./pinpoint explain ljpw        # Learn about the framework

For more information:
  ./pinpoint --help
        """)
        print("=" * 70 + "\n")

    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Goodbye!")


if __name__ == "__main__":
    main()
