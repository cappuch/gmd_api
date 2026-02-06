"""Tests for the LevelObject class."""

import pytest

from gmd_api import LevelObject


class TestLevelObject:
    """Test cases for the LevelObject class."""

    def test_create_object(self):
        """Test creating an object."""
        obj = LevelObject(211)
        assert obj is not None
        assert obj.properties[1] == 211

    def test_move_to(self):
        """Test moving an object."""
        obj = LevelObject(211).move_to(100, 200)
        assert obj.properties[2] == 100
        assert obj.properties[3] == 200

    def test_rotate_to(self):
        """Test rotating an object."""
        obj = LevelObject(211).rotate_to(45)
        assert obj.properties[6] == 45

    def test_scale_to(self):
        """Test scaling an object."""
        obj = LevelObject(211).scale_to(2.0, 1.5)
        assert obj.properties[128] == 2.0
        assert obj.properties[129] == 1.5

    def test_set_base_color(self):
        """Test setting base color channel."""
        obj = LevelObject(211).set_base_color(5)
        assert obj.properties[22] == 5

    def test_set_detail_color(self):
        """Test setting detail color channel."""
        obj = LevelObject(211).set_detail_color(6)
        assert obj.properties[21] == 6

    def test_set_color_channels(self):
        """Test setting both color channels."""
        obj = LevelObject(211).set_color_channels(5, 6)
        assert obj.properties[22] == 5
        assert obj.properties[21] == 6

    def test_set_base_hsv(self):
        """Test setting base HSV."""
        obj = LevelObject(211).set_base_hsv(180, 1.0, 1.0)
        assert obj.properties[42] == 1
        assert "180a1.0a1.0" in obj.properties[44]

    def test_set_detail_hsv(self):
        """Test setting detail HSV."""
        obj = LevelObject(211).set_detail_hsv(-90, 0.5, 0.8)
        assert obj.properties[41] == 1
        assert "-90a0.5a0.8" in obj.properties[43]

    def test_disable_base_hsv(self):
        """Test disabling base HSV."""
        obj = LevelObject(211).set_base_hsv(180, 1.0, 1.0).disable_base_hsv()
        assert obj.properties[42] == 0

    def test_set_groups(self):
        """Test setting group IDs."""
        obj = LevelObject(211).set_groups([1, 2, 3])
        assert obj.properties[57] == "1.2.3"

    def test_method_chaining(self):
        """Test that methods return self for chaining."""
        obj = LevelObject(211)
        result = obj.move_to(100, 200).rotate_to(45).scale_to(1.5, 1.5)
        assert result is obj

    def test_to_string(self):
        """Test converting object to string."""
        obj = LevelObject(211).move_to(100, 200)
        obj_string = obj.to_string()
        assert obj_string is not None
        assert "1,211" in obj_string
        assert "2,100" in obj_string
        assert "3,200" in obj_string
        assert obj_string.endswith(";")

    def test_get_property(self):
        """Test getting a property value."""
        obj = LevelObject(211).move_to(100, 200)
        assert obj.get(2) == 100
        assert obj.get(3) == 200
        assert obj.get(999) is None
