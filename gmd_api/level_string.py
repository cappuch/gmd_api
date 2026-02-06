"""Level string module for managing inner level data.

This module provides the InnerLevelString class which represents the encoded
and compressed level data containing objects, color channels, and settings.
"""

import gzip
from base64 import urlsafe_b64decode, urlsafe_b64encode
from typing import Any, Self

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
        self.properties: dict[str, Any] = {}

    def set(self, key: str, value: Any) -> Self:
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

    @classmethod
    def from_string(cls, encoded_string: str) -> Self:
        """Parse an inner level string from its compressed and encoded form.

        Args:
            encoded_string: The base64-encoded and gzip-compressed level string.

        Returns:
            InnerLevelString: A new InnerLevelString instance with parsed data.
        """
        # Decode and decompress
        try:
            compressed_data = urlsafe_b64decode(encoded_string)
            raw_string = gzip.decompress(compressed_data).decode("utf-8")
        except Exception as e:
            raise ValueError(f"Failed to decode/decompress inner level string: {e}")

        inner = cls()
        inner.objects.clear()
        inner.color_channels.clear()
        inner.properties.clear()

        # Parse the raw string
        # Format: kS38,{color_channels},{properties};{objects}
        parts = raw_string.split(";", 1)
        if len(parts) < 1:
            return inner

        prelude = parts[0]
        objects_str = parts[1] if len(parts) > 1 else ""

        # Parse prelude (colors and properties)
        if prelude.startswith("kS38,"):
            prelude_data = prelude[5:]  # Remove "kS38,"

            # Split by pipe to separate color channels
            tokens = prelude_data.split("|")

            # Parse color channels (all tokens before the properties)
            for token in tokens:
                if not token:
                    continue

                # Check if this is a color channel (starts with channel ID)
                if "_" in token:
                    try:
                        channel = parse_color_channel(token)
                        if channel:
                            inner.color_channels.append(channel)
                    except Exception:
                        # If parsing fails, it might be properties
                        pass

            # Parse properties from the last part
            # Properties come after all color channels
            if "," in prelude_data:
                # Find the last section after all pipes
                last_section = prelude_data.split("|")[-1]
                if "," in last_section and "_" not in last_section:
                    # This is the properties section
                    prop_pairs = last_section.split(",")
                    for i in range(0, len(prop_pairs) - 1, 2):
                        if i + 1 < len(prop_pairs):
                            key = prop_pairs[i]
                            value = prop_pairs[i + 1]
                            # Try to convert value to appropriate type
                            if value.lower() == "true":
                                inner.properties[key] = True
                            elif value.lower() == "false":
                                inner.properties[key] = False
                            else:
                                try:
                                    inner.properties[key] = int(value)
                                except ValueError:
                                    try:
                                        inner.properties[key] = float(value)
                                    except ValueError:
                                        inner.properties[key] = value

        # Parse objects
        if objects_str:
            object_strings = objects_str.split(";")
            for obj_str in object_strings:
                if obj_str.strip():
                    try:
                        obj = parse_object(obj_str)
                        if obj:
                            inner.objects.append(obj)
                    except Exception:
                        pass  # Skip malformed objects

        return inner


def parse_color_channel(channel_str: str) -> ColorChannel | None:
    """Parse a color channel from its string representation.

    Args:
        channel_str: The color channel string (e.g., "1_255_2_128_3_64_6_1_...").

    Returns:
        ColorChannel or None: The parsed color channel, or None if parsing fails.
    """
    if not channel_str or "_" not in channel_str:
        return None

    try:
        pairs = channel_str.split("_")
        properties = {}

        for i in range(0, len(pairs) - 1, 2):
            if i + 1 < len(pairs):
                key = int(pairs[i])
                value_str = pairs[i + 1]

                # Try to parse as int or float
                try:
                    value = int(value_str)
                except ValueError:
                    try:
                        value = float(value_str)
                    except ValueError:
                        value = value_str

                properties[key] = value

        # Get the channel ID (should be key 6)
        if 6 not in properties:
            return None

        channel = ColorChannel(properties[6])
        channel.properties = properties

        return channel
    except Exception:
        return None


def parse_object(obj_str: str) -> LevelObject | None:
    """Parse an object from its string representation.

    Args:
        obj_str: The object string (e.g., "1,211,2,100,3,200").

    Returns:
        LevelObject or None: The parsed object, or None if parsing fails.
    """
    if not obj_str or "," not in obj_str:
        return None

    try:
        pairs = obj_str.split(",")
        properties = {}

        for i in range(0, len(pairs) - 1, 2):
            if i + 1 < len(pairs):
                key = int(pairs[i])
                value_str = pairs[i + 1]

                # Try to parse as int or float
                try:
                    value = int(value_str)
                except ValueError:
                    try:
                        value = float(value_str)
                    except ValueError:
                        value = value_str

                properties[key] = value

        # Get the object ID (should be key 1)
        if 1 not in properties:
            return None

        obj = LevelObject(properties[1])
        obj.properties = properties

        return obj
    except Exception:
        return None
