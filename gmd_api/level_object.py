"""Level object module for representing in-game objects.

This module provides the LevelObject class which represents individual objects
in a Geometry Dash level with all their properties like position, rotation, colors, etc.
"""

from typing import Any, Iterable, Self

from .color import make_hsv_string
from .keys.objects import *


class LevelObject:
    """Represents a single object in a Geometry Dash level.

    Objects can be blocks, spikes, decorations, triggers, or any other placeable
    element in the level. Each object has an ID and various properties that define
    its appearance and behavior.

    Attributes:
        properties: Dictionary mapping property keys to values.

    Example:
        >>> obj = LevelObject(211)  # 211 is a block ID
        >>> obj.move_to(100, 200).rotate_to(45).set_base_hsv(180, 1.0, 1.0)
        >>> level.add_object(obj)
    """

    def __init__(self, id: int) -> None:
        """Initialize a new level object.

        Args:
            id: The object ID. Different IDs represent different object types
                (blocks, spikes, portals, triggers, etc.).
        """
        self.properties: dict[int, Any] = {}
        self.properties[ID] = id
        self.properties[155] = 1  # ???

    def get(self, key: int) -> Any:
        """Get a property value by key.

        Args:
            key: The property key to retrieve.

        Returns:
            The property value, or None if not set.
        """
        return self.properties[key] if key in self.properties else None

    def set(self, key: int, value: Any) -> Self:
        """Set a property value by key.

        Args:
            key: The property key (see gmd_api.keys.objects for constants).
            value: The value to set.

        Returns:
            Self: Returns self for method chaining.
        """
        self.properties[key] = value
        return self

    def move_to(self, x: float, y: float) -> Self:
        """Move the object to a specific position.

        Args:
            x: The x-coordinate position (in game units, 30 units = 1 block).
            y: The y-coordinate position (in game units, 30 units = 1 block).

        Returns:
            Self: Returns self for method chaining.
        """
        return self.set(POS_X, x).set(POS_Y, y)

    def rotate_to(self, degrees: float) -> Self:
        """Set the rotation angle of the object.

        Args:
            degrees: The rotation angle in degrees (0-360).

        Returns:
            Self: Returns self for method chaining.
        """
        return self.set(ROTATION_DEGREES, degrees)

    def scale_to(self, x: float, y: float) -> Self:
        """Set the scale of the object.

        Args:
            x: The x-axis scale factor (1.0 = normal size).
            y: The y-axis scale factor (1.0 = normal size).

        Returns:
            Self: Returns self for method chaining.
        """
        return self.set(SCALE_X, x).set(SCALE_Y, y)

    def set_base_color(self, channel_id: int) -> Self:
        """Set the base color channel for the object.

        Args:
            channel_id: The color channel ID to use for the base color.

        Returns:
            Self: Returns self for method chaining.
        """
        return self.set(COLOR_CHANNEL_BASE, channel_id)

    def set_detail_color(self, channel_id: int) -> Self:
        """Set the detail color channel for the object.

        Args:
            channel_id: The color channel ID to use for the detail color.

        Returns:
            Self: Returns self for method chaining.
        """
        return self.set(COLOR_CHANNEL_DETAIL, channel_id)

    def set_color_channels(self, base_id: int, detail_id: int) -> Self:
        """Set both base and detail color channels for the object.

        Args:
            base_id: The color channel ID for the base color.
            detail_id: The color channel ID for the detail color.

        Returns:
            Self: Returns self for method chaining.
        """
        return self.set_base_color(base_id).set_detail_color(detail_id)

    def set_base_hsv(self, h: int, s: float, v: float) -> Self:
        """Set the HSV color override for the base color.

        Args:
            h: Hue value (-180 to 180).
            s: Saturation value (0.0 to 1.0).
            v: Value/brightness (0.0 to 1.0).

        Returns:
            Self: Returns self for method chaining.
        """
        return self.set(HSV_BASE_ENABLED, 1).set(HSV_BASE, make_hsv_string(h, s, v))

    def disable_base_hsv(self) -> Self:
        """Disable the HSV color override for the base color.

        Returns:
            Self: Returns self for method chaining.
        """
        return self.set(HSV_BASE_ENABLED, 0)

    def set_detail_hsv(self, h: int, s: float, v: float) -> Self:
        """Set the HSV color override for the detail color.

        Args:
            h: Hue value (-180 to 180).
            s: Saturation value (0.0 to 1.0).
            v: Value/brightness (0.0 to 1.0).

        Returns:
            Self: Returns self for method chaining.
        """
        return self.set(HSV_DETAIL_ENABLED, 1).set(HSV_DETAIL, make_hsv_string(h, s, v))

    def disable_detail_hsv(self) -> Self:
        """Disable the HSV color override for the detail color.

        Returns:
            Self: Returns self for method chaining.
        """
        return self.set(HSV_DETAIL, 0)

    def set_groups(self, groups: Iterable[int]) -> Self:
        """Set the group IDs for this object.

        Groups are used for triggers to target specific objects.

        Args:
            groups: An iterable of group IDs (integers).

        Returns:
            Self: Returns self for method chaining.
        """
        groups_as_str = [str(gid) for gid in groups]
        return self.set(GROUPS, ".".join(groups_as_str))

    def to_string(self) -> str:
        """Convert the object to its string representation for the GMD format.

        Returns:
            str: The object data as a comma-separated string of key-value pairs.
        """
        return ",".join([f"{k},{v}" for k, v in sorted(self.properties.items())]) + ";"
