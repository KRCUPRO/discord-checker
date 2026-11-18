# src/config.py
import os
import re
from pathlib import Path
from typing import Any, Dict, Optional
import yaml

from src.utils.paths import resolve_resource

DEFAULT_CONFIG_PATH = Path("config.yaml")
EXAMPLE_CONFIG_PATH = Path("config/config.example.yaml")

def _replace_env_vars(match):
    var_name = match.group(1)
    return os.environ.get(var_name, "")

def _resolve_env_in_str(value: str) -> str:
    # Match ${VAR_NAME} pattern
    return re.sub(r"\$\{([A-Z0-9_]+)\}", _replace_env_vars, value)

def _deep_resolve(node: Any) -> Any:
    if isinstance(node, dict):
        return {k: _deep_resolve(v) for k, v in node.items()}
    elif isinstance(node, list):
        return [_deep_resolve(item) for item in node]
    elif isinstance(node, str):
        return _resolve_env_in_str(node)
    return node

class AppConfig:
    def __init__(self, data: Dict[str, Any]):
        self.raw = data
        self.target = data.get("target", {})
        self.network = data.get("network", {})
        self.proxy = data.get("proxy", {})
        self.webhook = data.get("webhook", {})
        self.storage = data.get("storage", {})
        self.ui = data.get("ui", {})

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "AppConfig":
        if config_path is None or config_path == DEFAULT_CONFIG_PATH or str(config_path) == "config.yaml":
            resolved_path = resolve_resource("config.yaml")
            if not resolved_path.exists():
                resolved_path = resolve_resource("config/config.example.yaml")
        else:
            resolved_path = Path(config_path) if not isinstance(config_path, Path) else config_path

        if not resolved_path.exists():
            raw_data = {}
        else:
            with open(resolved_path, "r", encoding="utf-8") as f:
                raw_data = yaml.safe_load(f) or {}

        resolved = _deep_resolve(raw_data)
        return cls(resolved)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target": self.target,
            "network": self.network,
            "proxy": self.proxy,
            "webhook": self.webhook,
            "storage": self.storage,
            "ui": self.ui
        }

    def save(self, config_path: Optional[Path] = None):
        if config_path is None:
            config_path = resolve_resource("config.yaml")
        try:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, "w", encoding="utf-8") as f:
                yaml.dump(self.to_dict(), f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        except Exception:
            pass
