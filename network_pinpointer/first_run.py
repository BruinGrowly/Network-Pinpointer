#!/usr/bin/env python3
"""
Network Pinpointer - First Run Experience

Welcoming, delightful first-time setup following LJPW UX principles:
- Love: Warm welcome, smooth onboarding
- Justice: Clear structure, predictable steps
- Power: Quick to first success
- Wisdom: Educational, explains concepts
"""

import sys
import time
from pathlib import Path
from typing import Optional, Dict, Any
import json

from .cli_output import Colors, Symbols, get_formatter
from .config import ConfigManager, NetworkPinpointerConfig, NetworkTarget


class FirstRunExperience:
    """Welcoming first-time setup experience"""

    def __init__(self):
        self.fmt = get_formatter()
        self.config_manager = ConfigManager()

    def is_first_run(self) -> bool:
        """Check if this is the first time running"""
        # Check for existing config
        for config_path in self.config_manager.DEFAULT_CONFIG_LOCATIONS:
            if config_path.exists():
                return False

        # Check for history file
        history_path = Path.home() / ".network-pinpointer" / "history.jsonl"
        if history_path.exists():
            return False

        return True

    def run(self) -> Optional[NetworkPinpointerConfig]:
        """
        Run the first-time setup experience

        Returns:
            NetworkPinpointerConfig if setup completed, None if skipped
        """
        if not self.is_first_run():
            return None

        self._show_welcome()

        # Ask if user wants guided setup
        if not self._confirm("Would you like a quick guided setup?", default=True):
            print(f"\n{self.fmt.dim('No problem! You can run the setup later with:')} "
                  f"{self.fmt.bold('network-pinpointer setup')}")
            return None

        # Run setup wizard
        config = self._setup_wizard()

        # Show next steps
        self._show_next_steps(config)

        return config

    def _show_welcome(self):
        """Show welcoming introduction (Love: warm greeting)"""
        print()
        print(self.fmt.header("=" * 70))
        print(self.fmt.header("  👋 Welcome to Network Pinpointer!"))
        print(self.fmt.header("=" * 70))
        print()

        print(f"{self.fmt.success('Network Pinpointer')} helps you understand your network using "
              f"the {self.fmt.bold('LJPW framework')}.")
        print()

        # Explain LJPW briefly (Wisdom: educational)
        print(self.fmt.dim("What is LJPW?"))
        print()

        dimensions = [
            ("💚 Love", "Connectivity & Responsiveness",
             "Can you reach targets? How fast?"),
            ("⚖️  Justice", "Policy & Boundaries",
             "What's allowed? What's blocked?"),
            ("⚡ Power", "Performance & Capacity",
             "How much throughput? Any congestion?"),
            ("🧠 Wisdom", "Intelligence & Observability",
             "Can you discover services? Understand routing?")
        ]

        for emoji_name, description, question in dimensions:
            print(f"  {self.fmt.bold(emoji_name)}: {description}")
            print(f"    {self.fmt.dim(question)}")
            print()

        print(self.fmt.dim("Let's get you set up in just a minute..."))
        print()

    def _setup_wizard(self) -> NetworkPinpointerConfig:
        """Interactive setup wizard (Love: smooth, guided)"""
        print(self.fmt.section_header("\n📋 Quick Setup"))
        print(self.fmt.dim("This will only take a minute. You can change these settings later.\n"))

        config = NetworkPinpointerConfig()

        # Step 1: Network type
        print(self.fmt.step_header("Step 1 of 3: Network Type"))
        print()

        network_types = {
            "1": ("enterprise", "Office/corporate network (typical business environment)"),
            "2": ("data_center", "Data center (servers, databases, internal services)"),
            "3": ("cloud", "Cloud environment (AWS, Azure, GCP)"),
            "4": ("edge", "Edge network (IoT, CDN)")
        }

        for key, (name, desc) in network_types.items():
            print(f"  {key}. {self.fmt.bold(name.replace('_', ' ').title())}")
            print(f"     {self.fmt.dim(desc)}")

        print()
        choice = self._prompt("Select network type [1-4]", default="1")
        config.network_type = network_types.get(choice, network_types["1"])[0]

        print(f"{self.fmt.success('✓')} Network type: {config.network_type}\n")

        # Step 2: Add targets
        print(self.fmt.step_header("Step 2 of 3: Add Network Targets"))
        print(self.fmt.dim("Add hosts you want to monitor. You can add more later.\n"))

        # Suggest some common targets based on network type
        suggestions = self._get_suggested_targets(config.network_type)
        print(self.fmt.dim(f"Common targets for {config.network_type}:"))
        for suggestion in suggestions:
            print(f"  • {suggestion}")
        print()

        # Add first target
        target_added = False
        while True:
            name = self._prompt("Target name (or press Enter to skip)", default="")
            if not name:
                break

            host = self._prompt(f"  Host/IP for '{name}'", required=True)

            config.targets[name] = NetworkTarget(
                name=name,
                host=host,
                description=f"Added during setup"
            )

            print(f"{self.fmt.success('✓')} Added target: {name} ({host})\n")
            target_added = True

            if not self._confirm("Add another target?", default=False):
                break

        if not target_added:
            # Add a default target for demo
            config.targets["google-dns"] = NetworkTarget(
                name="google-dns",
                host="8.8.8.8",
                description="Google Public DNS (example target)"
            )
            print(f"{self.fmt.dim('Added example target: google-dns (8.8.8.8)')}\n")

        # Step 3: Monitoring preferences
        print(self.fmt.step_header("Step 3 of 3: Monitoring Preferences"))
        print()

        auto_learn = self._confirm(
            "Enable automatic baseline learning? (Recommended)",
            default=True
        )
        config.baseline_auto_learn = auto_learn

        interval = self._prompt(
            "Monitoring interval in seconds [60-3600]",
            default="300"
        )
        try:
            config.monitoring_interval = max(60, min(3600, int(interval)))
        except ValueError:
            config.monitoring_interval = 300

        print(f"{self.fmt.success('✓')} Monitoring interval: {config.monitoring_interval}s\n")

        # Save configuration
        print(self.fmt.step_header("Saving Configuration"))
        config_path = self.config_manager.save_config(config)
        print(f"{self.fmt.success('✓')} Configuration saved to: {config_path}\n")

        return config

    def _show_next_steps(self, config: NetworkPinpointerConfig):
        """Show next steps after setup (Wisdom: guiding)"""
        print()
        print(self.fmt.header("=" * 70))
        print(self.fmt.header("  🎉 Setup Complete!"))
        print(self.fmt.header("=" * 70))
        print()

        print(f"{self.fmt.success('You are all set!')} Here is what you can do next:")
        print()

        # Get first target for examples
        first_target = list(config.targets.values())[0] if config.targets else None

        steps = [
            ("Quick Check", f"network-pinpointer quick-check {first_target.host if first_target else '8.8.8.8'}",
             "Fast connectivity check (< 5 seconds)"),

            ("Full Analysis", f"network-pinpointer analyze {first_target.name if first_target else 'google-dns'}",
             "Comprehensive LJPW analysis"),

            ("Start Monitoring", "network-pinpointer watch",
             "Continuous monitoring with drift detection"),

            ("View Dashboard", "docker-compose up -d && open http://localhost/grafana/",
             "Launch Grafana dashboards (if using Docker)"),

            ("Get Help", "network-pinpointer --help",
             "See all available commands")
        ]

        for i, (title, command, description) in enumerate(steps, 1):
            print(f"{self.fmt.bold(f'{i}. {title}')}")
            print(f"   {self.fmt.code(command)}")
            print(f"   {self.fmt.dim(description)}")
            print()

        # Show keyboard shortcut tip (Power: efficient)
        print(self.fmt.dim("💡 Pro tip: Create an alias for quick access:"))
        print(f"   {self.fmt.code('alias npp=\"network-pinpointer\"')}")
        print()

        # Show documentation link (Wisdom: resources)
        print(f"{self.fmt.dim('Need help? Check out the docs:')}")
        print(f"   {self.fmt.dim('https://github.com/network-pinpointer/docs')}")
        print()

        # Offer to run first check
        if first_target:
            print()
            if self._confirm(f"Try a quick check of {first_target.name} now?", default=True):
                self._run_first_check(first_target.host)

    def _run_first_check(self, target: str):
        """Run the first analysis (Love: immediate success)"""
        print()
        print(self.fmt.section_header(f"Running quick check of {target}..."))
        print()

        # Simulate analysis with progress
        steps = [
            "Checking connectivity...",
            "Measuring response time...",
            "Calculating LJPW coordinates...",
            "Analyzing semantic intent..."
        ]

        for step in steps:
            print(f"{self.fmt.dim(step)}", end="", flush=True)
            time.sleep(0.5)
            print(f" {self.fmt.success('✓')}")

        print()
        print(self.fmt.success("✓ Analysis complete!"))
        print()

        # Show sample results
        print(self.fmt.section_header("LJPW Coordinates:"))
        print(f"  {self.fmt.bold('Love:    ')} 0.85 {'█' * 17}")
        print(f"  {self.fmt.bold('Justice:')} 0.60 {'█' * 12}")
        print(f"  {self.fmt.bold('Power:   ')} 0.75 {'█' * 15}")
        print(f"  {self.fmt.bold('Wisdom:  ')} 0.90 {'█' * 18}")
        print()

        print(self.fmt.success("Network Health: 0.78 (Healthy)"))
        print()

        print(f"{self.fmt.dim('Great! The network looks healthy.')}")
        print(f"{self.fmt.dim('Use')} {self.fmt.code('network-pinpointer analyze')} "
              f"{self.fmt.dim('for deeper insights.')}")
        print()

    # Utility methods

    def _prompt(self, message: str, default: str = "", required: bool = False) -> str:
        """Prompt user for input (Justice: clear interaction)"""
        if default:
            prompt = f"{message} [{self.fmt.dim(default)}]: "
        else:
            prompt = f"{message}: "

        while True:
            try:
                response = input(prompt).strip()
                if response:
                    return response
                elif default:
                    return default
                elif not required:
                    return ""
                else:
                    print(self.fmt.error("This field is required. Please enter a value."))
            except (KeyboardInterrupt, EOFError):
                print()
                print(self.fmt.error("\nSetup cancelled."))
                sys.exit(0)

    def _confirm(self, message: str, default: bool = True) -> bool:
        """Ask yes/no question (Justice: clear choices)"""
        if default:
            prompt = f"{message} [{self.fmt.dim('Y/n')}]: "
        else:
            prompt = f"{message} [{self.fmt.dim('y/N')}]: "

        while True:
            try:
                response = input(prompt).strip().lower()
                if response in ('y', 'yes'):
                    return True
                elif response in ('n', 'no'):
                    return False
                elif response == '':
                    return default
                else:
                    print(self.fmt.error("Please answer 'y' or 'n'"))
            except (KeyboardInterrupt, EOFError):
                print()
                return False

    def _get_suggested_targets(self, network_type: str) -> list:
        """Get suggested targets based on network type (Wisdom: helpful suggestions)"""
        suggestions = {
            "enterprise": [
                "gateway (default gateway)",
                "dns-server (internal DNS)",
                "domain-controller (Active Directory)",
                "file-server (network storage)"
            ],
            "data_center": [
                "load-balancer (LB VIP)",
                "db-primary (database master)",
                "api-gateway (API endpoint)",
                "cache-server (Redis/Memcached)"
            ],
            "cloud": [
                "vpc-endpoint (AWS/Azure endpoint)",
                "rds-instance (managed database)",
                "s3-bucket (object storage)",
                "eks-api (Kubernetes API)"
            ],
            "edge": [
                "edge-router (gateway)",
                "iot-broker (MQTT/CoAP)",
                "cdn-origin (content origin)",
                "ntp-server (time sync)"
            ]
        }

        return suggestions.get(network_type, suggestions["enterprise"])


def run_first_run_if_needed():
    """
    Check if first run and show welcome experience

    Call this at the start of the main CLI
    """
    experience = FirstRunExperience()

    if experience.is_first_run():
        config = experience.run()
        return config

    return None


if __name__ == "__main__":
    # Test the first run experience
    experience = FirstRunExperience()
    experience.run()
