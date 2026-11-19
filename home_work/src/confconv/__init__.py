"""confconv: translator of an educational configuration language to JSON."""
from .errors import ConfigError, ConfigSemanticError, ConfigSyntaxError
from .translator import to_json, translate

__version__ = "1.0.0"

__all__ = [
    "ConfigError",
    "ConfigSemanticError",
    "ConfigSyntaxError",
    "__version__",
    "to_json",
    "translate",
]