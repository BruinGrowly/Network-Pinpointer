#!/usr/bin/env python3
"""
Historical Tracking & Playback - Review network state over time

Features:
- Record network state snapshots
- Play back historical data
- Generate timeline visualizations
- Trend analysis
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict

from .semantic_engine import Coordinates
from .cli_output import get_formatter


@dataclass
class HistoricalSnapshot:
    """A snapshot of network state at a point in time"""
    timestamp: datetime
    target: str
    coordinates: Coordinates
    metadata: Dict
    health_score: float


class HistoryManager:
    """Manages historical network data"""

    def __init__(self, history_dir: str = "./network_history"):
        self.history_dir = Path(history_dir)
        self.history_dir.mkdir(parents=True, exist_ok=True)
        self.fmt = get_formatter()

    def record(
        self,
        target: str,
        coords: Coordinates,
        metadata: Optional[Dict] = None
    ):
        """Record a network state snapshot"""
        timestamp = datetime.now()
        filename = f"{target.replace('.', '_')}_{timestamp.strftime('%Y%m')}.jsonl"
        filepath = self.history_dir / filename

        snapshot = {
            'timestamp': timestamp.isoformat(),
            'target': target,
            'coordinates': {
                'love': coords.love,
                'justice': coords.justice,
                'power': coords.power,
                'wisdom': coords.wisdom
            },
            'health_score': (coords.love + coords.justice + coords.power + coords.wisdom) / 4,
            'metadata': metadata or {}
        }

        # Append to JSONL file (one JSON per line)
        with open(filepath, 'a') as f:
            f.write(json.dumps(snapshot) + '\n')

    def load_history(
        self,
        target: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[HistoricalSnapshot]:
        """Load historical snapshots for a target"""

        snapshots = []

        # Find relevant files
        pattern = f"{target.replace('.', '_')}_*.jsonl"
        files = sorted(self.history_dir.glob(pattern))

        for file in files:
            with open(file, 'r') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        timestamp = datetime.fromisoformat(data['timestamp'])

                        # Filter by time range
                        if start_time and timestamp < start_time:
                            continue
                        if end_time and timestamp > end_time:
                            continue

                        coords = Coordinates(
                            love=data['coordinates']['love'],
                            justice=data['coordinates']['justice'],
                            power=data['coordinates']['power'],
                            wisdom=data['coordinates']['wisdom']
                        )

                        snapshot = HistoricalSnapshot(
                            timestamp=timestamp,
                            target=data['target'],
                            coordinates=coords,
                            metadata=data.get('metadata', {}),
                            health_score=data.get('health_score', 0)
                        )

                        snapshots.append(snapshot)

                    except Exception as e:
                        print(f"Error loading snapshot: {e}")

        return sorted(snapshots, key=lambda s: s.timestamp)

    def playback(
        self,
        target: str,
        hours: int = 24,
        speed: float = 1.0
    ):
        """
        Play back network history

        Args:
            target: Target to play back
            hours: How many hours of history
            speed: Playback speed multiplier (1.0 = real-time)
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)

        snapshots = self.load_history(target, start_time, end_time)

        if not snapshots:
            print(f"No history found for {target}")
            return

        print(self.fmt.section_header(f"Historical Playback: {target}"))
        print(f"Time range: {start_time.strftime('%Y-%m-%d %H:%M')} to {end_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"Snapshots: {len(snapshots)}\n")

        for i, snapshot in enumerate(snapshots):
            print(f"[{snapshot.timestamp.strftime('%Y-%m-%d %H:%M:%S')}]")
            print(f"  L={snapshot.coordinates.love:.2f} "
                  f"J={snapshot.coordinates.justice:.2f} "
                  f"P={snapshot.coordinates.power:.2f} "
                  f"W={snapshot.coordinates.wisdom:.2f} "
                  f"(Health: {snapshot.health_score:.2f})")

            if i < len(snapshots) - 1:
                # Calculate time to next snapshot
                next_snap = snapshots[i + 1]
                delta = (next_snap.timestamp - snapshot.timestamp).total_seconds()
                if speed > 0:
                    time.sleep(delta / speed)

    def generate_timeline(
        self,
        target: str,
        hours: int = 24,
        dimension: Optional[str] = None
    ) -> str:
        """
        Generate ASCII timeline visualization

        Args:
            target: Target to visualize
            hours: Time range
            dimension: Which dimension to plot (or None for health score)
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)

        snapshots = self.load_history(target, start_time, end_time)

        if not snapshots:
            return f"No history found for {target}"

        lines = []
        lines.append(self.fmt.section_header(f"Timeline: {target}"))
        lines.append(f"Time range: Last {hours} hours")

        if dimension:
            lines.append(f"Dimension: {dimension.capitalize()}\n")
        else:
            lines.append("Showing: Health Score\n")

        # Build timeline
        width = 60
        height = 10

        # Get values
        if dimension:
            dim_key = dimension.lower()
            values = [getattr(s.coordinates, dim_key) for s in snapshots]
        else:
            values = [s.health_score for s in snapshots]

        # Normalize to chart height
        min_val = min(values)
        max_val = max(values)
        range_val = max_val - min_val if max_val > min_val else 1

        chart = [[' ' for _ in range(width)] for _ in range(height)]

        # Plot points
        for i, val in enumerate(values):
            x = int((i / len(values)) * (width - 1))
            y = height - 1 - int(((val - min_val) / range_val) * (height - 1))
            chart[y][x] = '█'

        # Add scale
        lines.append(f"{max_val:.2f} |")
        for row in chart:
            lines.append("       |" + ''.join(row))
        lines.append(f"{min_val:.2f} |")
        lines.append("       └" + "─" * width)
        lines.append(f"        {snapshots[0].timestamp.strftime('%H:%M')}"
                    + " " * (width - 20)
                    + f"{snapshots[-1].timestamp.strftime('%H:%M')}")

        # Statistics
        lines.append(f"\nStatistics:")
        lines.append(f"  Min: {min_val:.3f}")
        lines.append(f"  Max: {max_val:.3f}")
        lines.append(f"  Avg: {sum(values)/len(values):.3f}")
        lines.append(f"  Current: {values[-1]:.3f}")

        # Trend
        if len(values) > 1:
            trend = values[-1] - values[0]
            trend_pct = (trend / values[0] * 100) if values[0] > 0 else 0
            direction = "↑" if trend > 0 else "↓" if trend < 0 else "→"
            lines.append(f"  Trend: {direction} {trend:+.3f} ({trend_pct:+.1f}%)")

        return '\n'.join(lines)


if __name__ == "__main__":
    # Demo historical tracking
    from .semantic_engine import Coordinates
    import time

    manager = HistoryManager()

    print("Recording sample history...")

    # Simulate some history
    target = "demo.example.com"
    base_time = datetime.now() - timedelta(hours=2)

    for i in range(10):
        # Simulate degrading network
        love = 0.9 - (i * 0.05)
        power = 0.8 - (i * 0.04)

        coords = Coordinates(
            love=max(0.3, love),
            justice=0.35,
            power=max(0.3, power),
            wisdom=0.85
        )

        # Fake the timestamp
        snapshot_time = base_time + timedelta(minutes=i * 15)

        snapshot = {
            'timestamp': snapshot_time.isoformat(),
            'target': target,
            'coordinates': {
                'love': coords.love,
                'justice': coords.justice,
                'power': coords.power,
                'wisdom': coords.wisdom
            },
            'health_score': (coords.love + coords.justice + coords.power + coords.wisdom) / 4,
            'metadata': {}
        }

        filename = f"{target.replace('.', '_')}_{snapshot_time.strftime('%Y%m')}.jsonl"
        filepath = manager.history_dir / filename

        with open(filepath, 'a') as f:
            f.write(json.dumps(snapshot) + '\n')

    print(f"✓ Recorded {10} snapshots\n")

    # Show timeline
    timeline = manager.generate_timeline(target, hours=24, dimension="love")
    print(timeline)
