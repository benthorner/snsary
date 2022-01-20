"""
A function accepts a single :mod:`Reading <snsary.models.reading>` as an argument and can either return a :mod:`Reading <snsary.models.reading>` or ``None``. This module contains classes whose instances are callable and act as functions.
"""

from .filter import Filter
from .window import Window
from .window_average import WindowAverage

__all__ = [
    "Filter",
    "Window",
    "WindowAverage"
]
