#!/usr/bin/env python3
"""
Interactive Mode - Guided diagnostic workflows

Provides an interactive, menu-driven interface for network diagnostics.
Guides users through problem diagnosis step-by-step.
"""

import sys
from typing import Optional, Dict, Any

from .cli_output import get_formatter
from .diagnostic_recipes import RecipeLibrary, display_recipe_menu
from .quick_commands import QuickCommands
from .real_packet_capture import get_packet_capture
from .semantic_packet_analyzer import SemanticPacketAnalyzer
from .root_cause_analyzer import RootCauseAnalyzer


class InteractiveMode:
    """Interactive diagnostic session"""

    def __init__(self):
        self.fmt = get_formatter()
        self.library = RecipeLibrary()
        self.quick = QuickCommands()
        self.capture = get_packet_capture()
        self.analyzer = SemanticPacketAnalyzer()
        self.root_cause = RootCauseAnalyzer()

    def run(self):
        """Run interactive mode"""
        self.show_welcome()

        while True:
            print("\n")
            choice = self.show_main_menu()

            if choice == 'q':
                self.show_goodbye()
                break
            elif choice == '1':
                self.run_guided_diagnosis()
            elif choice == '2':
                self.run_recipe()
            elif choice == '3':
                self.quick.quick_check(self.get_target())
            elif choice == '4':
                self.quick.show_health()
            elif choice == '5':
                self.show_help()
            else:
                print(self.fmt.warning("Invalid choice. Please try again."))

    def show_welcome(self):
        """Show welcome message"""
        print(self.fmt.section_header("Network Pinpointer - Interactive Mode"))
        print("""
Welcome! This interactive tool will guide you through network diagnostics
using the LJPW semantic framework.

The four dimensions:
  • Love (L)    - Connectivity and relationships
  • Justice (J) - Policy, security, and boundaries
  • Power (P)   - Performance and capacity
  • Wisdom (W)  - Visibility and monitoring

Let's diagnose your network!
        """)

    def show_goodbye(self):
        """Show goodbye message"""
        print("\n" + self.fmt.success("Thank you for using Network Pinpointer!"))
        print("For more help, visit the documentation or run with --help\n")

    def show_main_menu(self) -> str:
        """Show main menu and get choice"""
        print(self.fmt.subsection_header("What would you like to do?"))
        print("""
  1. Guided Diagnosis (I'll help you figure out what's wrong)
  2. Run a Diagnostic Recipe (Pre-built workflows)
  3. Quick Health Check (Fast 30-second test)
  4. View Network Health Status
  5. Learn about LJPW dimensions

  q. Quit
        """)

        choice = input("Enter your choice (1-5, or q): ").strip().lower()
        return choice

    def run_guided_diagnosis(self):
        """Run guided diagnosis workflow"""
        print(self.fmt.section_header("Guided Diagnosis"))

        # Step 1: Describe the problem
        print("\nLet's start by understanding your problem.\n")
        print("What symptoms are you experiencing?")
        print("  1. Can't connect to a service")
        print("  2. Connection is too slow")
        print("  3. Connection works sometimes, not others")
        print("  4. Want to check security configuration")
        print("  5. Just want to establish a baseline")
        print("  6. Other / Not sure")

        symptom = input("\nSelect (1-6): ").strip()

        symptom_map = {
            "1": ["can't connect", "unreachable"],
            "2": ["slow", "latency"],
            "3": ["intermittent", "flaky"],
            "4": ["security", "firewall"],
            "5": ["baseline", "healthy"],
            "6": ["unknown"]
        }

        symptoms = symptom_map.get(symptom, ["unknown"])

        # Step 2: Get target
        if symptom in ["1", "2", "3"]:
            target = self.get_target()
        else:
            target = None

        # Step 3: Recommend recipe
        recipe_name = self.library.recommend_recipe(symptoms)
        recipe = self.library.get_recipe(recipe_name)

        if not recipe:
            print(self.fmt.warning("Couldn't determine appropriate diagnostic."))
            print(self.fmt.info("Running quick health check instead..."))
            self.quick.quick_check(target or "8.8.8.8")
            return

        # Step 4: Show plan
        print("\n" + recipe.display_plan())

        # Step 5: Confirm
        confirm = input("\nRun this diagnostic? (y/n): ").strip().lower()

        if confirm == 'y':
            print("\n" + self.fmt.info("Starting diagnostic..."))
            self.execute_recipe(recipe, target)
        else:
            print(self.fmt.info("Diagnostic cancelled."))

    def run_recipe(self):
        """Run a specific recipe"""
        print(display_recipe_menu())

        choice = input("\nEnter choice (1-6): ").strip()

        recipe_map = {
            "1": "slow_connection",
            "2": "cant_connect",
            "3": "intermittent",
            "4": "security_audit",
            "5": "baseline",
            "6": "quick_check"
        }

        recipe_name = recipe_map.get(choice)

        if not recipe_name:
            print(self.fmt.warning("Invalid choice."))
            return

        recipe = self.library.get_recipe(recipe_name)

        if recipe:
            target = self.get_target()
            print("\n" + recipe.display_plan())
            print("\n" + self.fmt.info("Starting diagnostic..."))
            self.execute_recipe(recipe, target)

    def execute_recipe(self, recipe, target: Optional[str]):
        """Execute a diagnostic recipe"""
        # For now, we'll run a simplified version
        # In a full implementation, this would execute each step

        if not target:
            target = "8.8.8.8"

        print(f"\n{self.fmt.subsection_header('Running Diagnostics')}")

        try:
            # Run basic diagnostics
            if hasattr(self.capture, 'capture_icmp_via_ping'):
                print(self.fmt.spinner("Gathering data...", 0))

                packets = self.capture.capture_icmp_via_ping(target, count=20)

                if not packets:
                    print(self.fmt.error(f"Cannot reach {target}"))
                    return

                print(self.fmt.success(f"Collected {len(packets)} packets"))

                # Analyze
                print(self.fmt.spinner("Analyzing semantics...", 1))
                result = self.analyzer.analyze_icmp_packets(packets)

                # Display results
                print("\n" + self.fmt.section_header("Diagnostic Results"))
                print(self.fmt.coordinates_display(result.coordinates))

                # Root cause analysis
                metadata = {
                    "packet_loss": (20 - len(packets)) / 20,
                    "avg_ttl": sum(p.ttl for p in packets) / len(packets) if packets else 64
                }

                analysis = self.root_cause.analyze(result.coordinates, metadata)
                print("\n" + self.root_cause.display_analysis(analysis))

                # Ask if they want explanations
                print("\n")
                explain = input("Would you like me to explain any dimension? (love/justice/power/wisdom/n): ").strip().lower()

                if explain in ["love", "justice", "power", "wisdom"]:
                    print("\n")
                    self.quick.explain(explain)

            else:
                print(self.fmt.error("Packet capture not available"))

        except Exception as e:
            print(self.fmt.error(f"Diagnostic failed: {e}"))

    def get_target(self) -> str:
        """Get target from user"""
        target = input("\nEnter target IP or hostname (or press Enter for 8.8.8.8): ").strip()

        if not target:
            target = "8.8.8.8"
            print(self.fmt.dim(f"Using default: {target}"))

        return target

    def show_help(self):
        """Show help information"""
        print(self.fmt.section_header("Understanding LJPW Dimensions"))

        print("""
The Network Pinpointer uses four semantic dimensions to understand
your network. Each dimension represents a fundamental aspect:

{love} Love (Connectivity)
  How well things connect and communicate
  • High Love = Good connectivity, low packet loss
  • Low Love = Connection problems, isolation

{justice} Justice (Policy/Security)
  Rules, boundaries, and enforcement
  • High Justice = Active security, strict policies
  • Low Justice = Open network, minimal restrictions

{power} Power (Performance)
  Capacity, throughput, efficiency
  • High Power = Fast, efficient, low latency
  • Low Power = Slow, complex paths, bottlenecks

{wisdom} Wisdom (Visibility)
  How well you can observe and understand
  • High Wisdom = Clear visibility, good monitoring
  • Low Wisdom = Blind spots, limited information

For detailed explanations, select option 5 from the main menu.
        """.format(
            love=self.fmt.bold("📗"),
            justice=self.fmt.bold("⚖️"),
            power=self.fmt.bold("⚡"),
            wisdom=self.fmt.bold("🔍")
        ))

        input("\nPress Enter to continue...")


def main():
    """Main entry point for interactive mode"""
    try:
        mode = InteractiveMode()
        mode.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
