from typing import TypeVar, Type, Any, Optional, Generic, Dict
from enum import Enum
from dataclasses import dataclass, field

# Importing configuration loader and custom logger services
from core.config.loader import ConfigLoaderService
from core.utilities.logging.custom_logger import create_logger
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


@dataclass
class BaseAppConfigModel:
    """
    Base model for storing generic application configuration details.

    Attributes:
        parameters (Optional[dict]): Optional dictionary containing application-specific parameters.
        app_data (Optional[dict]): Optional dictionary for storing application context information, such as API keys.
        app_id (Optional[str]): Unique identifier for the application instance.
        id (Optional[str]): Configuration identifier, potentially used for versioning or referencing configurations.
    """
    parameters: Dict[str, Any] = field(default_factory=dict)
    app_data: Dict[str, Any] = field(default_factory=dict)
    app_id: Optional[str] = None
    id: Optional[str] = None


class AppConfig(Generic[TCfg]):
    """
    Generic class for handling application configurations using dynamic type instantiation.

    This class is designed to load and manage application configurations using a specified configuration class.

    Attributes:
        log (Logger): Logger instance for error and operation logging.
        app_config (dict): Dictionary holding the loaded configuration specific to the application.
        _config (TCfg): Instance of the configuration class loaded with the application configuration.
    """

    def __init__(self, app: TApp, type_hook_config: Type[TCfg], **kwargs):
        """
        Initialize an AppConfig instance by loading the appropriate configuration based on application enum and type.

        Args:
            app (TApp): The Enum representing the application for which configuration is loaded.
            type_hook_config (Type[TCfg]): The class type used for instantiation of the configuration object.
            **kwargs: Additional keyword arguments such as:
                      'logger' (Logger): Optional; custom logger for logging.
                      'base_path' (str): Optional; custom base path for configuration files.
        """
        self.log = kwargs.get('logger', create_logger(self.__class__.__name__))
        self.kwargs = kwargs

        try:
            self.app_config = ConfigLoaderService(**kwargs).config[app.value]
            self._config = type_hook_config(**self.app_config)  # Instantiate configuration class with loaded settings
        except KeyError as e:
            self.log.error(f"Cannot find application key for {app}: {str(e)}")
            raise

    @property
    def config(self) -> TCfg:
        """
        Retrieve the loaded configuration object instance.

        Returns:
            TCfg: The configuration instance loaded from the application-specific configuration.
        """
        return self._config


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
        self._current_app_configs: Dict[str, Dict[str, Any]] = {}

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

    def get(self, loader_class: Type[TAppConfig], config_id: str) -> TAppConfig:
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
