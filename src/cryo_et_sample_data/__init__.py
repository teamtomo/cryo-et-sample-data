try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"
from ._hiv import hiv
from ._sample_data import make_sample_data

__all__ = ("make_sample_data", "hiv")
