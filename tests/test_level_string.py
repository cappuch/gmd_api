"""Tests for the InnerLevelString class."""

import pytest

from gmd_api import ColorChannel, InnerLevelString, LevelObject


class TestInnerLevelString:
    """Test cases for the InnerLevelString class."""

    def test_create_inner_level_string(self):
        """Test creating an inner level string."""
        inner = InnerLevelString()
        assert inner is not None
        assert len(inner.objects) == 0
        assert len(inner.color_channels) > 0  # Has default colors

    def test_set_platformer(self):
        """Test setting platformer mode."""
        inner = InnerLevelString().set_platformer(True)
        assert inner.properties["kA23"] is True

    def test_set_background_id(self):
        """Test setting background ID."""
        inner = InnerLevelString().set_background_id(12)
        assert inner.properties["kA6"] == 12

    def test_set_ground_id(self):
        """Test setting ground ID."""
        inner = InnerLevelString().set_ground_id(5)
        assert inner.properties["kA7"] == 5

    def test_set_middleground_id(self):
        """Test setting middleground ID."""
        inner = InnerLevelString().set_middleground_id(3)
        assert inner.properties["kA25"] == 3

    def test_method_chaining(self):
        """Test that methods return self for chaining."""
        inner = InnerLevelString()
        result = inner.set_platformer(True).set_background_id(12).set_ground_id(5)
        assert result is inner

    def test_to_raw_string(self):
        """Test converting to raw string."""
        inner = InnerLevelString()
        raw_string = inner.to_raw_string()
        assert raw_string is not None
        assert "kS38" in raw_string

    def test_to_string(self):
        """Test converting to compressed string."""
        inner = InnerLevelString()
        compressed_string = inner.to_string()
        assert compressed_string is not None
        # Should be base64 encoded
        assert all(
            c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_="
            for c in compressed_string
        )

    def test_to_string_with_objects(self):
        """Test converting to string with objects."""
        inner = InnerLevelString()
        inner.objects.append(LevelObject(211).move_to(100, 200))
        inner.objects.append(LevelObject(211).move_to(200, 300))
        compressed_string = inner.to_string()
        assert compressed_string is not None
