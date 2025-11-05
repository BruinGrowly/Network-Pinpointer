#!/usr/bin/env python3
"""
Configuration System - YAML/JSON config file support

Supports configuration via:
- Default settings
- User config file (~/.network-pinpointer/config.yaml)
- Project config file (./network-pinpointer.yaml)
- Environment variables
- Command-line arguments (highest priority)
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict, field


@dataclass
class NetworkTarget:
    """Configuration for a monitored network target"""
    name: str
    host: str
    ports: List[int] = field(default_factory=lambda: [80, 443])
    baseline: Optional[Dict[str, float]] = None
    alert_threshold: float = 0.15
    critical: bool = False


@dataclass
class ThresholdConfig:
    """Health threshold configuration"""
    critical: Dict[str, float] = field(default_factory=lambda: {"love": 0.3, "power": 0.3})
    warning: Dict[str, float] = field(default_factory=lambda: {"love": 0.5, "power": 0.5})


@dataclass
class OutputConfig:
    """Output formatting configuration"""
    format: str = "rich"  # rich, plain, json
    colors: bool = True
    emoji: bool = True
    verbosity: str = "normal"  # quiet, normal, verbose, debug


@dataclass
class MonitoringConfig:
    """Monitoring and alerting configuration"""
    enabled: bool = False
    interval: int = 300  # seconds
    targets: List[str] = field(default_factory=list)
    alert_methods: List[str] = field(default_factory=list)  # slack, email, webhook


@dataclass
class NetworkPinpointerConfig:
    """Complete configuration for Network Pinpointer"""

    # Network settings
    network_type: str = "enterprise"  # enterprise, datacenter, high-security, development
    baseline_auto_learn: bool = True
    monitoring_interval: int = 300  # seconds

    # Targets
    targets: Dict[str, NetworkTarget] = field(default_factory=dict)

    # Thresholds
    thresholds: ThresholdConfig = field(default_factory=ThresholdConfig)

    # Output
    output: OutputConfig = field(default_factory=OutputConfig)

    # Monitoring
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)

    # Export settings
    export_dir: str = "./network_reports"
    auto_export: bool = False

    # Alert settings
    alert_slack_webhook: Optional[str] = None
    alert_email: Optional[str] = None
    alert_webhook: Optional[str] = None


class ConfigManager:
    """Manages configuration loading and merging"""

    DEFAULT_CONFIG_LOCATIONS = [
        Path.home() / ".network-pinpointer" / "config.yaml",
        Path.home() / ".network-pinpointer" / "config.json",
        Path("./network-pinpointer.yaml"),
        Path("./network-pinpointer.json"),
        Path("./.network-pinpointer.yaml"),
        Path("./.network-pinpointer.json"),
    ]

    def __init__(self, config_file: Optional[str] = None):
        self.config_file = Path(config_file) if config_file else None
        self.config = self.load_config()

    def load_config(self) -> NetworkPinpointerConfig:
        """Load configuration from files and environment"""

        # Start with defaults
        config_dict = {}

        # Try to load from file
        loaded_file = None

        if self.config_file and self.config_file.exists():
            # Explicit config file provided
            config_dict = self._load_file(self.config_file)
            loaded_file = self.config_file
        else:
            # Try default locations
            for location in self.DEFAULT_CONFIG_LOCATIONS:
                if location.exists():
                    config_dict = self._load_file(location)
                    loaded_file = location
                    break

        # Apply environment variable overrides
        config_dict = self._apply_env_overrides(config_dict)

        # Create config object
        config = self._dict_to_config(config_dict)

        if loaded_file:
            print(f"✓ Loaded configuration from: {loaded_file}")

        return config

    def _load_file(self, path: Path) -> Dict[str, Any]:
        """Load config from YAML or JSON file"""
        try:
            with open(path, 'r') as f:
                if path.suffix in ['.yaml', '.yml']:
                    return yaml.safe_load(f) or {}
                elif path.suffix == '.json':
                    return json.load(f)
                else:
                    raise ValueError(f"Unsupported config format: {path.suffix}")
        except Exception as e:
            print(f"Warning: Failed to load config from {path}: {e}")
            return {}

    def _apply_env_overrides(self, config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Apply environment variable overrides"""

        # Network Pinpointer environment variables
        env_mappings = {
            'NETPIN_NETWORK_TYPE': ['network_type'],
            'NETPIN_MONITORING_INTERVAL': ['monitoring_interval'],
            'NETPIN_OUTPUT_FORMAT': ['output', 'format'],
            'NETPIN_COLORS': ['output', 'colors'],
            'NETPIN_VERBOSITY': ['output', 'verbosity'],
            'NETPIN_ALERT_SLACK': ['alert_slack_webhook'],
            'NETPIN_ALERT_EMAIL': ['alert_email'],
        }

        for env_var, keys in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                # Navigate nested dict
                current = config_dict
                for key in keys[:-1]:
                    if key not in current:
                        current[key] = {}
                    current = current[key]

                # Convert types
                final_key = keys[-1]
                if final_key in ['monitoring_interval']:
                    value = int(value)
                elif final_key == 'colors':
                    value = value.lower() in ['true', '1', 'yes']

                current[final_key] = value

        return config_dict

    def _dict_to_config(self, config_dict: Dict[str, Any]) -> NetworkPinpointerConfig:
        """Convert dictionary to config object"""

        # Handle nested structures
        if 'targets' in config_dict:
            targets = {}
            for name, target_data in config_dict['targets'].items():
                targets[name] = NetworkTarget(name=name, **target_data)
            config_dict['targets'] = targets

        if 'thresholds' in config_dict:
            config_dict['thresholds'] = ThresholdConfig(**config_dict['thresholds'])

        if 'output' in config_dict:
            config_dict['output'] = OutputConfig(**config_dict['output'])

        if 'monitoring' in config_dict:
            config_dict['monitoring'] = MonitoringConfig(**config_dict['monitoring'])

        return NetworkPinpointerConfig(**config_dict)

    def save_config(self, path: Optional[Path] = None, format: str = 'yaml'):
        """Save current configuration to file"""

        if path is None:
            path = Path.home() / ".network-pinpointer" / f"config.{format}"

        # Create directory if needed
        path.parent.mkdir(parents=True, exist_ok=True)

        # Convert to dict
        config_dict = asdict(self.config)

        # Write file
        with open(path, 'w') as f:
            if format == 'yaml':
                yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)
            elif format == 'json':
                json.dump(config_dict, f, indent=2)

        print(f"✓ Configuration saved to: {path}")

    def create_example_config(self, path: Path):
        """Create an example configuration file"""

        example = {
            'network_type': 'enterprise',
            'baseline_auto_learn': True,
            'monitoring_interval': 300,

            'targets': {
                'production_api': {
                    'name': 'Production API',
                    'host': 'api.prod.example.com',
                    'ports': [443, 8080],
                    'baseline': {'love': 0.90, 'justice': 0.30, 'power': 0.85, 'wisdom': 0.90},
                    'alert_threshold': 0.15,
                    'critical': True
                },
                'database': {
                    'name': 'Main Database',
                    'host': 'db.prod.example.com',
                    'ports': [5432],
                    'baseline': {'love': 0.95, 'justice': 0.25, 'power': 0.90, 'wisdom': 0.85},
                    'alert_threshold': 0.10,
                    'critical': True
                },
                'external_service': {
                    'name': 'AWS S3',
                    'host': 's3.amazonaws.com',
                    'ports': [443],
                    'baseline': None,  # Will auto-learn
                    'alert_threshold': 0.20,
                    'critical': False
                }
            },

            'thresholds': {
                'critical': {'love': 0.3, 'power': 0.3},
                'warning': {'love': 0.5, 'power': 0.5}
            },

            'output': {
                'format': 'rich',  # rich, plain, json
                'colors': True,
                'emoji': True,
                'verbosity': 'normal'  # quiet, normal, verbose, debug
            },

            'monitoring': {
                'enabled': False,
                'interval': 300,
                'targets': ['production_api', 'database'],
                'alert_methods': ['slack', 'email']
            },

            'export_dir': './network_reports',
            'auto_export': False,

            'alert_slack_webhook': 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL',
            'alert_email': 'oncall@example.com',
            'alert_webhook': None
        }

        # Create directory
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write example
        with open(path, 'w') as f:
            if path.suffix in ['.yaml', '.yml']:
                yaml.dump(example, f, default_flow_style=False, sort_keys=False)
            elif path.suffix == '.json':
                json.dump(example, f, indent=2)

        print(f"✓ Example configuration created at: {path}")
        print(f"\nEdit this file to customize your settings.")
        print(f"Then run: pinpoint --config {path}")


# Global config instance
_config: Optional[ConfigManager] = None


def get_config(config_file: Optional[str] = None) -> NetworkPinpointerConfig:
    """Get or create global config instance"""
    global _config
    if _config is None or config_file:
        _config = ConfigManager(config_file)
    return _config.config


def reload_config(config_file: Optional[str] = None):
    """Reload configuration"""
    global _config
    _config = ConfigManager(config_file)
    return _config.config


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "create-example":
        manager = ConfigManager()
        output_path = Path.home() / ".network-pinpointer" / "config.yaml"
        manager.create_example_config(output_path)
    else:
        # Demo: Load and display config
        manager = ConfigManager()
        config = manager.config

        print("\n Current Configuration:")
        print("=" * 70)
        print(f"Network Type: {config.network_type}")
        print(f"Monitoring Interval: {config.monitoring_interval}s")
        print(f"Output Format: {config.output.format}")
        print(f"Colors: {config.output.colors}")
        print(f"Targets Configured: {len(config.targets)}")

        if config.targets:
            print("\nConfigured Targets:")
            for name, target in config.targets.items():
                print(f"  • {target.name} ({target.host})")
