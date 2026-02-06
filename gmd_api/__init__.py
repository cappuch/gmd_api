"""gmd_api - A Python API for creating Geometry Dash levels.

This package provides a simple, Pythonic interface for creating and manipulating
Geometry Dash level files in the GMD format used by GDShare.

Main classes:
    - Level: Represents a complete level with metadata and objects
    - LevelObject: Represents a single object in a level
    - ColorChannel: Represents a color channel definition
    - InnerLevelString: Represents the inner level data (objects, colors, settings)

Example:
    >>> from gmd_api import Level, LevelObject, ColorChannel
    >>> level = Level(name="My Level")
    >>> obj = LevelObject(211).move_to(100, 100)
    >>> level.add_object(obj)
    >>> level.save("my_level.gmd")
"""

from .color import ColorChannel
from .level import Level
from .level_object import LevelObject
from .level_string import InnerLevelString

__version__ = "0.1.2"
__all__ = ["Level", "LevelObject", "ColorChannel", "InnerLevelString"]
