"""Level string module for managing inner level data.

This module provides the InnerLevelString class which represents the encoded
and compressed level data containing objects, color channels, and settings.
"""

import gzip
from base64 import urlsafe_b64encode
from typing import Self

from .color import ColorChannel, get_default_colors
from .keys.inner_level_string import *
from .level_object import LevelObject


class InnerLevelString:
    """Represents the inner level data of a Geometry Dash level.

    This contains the actual level content: objects, color channels, and various
    settings like game mode, speed, background, etc. The data is compressed and
    encoded before being embedded in the level file.

    Attributes:
        objects: List of LevelObject instances in the level.
        color_channels: List of ColorChannel instances defining colors.
        properties: Dictionary of level settings.

    Example:
        >>> inner = InnerLevelString()
        >>> inner.set_platformer(True)
        >>> inner.set_background_id(12)
    """

    def __init__(self) -> None:
        """Initialize a new inner level string with default values."""
        self.objects: list[LevelObject] = []
        self.color_channels: list[ColorChannel] = get_default_colors()
        self.properties: dict[str, any] = {}
    
    def set(self, key: str, value: any) -> Self:
        """Set a property value.

        Args:
            key: The property key (see gmd_api.keys.inner_level_string for constants).
            value: The value to set.

        Returns:
            Self: Returns self for method chaining.
        """
        self.properties[key] = value
        return self
    
    def set_platformer(self, to: bool = True) -> Self:
        """Set whether the level is in platformer mode.

        Args:
            to: True for platformer mode, False for classic mode. Defaults to True.

        Returns:
            Self: Returns self for method chaining.
        """
        return self.set(IS_PLATFORMER, to)
    
    def set_background_id(self, id: int) -> Self:
        """Set the background ID.

        Args:
            id: The background ID number.

        Returns:
            Self: Returns self for method chaining.
        """
        return self.set(BG_ID, id)
    
    def set_ground_id(self, id: int) -> Self:
        """Set the ground ID.

        Args:
            id: The ground ID number.

        Returns:
            Self: Returns self for method chaining.
        """
        return self.set(GROUND_ID, id)
    
    def set_middleground_id(self, id: int) -> Self:
        """Set the middleground ID.

        Args:
            id: The middleground ID number.

        Returns:
            Self: Returns self for method chaining.
        """
        return self.set(MG_ID, id)

    def to_raw_string(self) -> str:
        """Convert the inner level string to its uncompressed string representation.

        Returns:
            str: The raw level string before compression and encoding.
        """
        colors: str = "".join([channel.to_string() for channel in self.color_channels])
        keys: str = ",".join([f"{k},{v}" for k, v in self.properties.items()])
        prelude: str = f"kS38,{colors},{keys};"
        objects: str = "".join([obj.to_string() for obj in self.objects])

        return f"{prelude}{objects}"
    
    def to_string(self) -> str:
        """Convert the inner level string to its compressed and encoded form.

        Returns:
            str: The level string gzip-compressed and base64-encoded.
        """
        raw_level_string = bytes(self.to_raw_string(), encoding="utf-8")
        return urlsafe_b64encode(gzip.compress(raw_level_string)).decode("utf-8")