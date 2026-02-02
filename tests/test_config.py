import pytest
from pathlib import Path
from src.config.settings import Config, CONFIG


def test_config_defaults():
    """Test default config values."""
    config = Config()
    assert config.model == "mistral"
    assert config.temperature == 0.0
    assert config.max_tokens == 200
    assert config.max_retries == 2


def test_config_paths():
    """Test config paths."""
    config = Config()
    assert isinstance(config.data_dir, Path)
    assert isinstance(config.db_path, Path)


def test_config_ollama_url():
    """Test Ollama URL format."""
    assert CONFIG.ollama_url.startswith("http")
    assert "11434" in CONFIG.ollama_url
