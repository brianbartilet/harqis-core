from typing import TypeVar, Type, Any, Optional, Generic, Dict
from enum import Enum

# Importing configuration loader and custom logger services
from core.config.loader import ConfigLoaderService
from pathlib import Path
from dataclasses import is_dataclass

TApp = TypeVar('TApp', bound=Enum)
"""
Type variable representing application names, bound to the Enum class to ensure only enumeration subclasses are used.
"""

TCfg = TypeVar('TCfg', bound=Any)
"""
Type variable for configuration objects, unrestricted in type to allow flexibility in configuration structure.
"""

TAppConfig = TypeVar('TAppConfig', bound=Any)
"""
Type variable for application configuration objects,
unrestricted in type to allow flexibility in configuration structure.
"""

class AppConfigManager:
    """
    Loads and retrieves application configuration sections.

    - `load(app_id, from_path=None)` loads config from service (or YAML path if provided),
      then keeps only sections whose inner dict has app_id==<app_id> OR application_name==<app_id>.
    - `get(loader_class, config_id)` returns a typed instance of the section (or raw dict).
    """

    def __init__(self, service: ConfigLoaderService):
        self.service = service
        # Holds the filtered, current app's sections: { "N8N": {...}, "HARQIS_GPT": {...}, ... }
        self._current_app_configs: Dict[str, Dict[str, Any]] = service.config

    def _normalize_source(self, source: Any) -> Dict[str, Dict[str, Any]]:
        """
        Ensure we have a dict[str, dict]. Your YAML should load into a mapping of sections.
        """
        if not isinstance(source, dict):
            raise TypeError("Root configuration must be a mapping (dict).")
        # Keep only dict-like sections
        return {k: v for k, v in source.items() if isinstance(v, dict)}

    def _filter_by_app_id(self, source: Dict[str, Dict[str, Any]], app_id: str) -> Dict[str, Dict[str, Any]]:
        """
        Keep sections whose inner dict declares app ownership via 'app_id' or 'application_name'.
        """
        filtered: Dict[str, Dict[str, Any]] = {}
        for section_key, section_val in source.items():
            section_app = section_val.get("app_id") or section_val.get("application_name")
            if section_app == app_id:
                filtered[section_key] = section_val
        return filtered

    def load(self, app_id: str, *, from_path: Optional[str | Path] = None) -> None:
        """
        Load and select configs for a given app.

        Args:
            app_id: The app identifier to match in sections (via 'app_id' OR 'application_name').
            from_path: Optional YAML file path to (re)load using the service;
                       if omitted, uses self.service.config as-is.
        """
        if from_path is not None:
            # If your ConfigLoaderService already has a method that loads YAML
            # into .config, call it here. Otherwise, adapt as needed.
            if hasattr(self.service, "load_yaml"):
                data = self.service.load_yaml(from_path)  # type: ignore[attr-defined]
                self.service.config = data  # keep it on the service for consistency
            else:
                raise AttributeError(
                    "ConfigLoaderService has no 'load_yaml' method; "
                    "either add it or pre-populate 'service.config' before calling load(...)."
                )

        source = self._normalize_source(self.service.config)
        filtered = self._filter_by_app_id(source, app_id)

        if not filtered:
            # Helpful error that also lists available declared app ids
            declared = []
            for sec, val in source.items():
                v = val.get("app_id") or val.get("application_name")
                if v:
                    declared.append(f"{sec} -> {v}")
            hint = f"Declared sections: {', '.join(declared)}" if declared else "No sections declared any app_id/application_name."
            raise KeyError(
                f"No configurations found for app_id '{app_id}'. "
                f"Ensure sections include 'app_id' or 'application_name' matching it. {hint}"
            )

        self._current_app_configs = filtered

    def get(self, config_id: str, loader_class: Type[TAppConfig] = dict) -> TAppConfig:
        """
        Retrieve a section by its key (e.g., 'N8N', 'HARQIS_GPT').

        If loader_class is `dict`, returns the raw dict.
        If it's a dataclass or a **kwargs-constructible class (e.g., Pydantic), returns an instance.
        """
        if config_id not in self._current_app_configs:
            available = ", ".join(self._current_app_configs.keys()) or "(none loaded)"
            raise KeyError(f"Config section '{config_id}' not found. Available: {available}")

        raw = self._current_app_configs[config_id]

        if loader_class is dict:  # type: ignore[comparison-overlap]
            return raw  # type: ignore[return-value]

        if is_dataclass(loader_class):
            return loader_class(**raw)  # type: ignore[misc]

        try:
            return loader_class(**raw)  # type: ignore[misc]
        except TypeError as e:
            raise TypeError(
                f"Failed to construct {loader_class.__name__} from section '{config_id}'. "
                f"Check field names and types. Error: {e}"
            )
