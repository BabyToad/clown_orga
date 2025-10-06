"""
Configuration management for the Workshop Allocation Tool.
Handles persistent settings and provides defaults.
"""
import json
from pathlib import Path
from typing import Dict, Any


class Config:
    """Manages application configuration with persistent storage."""

    DEFAULT_CONFIG = {
        "num_days": 3,
        "num_workshops": 12,
        "max_participants_per_workshop": None,  # None = unlimited
        "keep_classes_together": "egal",  # "ja" / "nein" / "egal"
        "wish_weights": {
            "wunsch1": 10,
            "wunsch2": 5,
            "wunsch3": 2,
            "wunsch4": 1
        },
        "language": "de",
        "theme": "cosmo",  # ttkbootstrap theme
        "last_import_path": "",
        "last_export_path": ""
    }

    def __init__(self, config_file: str = "settings.json"):
        self.config_file = Path(config_file)
        self.settings = self.load()

    def load(self) -> Dict[str, Any]:
        """Load configuration from file, or return defaults."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return {**self.DEFAULT_CONFIG, **loaded}
            except (json.JSONDecodeError, IOError):
                return self.DEFAULT_CONFIG.copy()
        return self.DEFAULT_CONFIG.copy()

    def save(self):
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Could not save configuration: {e}")

    def get(self, key: str, default=None):
        """Get configuration value."""
        return self.settings.get(key, default)

    def set(self, key: str, value: Any):
        """Set configuration value."""
        self.settings[key] = value

    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self.settings = self.DEFAULT_CONFIG.copy()
