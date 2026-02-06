"""Level module for creating and managing Geometry Dash levels.

This module provides the Level class which represents a complete GMD level file
with all its properties, objects, and color channels.
"""

import base64
import xml.etree.ElementTree as ET
from typing import Self

from .color import ColorChannel
from .keys.level import *
from .level_object import LevelObject
from .level_string import InnerLevelString


class Level:
    """Represents a Geometry Dash level in the GMD format.

    A Level contains metadata (name, description, song, etc.) and an inner level string
    with objects, color channels, and settings. This class provides methods to create,
    load, save, and manipulate level files.

    Attributes:
        inner_string: The InnerLevelString containing objects and color channels.
        properties: Dictionary of level metadata properties.

    Example:
        >>> level = Level(name="My Level", description="A cool level")
        >>> level.set_official_song_id(22)
        >>> obj = LevelObject(211).move_to(100, 100)
        >>> level.add_object(obj)
        >>> level.save("my_level.gmd")
    """

    def __init__(self, name: str = "", description: str = "") -> None:
        """Initialize a new Level.

        Args:
            name: The name of the level. Defaults to empty string.
            description: The description of the level. Defaults to empty string.
        """
        self.inner_string: InnerLevelString = InnerLevelString()
        self.properties: dict[str, any] = {}

        self.set_name(name)
        self.set_description(description)
        self.set(LEVEL_VERSION, 1)
        self.set(LEVEL_TYPE, LEVEL_TYPE_LOCAL)
        self.set(BINARY_VERSION, 40)
        self.set(KCEK, 4)
    
    def set(self, key: str, value: any) -> Self:
        """Set a level property by key.

        Args:
            key: The property key (see gmd_api.keys.level for constants).
            value: The value to set for the property.

        Returns:
            Self: Returns self for method chaining.
        """
        self.properties[key] = value
        return self
    
    def set_time_spent(self, seconds: int) -> Self:
        """Set the time spent editing the level.

        Args:
            seconds: Time spent editing in seconds.

        Returns:
            Self: Returns self for method chaining.
        """
        return self.set(SECS_SPENT_EDITING, seconds)
    
    def set_official_song_id(self, id: int) -> Self:
        """Set the official song ID for the level.

        Args:
            id: The official song ID (0-21+ for in-game songs).

        Returns:
            Self: Returns self for method chaining.
        """
        return self.set(OFFICIAL_SONG_ID, id)
    
    def set_custom_song_id(self, id: int) -> Self:
        """Set the custom song ID for the level.

        Args:
            id: The custom song ID from Newgrounds.

        Returns:
            Self: Returns self for method chaining.
        """
        return self.set(CUSTOM_SONG_ID, id)
    
    def set_name(self, name: str) -> Self:
        """Set the level name.

        Args:
            name: The name for the level.

        Returns:
            Self: Returns self for method chaining.
        """
        return self.set(LEVEL_NAME, name)

    def set_description(self, description: str) -> Self:
        """Set the level description.

        The description is automatically base64-encoded as required by the GMD format.

        Args:
            description: The description text for the level.

        Returns:
            Self: Returns self for method chaining.
        """
        encoded = base64.urlsafe_b64encode(bytes(description, encoding="utf-8"))
        decoded_back = encoded.decode("utf-8")
        return self.set(DESCRIPTION_BASE64, decoded_back)

    def add_object(self, obj: LevelObject) -> Self:
        """Add an object to the level.

        Args:
            obj: The LevelObject to add to the level.

        Returns:
            Self: Returns self for method chaining.
        """
        self.inner_string.objects.append(obj)
        return self
    
    def add_color_channel(self, channel: ColorChannel) -> Self:
        """Add a color channel to the level.

        Args:
            channel: The ColorChannel to add to the level.

        Returns:
            Self: Returns self for method chaining.
        """
        self.inner_string.color_channels.append(channel)
        return self
    
    def inner(self) -> InnerLevelString:
        """Get the inner level string containing objects and settings.

        Returns:
            InnerLevelString: The inner level data object.
        """
        return self.inner_string

    def to_string(self) -> str:
        """Convert the level to a GMD format string.

        Returns:
            str: The level data in GMD XML format.
        """
        props = "".join(
            f"<k>{k}</k><{get_type_tag(v)}>{v}</{get_type_tag(v)}>" for k, v in self.properties.items()
        )

        string: str = f"""<?xml version="1.0"?>
<plist version="1.0" gjver="2.0">
    <dict>
        <k>k4</k><s>{self.inner_string.to_string()}</s>
        {props}
    </dict>
</plist>"""
        return string \
            .replace("\n", "") \
            .replace("\t", "")
    
    def save(self, to_file: str) -> None:
        """Save the level to a GMD file.

        Args:
            to_file: The file path where the level should be saved.
        """
        with open(to_file, "w") as f:
            f.write(self.to_string())

    @classmethod
    def load(cls, from_file: str) -> Self:
        """Load a level from a GMD file.

        Args:
            from_file: The file path to load the level from.

        Returns:
            Level: A new Level instance with data loaded from the file.
        """
        with open(from_file, "r") as f:
            content = f.read()
        return cls.from_string(content)
    
    @classmethod
    def from_string(cls, gmd_string: str) -> Self:
        """Parse a level from a GMD format string.

        Args:
            gmd_string: The GMD XML string to parse.

        Returns:
            Level: A new Level instance with data parsed from the string.

        Raises:
            ValueError: If the GMD format is invalid or malformed.
        """
        level = cls()
        level.properties.clear()  # clear default properties
        
        # parse XML
        root = ET.fromstring(gmd_string)
        
        # find the dict element
        dict_elem = root.find("dict")
        if dict_elem is None:
            raise ValueError("Invalid GMD format: no dict element found")

        # parse key-value pairs
        children = list(dict_elem)
        i = 0
        while i < len(children):
            if children[i].tag == "k":
                key = children[i].text
                i += 1
                
                if i >= len(children):
                    break
                
                value_elem = children[i]
                value = parse_value(value_elem)

                # handle the inner level string (k4)
                if key == "k4":
                    if isinstance(value, str):
                        level.inner_string = InnerLevelString.from_string(value)
                else:
                    level.properties[key] = value
                
                i += 1
            else:
                i += 1
        
        return level


def parse_value(elem: ET.Element) -> any:
    """Parse a value from an XML element based on its tag type.

    Args:
        elem: The XML element to parse.

    Returns:
        The parsed value (int, str, float, bool, or dict).
    """
    if elem.tag == "i":
        return int(elem.text) if elem.text else 0
    elif elem.tag == "s":
        return elem.text if elem.text else ""
    elif elem.tag == "d":
        result = {}
        children = list(elem)
        i = 0
        while i < len(children):
            if children[i].tag == "k":
                key = children[i].text
                i += 1
                if i < len(children):
                    result[key] = parse_value(children[i])
                    i += 1
            else:
                i += 1
        return result
    elif elem.tag == "t":
        return True
    elif elem.tag == "f":
        return False
    elif elem.tag == "r":
        return float(elem.text) if elem.text else 0.0
    else:
        return elem.text if elem.text else ""


def get_type_tag(value: any) -> str:
    """Get the XML tag type for a Python value.

    Args:
        value: The Python value to get a tag for.

    Returns:
        str: The XML tag name ('i', 't', 'f', 'r', 'd', or 's').
    """
    if isinstance(value, int):
        return "i"
    elif isinstance(value, bool):
        return "t" if value else "f"
    elif isinstance(value, float):
        return "r"
    elif isinstance(value, dict):
        return "d"
    return "s"