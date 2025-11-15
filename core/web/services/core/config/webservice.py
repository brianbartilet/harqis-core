from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from core.config.app_config import BaseAppConfigModel


@dataclass
class AppConfigWSClient(BaseAppConfigModel):
    """
    Base configuration object for web services.
    Tracks which attributes were changed.
    """

    client: Optional[str] = None
    parameters: Dict[str, Optional[Any]] = field(default_factory=lambda: {
        "base_url": None,
        "response_encoding": None,
        "verify": None,
        "timeout": None,
        "stream": False,
        "logging": None,
    })
    headers: Optional[Dict[str, str]] = None
    return_data_only: bool = False

    # internal field to track updated attributes
    changed: set = field(default_factory=set, init=False, repr=False)

    def __setattr__(self, key, value):
        # let the dataclass initialize without tracking initial assignments
        if "_initialized" in self.__dict__:
            # track changes only for real fields
            if key in self.__dataclass_fields__ and key != "changed":
                self.changed.add(key)

        super().__setattr__(key, value)

    def __post_init__(self):
        # mark class as initialized so further __setattr__ calls are tracked
        self._initialized = True
