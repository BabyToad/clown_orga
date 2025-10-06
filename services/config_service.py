"""Configuration service - manages application settings."""
from typing import Any, Dict
from services.config import Config


class ConfigService:
    """Service for managing configuration - wraps Config."""

    def __init__(self, config_file: str = 'config.json'):
        self.config = Config(config_file)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Set a configuration value."""
        self.config.set(key, value)

    def save(self):
        """Save configuration to file."""
        self.config.save()

    def get_all(self) -> Dict:
        """Get all configuration settings."""
        return self.config.settings.copy()

    def update_parameters(self, params: Dict):
        """Update multiple parameters at once."""
        for key, value in params.items():
            self.config.set(key, value)
        self.save()

    def reset_to_defaults(self):
        """Reset configuration to default values."""
        self.config.settings = self.config.DEFAULT_CONFIG.copy()
        self.save()

    def get_optimization_params(self) -> Dict:
        """Get parameters needed for optimization."""
        return {
            'num_days': self.get('num_days', 3),
            'num_workshops': self.get('num_workshops', 12),
            'max_participants_per_workshop': self.get('max_participants_per_workshop'),
            'keep_classes_together': self.get('keep_classes_together', 'egal'),
            'wish_weights': self.get('wish_weights', {
                'wunsch1': 10,
                'wunsch2': 5,
                'wunsch3': 2,
                'wunsch4': 1
            })
        }
