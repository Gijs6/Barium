from .cli import build, serve
from importlib.metadata import version

__version__ = version("BariumSSG")
__all__ = ["build", "serve"]
