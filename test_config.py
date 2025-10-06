"""
Unit tests for config.py module.
Run with: python -m pytest test_config.py -v
"""
import pytest
import json
from pathlib import Path
from config import Config


class TestConfig:
    """Test cases for Config class."""

    @pytest.fixture
    def temp_config_file(self, tmp_path):
        """Create a temporary config file path."""
        return tmp_path / "test_settings.json"

    @pytest.fixture
    def config(self, temp_config_file):
        """Create a Config instance with temporary file."""
        return Config(str(temp_config_file))

    def test_default_config_values(self, config):
        """Test that default values are loaded correctly."""
        assert config.get('num_days') == 3
        assert config.get('num_workshops') == 12
        assert config.get('max_participants_per_workshop') is None
        assert config.get('keep_classes_together') == 'egal'
        assert config.get('language') == 'de'
        assert config.get('theme') == 'cosmo'

    def test_default_wish_weights(self, config):
        """Test that wish weights have correct defaults."""
        weights = config.get('wish_weights')
        assert weights['wunsch1'] == 10
        assert weights['wunsch2'] == 5
        assert weights['wunsch3'] == 2
        assert weights['wunsch4'] == 1

    def test_get_nonexistent_key(self, config):
        """Test getting a key that doesn't exist."""
        assert config.get('nonexistent_key') is None
        assert config.get('nonexistent_key', 'default_value') == 'default_value'

    def test_set_and_get(self, config):
        """Test setting and getting values."""
        config.set('num_days', 5)
        assert config.get('num_days') == 5

        config.set('custom_key', 'custom_value')
        assert config.get('custom_key') == 'custom_value'

    def test_save_and_load(self, temp_config_file):
        """Test that configuration persists across instances."""
        # Create config and set values
        config1 = Config(str(temp_config_file))
        config1.set('num_days', 7)
        config1.set('num_workshops', 20)
        config1.save()

        # Load in new instance
        config2 = Config(str(temp_config_file))
        assert config2.get('num_days') == 7
        assert config2.get('num_workshops') == 20
        # Defaults should still be there
        assert config2.get('keep_classes_together') == 'egal'

    def test_reset_to_defaults(self, config):
        """Test resetting configuration to defaults."""
        config.set('num_days', 10)
        config.set('custom_key', 'value')
        config.reset_to_defaults()

        assert config.get('num_days') == 3
        assert config.get('custom_key') is None

    def test_save_with_special_characters(self, temp_config_file):
        """Test saving configuration with German characters."""
        config = Config(str(temp_config_file))
        config.set('test_string', 'Töpfern & Nähen')
        config.save()

        config2 = Config(str(temp_config_file))
        assert config2.get('test_string') == 'Töpfern & Nähen'

    def test_load_corrupted_config(self, temp_config_file):
        """Test loading a corrupted config file falls back to defaults."""
        # Write invalid JSON
        temp_config_file.write_text("{ invalid json }")

        config = Config(str(temp_config_file))
        assert config.get('num_days') == 3  # Should load defaults

    def test_load_nonexistent_file(self, temp_config_file):
        """Test loading config when file doesn't exist."""
        config = Config(str(temp_config_file))
        assert config.get('num_days') == 3  # Should load defaults
        assert not temp_config_file.exists()

    def test_config_file_created_on_save(self, temp_config_file):
        """Test that config file is created when saving."""
        config = Config(str(temp_config_file))
        assert not temp_config_file.exists()

        config.save()
        assert temp_config_file.exists()

    def test_merge_with_defaults(self, temp_config_file):
        """Test that loading merges with defaults (for backward compatibility)."""
        # Create config with only some keys
        partial_config = {'num_days': 5, 'theme': 'darkly'}
        temp_config_file.write_text(json.dumps(partial_config))

        config = Config(str(temp_config_file))
        assert config.get('num_days') == 5  # From file
        assert config.get('theme') == 'darkly'  # From file
        assert config.get('num_workshops') == 12  # From defaults

    def test_wish_weights_modification(self, config):
        """Test modifying wish weights."""
        weights = config.get('wish_weights')
        weights['wunsch1'] = 20
        config.set('wish_weights', weights)

        assert config.get('wish_weights')['wunsch1'] == 20
        assert config.get('wish_weights')['wunsch2'] == 5

    def test_config_immutable_defaults(self):
        """Test that modifying one config doesn't affect defaults."""
        config1 = Config('config1.json')
        config2 = Config('config2.json')

        config1.set('num_days', 99)
        assert config2.get('num_days') == 3

        # Cleanup
        Path('config1.json').unlink(missing_ok=True)
        Path('config2.json').unlink(missing_ok=True)
