"""Color module for managing level color channels.

This module provides the ColorChannel class for defining custom colors in levels,
and utility functions for working with colors.
"""

from typing import Self

from .keys.color_channels import *
from .keys.colors import *


class ColorChannel:
    """Represents a color channel in a Geometry Dash level.

    Color channels define custom colors that can be referenced by objects in the level.
    Each channel has an ID and RGB values, plus additional properties.

    Attributes:
        properties: Dictionary of color channel properties.

    Example:
        >>> channel = ColorChannel(1)
        >>> channel.set_rgb(255, 0, 0).set_opacity(0.8)
        >>> level.add_color_channel(channel)
    """

    def __init__(self, id: int) -> None:
        """Initialize a new color channel.

        Args:
            id: The color channel ID. Use constants from gmd_api.keys.color_channels
                for standard channels (CHANNEL_BG, CHANNEL_G1, etc.).
        """
        self.properties: dict[int, any] = {}

        self.set(ID, id)
        self.set(RED, 0)
        self.set(GREEN, 0)
        self.set(BLUE, 0)

        # unknown for now
        self.set(11, 255)
        self.set(12, 255)
        self.set(13, 255)

        self.set(4, -1)

        self.set(7, 1)
        self.set(8, 1)
        self.set(15, 1)
        self.set(18, 1)
    
    def set(self, key: int, value: any) -> Self:
        """Set a color channel property.

        Args:
            key: The property key (see gmd_api.keys.colors for constants).
            value: The value to set.

        Returns:
            Self: Returns self for method chaining.
        """
        self.properties[key] = value
        return self

    def set_rgb(self, r: int, g: int, b: int) -> Self:
        """Set the RGB color values.

        Args:
            r: Red component (0-255).
            g: Green component (0-255).
            b: Blue component (0-255).

        Returns:
            Self: Returns self for method chaining.
        """
        return self.set(RED, r) \
            .set(GREEN, g) \
            .set(BLUE, b)
    
    def set_opacity(self, opacity: float) -> Self:
        """Set the opacity/alpha value.

        Args:
            opacity: Opacity value (0.0 = fully transparent, 1.0 = fully opaque).

        Returns:
            Self: Returns self for method chaining.
        """
        return self.set(OPACITY, opacity)
    
    def set_rgba(self, r: int, g: int, b: int, a: float) -> Self:
        """Set the RGBA color values.

        Args:
            r: Red component (0-255).
            g: Green component (0-255).
            b: Blue component (0-255).
            a: Alpha/opacity (0.0 = fully transparent, 1.0 = fully opaque).

        Returns:
            Self: Returns self for method chaining.
        """
        return self.set_rgb(r, g, b).set_opacity(a)
    
    def to_string(self) -> str:
        """Convert the color channel to its string representation.

        Returns:
            str: The color channel data as an underscore-separated string.
        """
        return "_".join([f"{k}_{v}" for k, v in self.properties.items()]) + "|"


def get_default_colors() -> list[ColorChannel]:
    """Get the default color channels for a new level.

    Returns:
        list[ColorChannel]: A list of default color channels including background,
            ground, player colors, etc.
    """
    return [
        ColorChannel(CHANNEL_BG).set_rgb(255, 255, 255),
        ColorChannel(CHANNEL_G1).set_rgb(0, 0, 0),
        ColorChannel(CHANNEL_G2).set_rgb(0, 0, 0),
        ColorChannel(CHANNEL_MG1).set_rgb(0, 0, 0),
        ColorChannel(CHANNEL_MG2).set_rgb(0, 0, 0),
        ColorChannel(CHANNEL_OBJ).set_rgb(200, 200, 200),

        ColorChannel(CHANNEL_P1).set_rgb(255, 255, 255),
        ColorChannel(CHANNEL_P2).set_rgb(255, 255, 255),
    ]


def make_hsv_string(h: int, s: float, v: float) -> str:
    """Create an HSV color string in the GMD format.

    Args:
        h: Hue value (-180 to 180).
        s: Saturation value (0.0 to 1.0).
        v: Value/brightness (0.0 to 1.0).

    Returns:
        str: The HSV string in GMD format.
    """
    return f"{h}a{s}a{v}a0a0"