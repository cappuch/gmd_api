from .level_object import LevelObject
from .color import ColorChannel
from .level_string import InnerLevelString
from .keys.level import *
from typing import Self
import base64
import xml.etree.ElementTree as ET

class Level:
    def __init__(self, name: str = "", description: str = "") -> None:
        self.inner_string: InnerLevelString = InnerLevelString()
        self.properties: dict[str, any] = {}

        self.set_name(name)
        self.set_description(description)
        self.set(LEVEL_VERSION, 1)
        self.set(LEVEL_TYPE, LEVEL_TYPE_LOCAL)
        self.set(BINARY_VERSION, 40)
        self.set(KCEK, 4)
    
    def set(self, key: str, value: any) -> Self:
        self.properties[key] = value
        return self
    
    def set_time_spent(self, seconds: int) -> Self:
        return self.set(SECS_SPENT_EDITING, seconds)
    
    def set_official_song_id(self, id: int) -> Self:
        return self.set(OFFICIAL_SONG_ID, id)
    
    def set_custom_song_id(self, id: int) -> Self:
        return self.set(CUSTOM_SONG_ID, id)
    
    def set_name(self, name: str) -> Self:
        return self.set(LEVEL_NAME, name)

    def set_description(self, description: str) -> Self:
        encoded = base64.urlsafe_b64encode(bytes(description, encoding="utf-8"))
        decoded_back = encoded.decode("utf-8")
        return self.set(DESCRIPTION_BASE64, decoded_back)

    def add_object(self, obj: LevelObject) -> Self:
        self.inner_string.objects.append(obj)
        return self
    
    def add_color_channel(self, channel: ColorChannel) -> Self:
        self.inner_string.color_channels.append(channel)
        return self
    
    def inner(self) -> InnerLevelString:
        return self.inner_string

    def to_string(self) -> str:
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
        with open(to_file, "w") as f:
            f.write(self.to_string())

    @classmethod
    def load(cls, from_file: str) -> Self:
        with open(from_file, "r") as f:
            content = f.read()
        return cls.from_string(content)
    
    @classmethod
    def from_string(cls, gmd_string: str) -> Self:
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
    if isinstance(value, int):
        return "i"
    elif isinstance(value, bool):
        return "t" if value else "f"
    elif isinstance(value, float):
        return "r"
    elif isinstance(value, dict):
        return "d"
    return "s"