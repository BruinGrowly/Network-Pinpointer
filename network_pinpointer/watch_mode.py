#!/usr/bin/env python3
"""
Watch Mode - Continuous network monitoring

Monitors network state continuously and alerts on changes.
"""

import time
import signal
import sys
from datetime import datetime, timedelta
from typing import Optional, Callable, List
from pathlib import Path

from .real_packet_capture import get_packet_capture
from .semantic_packet_analyzer import SemanticPacketAnalyzer
from .holistic_health import NetworkHealthTracker
from .diff_mode import DiffAnalyzer
from .cli_output import get_formatter
from .semantic_engine import Coordinates


class WatchMode:
    """Continuous monitoring mode"""

    def __init__(
        self,
        targets: List[str],
        interval: int = 300,  # seconds
        alert_callback: Optional[Callable] = None
    ):
        self.targets = targets
        self.interval = interval
        self.alert_callback = alert_callback
        self.running = False

        self.capture = get_packet_capture()
        self.analyzer = SemanticPacketAnalyzer()
        self.tracker = NetworkHealthTracker()
        self.differ = DiffAnalyzer()
        self.fmt = get_formatter()

        self.previous_states = {}  # target -> Coordinates
        self.alert_history = []

        # Handle Ctrl+C gracefully
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, sig, frame):
        """Handle interrupt signal"""
        print(f"\n\n{self.fmt.info('Watch mode stopped by user')}")
        self.stop()
        sys.exit(0)

    def start(self):
        """Start continuous monitoring"""
        self.running = True

        print(self.fmt.section_header("Network Watch Mode"))
        print(f"\nMonitoring {len(self.targets)} target(s)")
        print(f"Check interval: {self.interval}s")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\nPress Ctrl+C to stop\n")

        iteration = 0

        while self.running:
            iteration += 1
            timestamp = datetime.now()

            print(f"[{timestamp.strftime('%H:%M:%S')}] Check #{iteration}")

            for target in self.targets:
                self._check_target(target, timestamp)

            # Wait for next interval
            if self.running:
                print(f"Next check in {self.interval}s...")
                time.sleep(self.interval)

    def stop(self):
        """Stop monitoring"""
        self.running = False

        if self.alert_history:
            print(f"\n{self.fmt.subsection_header('Alert Summary')}")
            print(f"Total alerts: {len(self.alert_history)}")

            # Show recent alerts
            recent = self.alert_history[-5:]
            for alert in recent:
                print(f"  [{alert['timestamp']}] {alert['target']}: {alert['message']}")

    def _check_target(self, target: str, timestamp: datetime):
        """Check a single target"""
        try:
            # Capture packets
            if hasattr(self.capture, 'capture_icmp_via_ping'):
                packets = self.capture.capture_icmp_via_ping(target, count=5)

                if not packets:
                    self._alert(target, "No response", timestamp)
                    return

                # Analyze
                result = self.analyzer.analyze_icmp_packets(packets)
                current_coords = result.coordinates

                # Check for changes
                if target in self.previous_states:
                    previous_coords = self.previous_states[target]

                    # Calculate drift
                    total_drift = (
                        abs(current_coords.love - previous_coords.love) +
                        abs(current_coords.justice - previous_coords.justice) +
                        abs(current_coords.power - previous_coords.power) +
                        abs(current_coords.wisdom - previous_coords.wisdom)
                    )

                    if total_drift > 0.3:  # Significant change
                        analysis = self.differ.compare_states(
                            previous_coords, current_coords,
                            "Previous", "Current"
                        )

                        message = f"State changed (drift: {total_drift:.2f})"

                        # Add details about major changes
                        major = analysis.get('major_changes', [])
                        if major:
                            details = ", ".join(f"{c.dimension} {c.change:+.2f}" for c in major[:2])
                            message += f" - {details}"

                        self._alert(target, message, timestamp)

                        # Show details
                        print(f"    Change detected:")
                        for cause in analysis.get('likely_causes', [])[:2]:
                            print(f"      • {cause}")

                # Store current state
                self.previous_states[target] = current_coords

                # Display status
                health = (current_coords.love + current_coords.power + current_coords.wisdom) / 3
                status = "✓" if health > 0.7 else "⚠️" if health > 0.5 else "✗"
                print(f"  {status} {target}: L={current_coords.love:.2f} J={current_coords.justice:.2f} "
                      f"P={current_coords.power:.2f} W={current_coords.wisdom:.2f}")

        except Exception as e:
            print(f"  ✗ {target}: Error - {e}")

    def _alert(self, target: str, message: str, timestamp: datetime):
        """Generate an alert"""
        alert = {
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'target': target,
            'message': message
        }

        self.alert_history.append(alert)

        # Print alert
        print(f"  🚨 ALERT: {target} - {message}")

        # Call callback if provided
        if self.alert_callback:
            self.alert_callback(alert)


if __name__ == "__main__":
    # Demo watch mode
    import sys

    targets = sys.argv[1:] if len(sys.argv) > 1 else ["8.8.8.8"]

    watcher = WatchMode(targets, interval=10)  # 10s for demo
    watcher.start()
