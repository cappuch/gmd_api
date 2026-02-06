"""Tests for the Level class."""

import tempfile
from pathlib import Path

import pytest

from gmd_api import Level, LevelObject, ColorChannel


class TestLevel:
    """Test cases for the Level class."""

    def test_create_empty_level(self):
        """Test creating an empty level."""
        level = Level()
        assert level is not None
        assert level.properties is not None
        assert level.inner_string is not None

    def test_create_level_with_name_and_description(self):
        """Test creating a level with name and description."""
        level = Level(name="Test Level", description="A test level")
        assert "k2" in level.properties
        assert level.properties["k2"] == "Test Level"
        assert "k3" in level.properties

    def test_set_official_song(self):
        """Test setting an official song."""
        level = Level()
        level.set_official_song_id(22)
        assert level.properties["k8"] == 22

    def test_set_custom_song(self):
        """Test setting a custom song."""
        level = Level()
        level.set_custom_song_id(123456)
        assert level.properties["k45"] == 123456

    def test_set_time_spent(self):
        """Test setting time spent editing."""
        level = Level()
        level.set_time_spent(3600)
        assert level.properties["k80"] == 3600

    def test_add_object(self):
        """Test adding objects to a level."""
        level = Level()
        obj = LevelObject(211).move_to(100, 200)
        level.add_object(obj)
        assert len(level.inner_string.objects) == 1
        assert level.inner_string.objects[0].properties[1] == 211

    def test_add_color_channel(self):
        """Test adding color channels to a level."""
        level = Level()
        initial_count = len(level.inner_string.color_channels)
        channel = ColorChannel(1).set_rgb(255, 0, 0)
        level.add_color_channel(channel)
        assert len(level.inner_string.color_channels) == initial_count + 1

    def test_to_string(self):
        """Test converting level to string format."""
        level = Level(name="Test")
        level_string = level.to_string()
        assert level_string is not None
        assert "<?xml version" in level_string
        assert "<plist" in level_string
        assert "Test" in level_string

    def test_save_and_load(self):
        """Test saving and loading a level."""
        # Create a level
        level = Level(name="Save Test", description="Test saving")
        level.set_official_song_id(10)
        obj = LevelObject(211).move_to(100, 200)
        level.add_object(obj)

        # Save to temporary file
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_level.gmd"
            level.save(str(filepath))

            # Load it back
            loaded_level = Level.load(str(filepath))

            # Verify basic properties
            assert loaded_level.properties["k2"] == "Save Test"
            assert loaded_level.properties["k8"] == 10
            assert len(loaded_level.inner_string.objects) == 1

    def test_method_chaining(self):
        """Test that methods return self for chaining."""
        level = Level()
        result = level.set_name("Test").set_official_song_id(5).set_time_spent(100)
        assert result is level
        assert level.properties["k2"] == "Test"
        assert level.properties["k8"] == 5
        assert level.properties["k80"] == 100

    def test_inner_returns_inner_string(self):
        """Test that inner() returns the InnerLevelString."""
        level = Level()
        inner = level.inner()
        assert inner is level.inner_string
