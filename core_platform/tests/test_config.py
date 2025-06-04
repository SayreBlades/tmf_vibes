import os
import tempfile
import pytest
from pathlib import Path
from pydantic import ValidationError
from core_platform.config import AppConfig

def test_config_loading():
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        
        with open(config_path, 'w') as f:
            f.write("""
auth:
  credentials:
    - username: user1
      password: pass1
    - username: user2
      password: pass2

legacy_systems:
  product_catalog:
    base_url: http://test:8000
            """)
            
        config = AppConfig(config_path=str(config_path))
        
        assert len(config.auth['credentials']) == 2
        assert config.auth['credentials'][0].username == 'user1'
        assert config.auth['credentials'][0].password == 'pass1'
        assert config.legacy_systems['product_catalog'].base_url == 'http://test:8000'
        
def test_config_env_vars(monkeypatch):
    monkeypatch.setenv('CONFIG_PATH', '/dev/null')  # Disable file loading
    monkeypatch.setenv('CORE_AUTH', 
                      '{"credentials": [{"username": "env_user", "password": "env_pass"}]}')
    monkeypatch.setenv('CORE_LEGACY_SYSTEMS', 
                      '{"product_catalog": {"base_url": "http://env:9000"}}')
                      
    config = AppConfig()  # Should use env vars
    
    assert len(config.auth['credentials']) == 1
    assert config.auth['credentials'][0].username == 'env_user'
    assert config.auth['credentials'][0].password == 'env_pass'
    assert config.legacy_systems['product_catalog'].base_url == 'http://env:9000'
        
def test_missing_config():
    with pytest.raises(ValidationError):
        AppConfig(config_path='non_existent_path.yaml')
        
def test_invalid_config():
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        
        with open(config_path, 'w') as f:
            f.write("invalid: \n  - yaml: [")
            
        with pytest.raises(ValueError) as excinfo:
            config = AppConfig(config_path=str(config_path))
        assert "Error parsing config file" in str(excinfo.value)

def test_minimal_config():
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        
        with open(config_path, 'w') as f:
            f.write("auth: {}")
            
        with pytest.raises(ValidationError):
            AppConfig(config_path=str(config_path))
