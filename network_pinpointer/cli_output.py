#!/usr/bin/env python3
"""
CLI Output Formatting - Rich, colorful, and user-friendly output

Provides formatted output with:
- Color-coded results
- Progress bars
- Visual LJPW coordinate displays
- Clear status indicators
"""

import sys
from typing import Optional, List, Dict
from dataclasses import dataclass
from .semantic_engine import Coordinates


# ANSI Color Codes
class Colors:
    """ANSI color codes for terminal output"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright foreground colors
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"

    # Background colors
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"


class Symbols:
    """Unicode symbols for output"""
    CHECK = "✓"
    CROSS = "✗"
    WARNING = "⚠️"
    INFO = "ℹ️"
    ARROW = "→"
    UP_ARROW = "↑"
    DOWN_ARROW = "↓"
    RIGHT_ARROW = "▶"
    BULLET = "•"
    CIRCLE = "○"
    FILLED_CIRCLE = "●"
    BOX = "□"
    FILLED_BOX = "■"
    STAR = "★"
    FIRE = "🔥"
    CHART = "📊"
    NETWORK = "🌐"
    HEALTH = "🏥"
    SEARCH = "🔍"
    LIGHT = "💡"
    CRITICAL = "🔴"
    HIGH = "🟠"
    MEDIUM = "🟡"
    LOW = "🟢"


class OutputFormatter:
    """Formats output for CLI display"""

    def __init__(self, use_colors: bool = True, use_emoji: bool = True):
        self.use_colors = use_colors and sys.stdout.isatty()
        self.use_emoji = use_emoji

    def color(self, text: str, color: str) -> str:
        """Apply color to text if colors enabled"""
        if not self.use_colors:
            return text
        return f"{color}{text}{Colors.RESET}"

    def bold(self, text: str) -> str:
        """Make text bold"""
        if not self.use_colors:
            return text
        return f"{Colors.BOLD}{text}{Colors.RESET}"

    def dim(self, text: str) -> str:
        """Make text dimmed"""
        if not self.use_colors:
            return text
        return f"{Colors.DIM}{text}{Colors.RESET}"

    def code(self, text: str) -> str:
        """Format text as inline code"""
        if not self.use_colors:
            return f"`{text}`"
        return self.color(f"`{text}`", Colors.CYAN)

    def success(self, text: str) -> str:
        """Format success message"""
        symbol = Symbols.CHECK if self.use_emoji else "[OK]"
        return self.color(f"{symbol} {text}", Colors.GREEN)

    def error(self, text: str) -> str:
        """Format error message"""
        symbol = Symbols.CROSS if self.use_emoji else "[ERROR]"
        return self.color(f"{symbol} {text}", Colors.RED)

    def warning(self, text: str) -> str:
        """Format warning message"""
        symbol = Symbols.WARNING if self.use_emoji else "[WARN]"
        return self.color(f"{symbol} {text}", Colors.YELLOW)

    def info(self, text: str) -> str:
        """Format info message"""
        symbol = Symbols.INFO if self.use_emoji else "[INFO]"
        return self.color(f"{symbol} {text}", Colors.CYAN)

    def section_header(self, text: str, width: int = 70) -> str:
        """Format a section header"""
        separator = "=" * width
        return f"\n{self.bold(separator)}\n{self.bold(text)}\n{self.bold(separator)}"

    def subsection_header(self, text: str) -> str:
        """Format a subsection header"""
        return f"\n{self.bold(text)}"

    def step_header(self, text: str) -> str:
        """Format a step header for wizard/setup steps"""
        arrow = Symbols.RIGHT_ARROW if self.use_emoji else ">"
        separator = "─" * 60
        header_line = f"{arrow} {text}"
        return f"\n{self.color(separator, Colors.CYAN)}\n{self.bold(self.color(header_line, Colors.BRIGHT_CYAN))}\n{self.color(separator, Colors.CYAN)}"

    def progress_bar(
        self,
        current: int,
        total: int,
        width: int = 30,
        prefix: str = "",
        suffix: str = ""
    ) -> str:
        """Generate a progress bar"""
        if total == 0:
            percent = 100
        else:
            percent = int((current / total) * 100)

        filled = int((current / total) * width) if total > 0 else width
        bar = "█" * filled + "░" * (width - filled)

        percentage_str = f"{percent}%"
        count_str = f"({current}/{total})"

        result = f"{prefix} [{bar}] {percentage_str} {count_str} {suffix}"

        if percent == 100:
            return self.color(result, Colors.GREEN)
        elif percent >= 50:
            return self.color(result, Colors.YELLOW)
        else:
            return self.color(result, Colors.CYAN)

    def dimension_bar(
        self,
        name: str,
        value: float,
        width: int = 20,
        show_status: bool = True
    ) -> str:
        """Display LJPW dimension with visual bar"""
        # Determine color and status
        if value >= 0.8:
            color = Colors.GREEN
            status = "EXCELLENT" if show_status else ""
            symbol = Symbols.CHECK if self.use_emoji else ""
        elif value >= 0.6:
            color = Colors.BRIGHT_GREEN
            status = "GOOD" if show_status else ""
            symbol = Symbols.CHECK if self.use_emoji else ""
        elif value >= 0.4:
            color = Colors.YELLOW
            status = "FAIR" if show_status else ""
            symbol = Symbols.WARNING if self.use_emoji else ""
        elif value >= 0.2:
            color = Colors.BRIGHT_YELLOW
            status = "POOR" if show_status else ""
            symbol = Symbols.WARNING if self.use_emoji else ""
        else:
            color = Colors.RED
            status = "CRITICAL" if show_status else ""
            symbol = Symbols.CROSS if self.use_emoji else ""

        # Create bar
        filled = int(value * width)
        bar = "█" * filled + "░" * (width - filled)

        # Format output
        value_str = f"{value:.2f}"
        status_str = f"  {status}" if show_status else ""
        symbol_str = f"{symbol} " if symbol else ""

        line = f"{symbol_str}{name:12} {value_str}  {bar}{status_str}"
        return self.color(line, color)

    def coordinates_display(self, coords: Coordinates, show_labels: bool = True) -> str:
        """Display full LJPW coordinates"""
        lines = []

        if show_labels:
            lines.append(self.subsection_header("LJPW Coordinates"))

        lines.append(self.dimension_bar("Love", coords.love))
        lines.append(self.dimension_bar("Justice", coords.justice))
        lines.append(self.dimension_bar("Power", coords.power))
        lines.append(self.dimension_bar("Wisdom", coords.wisdom))

        return "\n".join(lines)

    def health_score_display(self, score: float) -> str:
        """Display health score with visual indicator"""
        percentage = int(score * 100)

        if score >= 0.8:
            color = Colors.GREEN
            status = "EXCELLENT"
            symbol = "🎉" if self.use_emoji else "[++]"
        elif score >= 0.6:
            color = Colors.BRIGHT_GREEN
            status = "GOOD"
            symbol = Symbols.CHECK if self.use_emoji else "[+]"
        elif score >= 0.4:
            color = Colors.YELLOW
            status = "FAIR"
            symbol = Symbols.WARNING if self.use_emoji else "[~]"
        elif score >= 0.2:
            color = Colors.BRIGHT_YELLOW
            status = "POOR"
            symbol = "⚠️" if self.use_emoji else "[-]"
        else:
            color = Colors.RED
            status = "CRITICAL"
            symbol = Symbols.CRITICAL if self.use_emoji else "[--]"

        return self.color(f"{symbol} Health Score: {percentage}% ({status})", color)

    def priority_indicator(self, priority: str) -> str:
        """Display priority indicator"""
        priority_upper = priority.upper()

        if priority_upper == "CRITICAL":
            symbol = Symbols.CRITICAL if self.use_emoji else "[CRIT]"
            return self.color(f"{symbol} CRITICAL", Colors.BRIGHT_RED)
        elif priority_upper == "HIGH":
            symbol = Symbols.HIGH if self.use_emoji else "[HIGH]"
            return self.color(f"{symbol} HIGH", Colors.RED)
        elif priority_upper == "MEDIUM":
            symbol = Symbols.MEDIUM if self.use_emoji else "[MED]"
            return self.color(f"{symbol} MEDIUM", Colors.YELLOW)
        else:  # LOW
            symbol = Symbols.LOW if self.use_emoji else "[LOW]"
            return self.color(f"{symbol} LOW", Colors.GREEN)

    def bullet_list(self, items: List[str], indent: int = 0) -> str:
        """Format a bullet list"""
        bullet = Symbols.BULLET if self.use_emoji else "-"
        indent_str = " " * indent
        lines = [f"{indent_str}{bullet} {item}" for item in items]
        return "\n".join(lines)

    def numbered_list(self, items: List[str], indent: int = 0) -> str:
        """Format a numbered list"""
        indent_str = " " * indent
        lines = [f"{indent_str}{i}. {item}" for i, item in enumerate(items, 1)]
        return "\n".join(lines)

    def table(
        self,
        headers: List[str],
        rows: List[List[str]],
        column_widths: Optional[List[int]] = None
    ) -> str:
        """Format a simple table"""
        if not rows:
            return ""

        # Calculate column widths if not provided
        if column_widths is None:
            column_widths = [
                max(len(str(header)), max(len(str(row[i])) for row in rows))
                for i, header in enumerate(headers)
            ]

        # Create separator
        separator = "─" * (sum(column_widths) + len(headers) * 3 + 1)

        # Format header
        header_row = "│ " + " │ ".join(
            str(h).ljust(w) for h, w in zip(headers, column_widths)
        ) + " │"

        # Format rows
        data_rows = []
        for row in rows:
            row_str = "│ " + " │ ".join(
                str(cell).ljust(w) for cell, w in zip(row, column_widths)
            ) + " │"
            data_rows.append(row_str)

        # Combine
        lines = [
            separator,
            self.bold(header_row),
            separator,
            *data_rows,
            separator
        ]

        return "\n".join(lines)

    def comparison(self, label: str, before: float, after: float) -> str:
        """Show before/after comparison"""
        diff = after - before
        diff_pct = (diff / before * 100) if before != 0 else 0

        if diff > 0:
            arrow = Symbols.UP_ARROW if self.use_emoji else "↑"
            color = Colors.GREEN if diff_pct > 10 else Colors.BRIGHT_GREEN
            sign = "+"
        elif diff < 0:
            arrow = Symbols.DOWN_ARROW if self.use_emoji else "↓"
            color = Colors.RED if diff_pct < -10 else Colors.BRIGHT_YELLOW
            sign = ""
        else:
            arrow = "→" if self.use_emoji else "-"
            color = Colors.WHITE
            sign = ""

        comparison_str = f"{label:10} {before:.2f} → {after:.2f}  ({sign}{diff_pct:.0f}%)  {arrow}"

        if abs(diff_pct) > 10:
            return self.bold(self.color(comparison_str, color))
        else:
            return self.color(comparison_str, color)

    def spinner(self, text: str, frame: int = 0) -> str:
        """Show a spinner animation"""
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"] if self.use_emoji else ["|", "/", "-", "\\"]
        spinner_char = frames[frame % len(frames)]
        return self.color(f"{spinner_char} {text}", Colors.CYAN)


# Global formatter instance
_formatter: Optional[OutputFormatter] = None


def get_formatter(use_colors: bool = True, use_emoji: bool = True) -> OutputFormatter:
    """Get or create global formatter instance"""
    global _formatter
    if _formatter is None:
        _formatter = OutputFormatter(use_colors, use_emoji)
    return _formatter


def print_success(message: str):
    """Print success message"""
    print(get_formatter().success(message))


def print_error(message: str):
    """Print error message"""
    print(get_formatter().error(message))


def print_warning(message: str):
    """Print warning message"""
    print(get_formatter().warning(message))


def print_info(message: str):
    """Print info message"""
    print(get_formatter().info(message))


def print_section(title: str):
    """Print section header"""
    print(get_formatter().section_header(title))


def print_coordinates(coords: Coordinates):
    """Print LJPW coordinates"""
    print(get_formatter().coordinates_display(coords))


if __name__ == "__main__":
    # Demo output formatting
    fmt = OutputFormatter()

    print(fmt.section_header("CLI Output Formatting Demo"))

    print(fmt.subsection_header("Status Messages"))
    print(fmt.success("Connection established successfully"))
    print(fmt.error("Failed to reach target host"))
    print(fmt.warning("High latency detected"))
    print(fmt.info("Running diagnostics..."))

    print(fmt.subsection_header("Progress Bar"))
    print(fmt.progress_bar(75, 100, prefix="Scanning", suffix="packets"))

    print(fmt.subsection_header("LJPW Dimensions"))
    coords = Coordinates(love=0.85, justice=0.35, power=0.65, wisdom=0.90)
    print(fmt.coordinates_display(coords))

    print(fmt.subsection_header("Health Score"))
    print(fmt.health_score_display(0.75))

    print(fmt.subsection_header("Priority Indicators"))
    for priority in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        print(fmt.priority_indicator(priority))

    print(fmt.subsection_header("Lists"))
    print(fmt.bullet_list(["First item", "Second item", "Third item"]))

    print(fmt.subsection_header("Comparison"))
    print(fmt.comparison("Love", 0.85, 0.45))
    print(fmt.comparison("Justice", 0.35, 0.65))
    print(fmt.comparison("Power", 0.70, 0.72))
