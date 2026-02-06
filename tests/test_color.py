"""Tests for the ColorChannel class."""

import pytest

from gmd_api import ColorChannel
from gmd_api.color import get_default_colors, make_hsv_string


class TestColorChannel:
    """Test cases for the ColorChannel class."""

    def test_create_color_channel(self):
        """Test creating a color channel."""
        channel = ColorChannel(1)
        assert channel is not None
        assert channel.properties[6] == 1

    def test_set_rgb(self):
        """Test setting RGB values."""
        channel = ColorChannel(1).set_rgb(255, 128, 64)
        assert channel.properties[1] == 255
        assert channel.properties[2] == 128
        assert channel.properties[3] == 64

    def test_set_opacity(self):
        """Test setting opacity."""
        channel = ColorChannel(1).set_opacity(0.5)
        assert channel.properties[7] == 0.5

    def test_set_rgba(self):
        """Test setting RGBA values."""
        channel = ColorChannel(1).set_rgba(255, 0, 0, 0.75)
        assert channel.properties[1] == 255
        assert channel.properties[2] == 0
        assert channel.properties[3] == 0
        assert channel.properties[7] == 0.75

    def test_method_chaining(self):
        """Test that methods return self for chaining."""
        channel = ColorChannel(1)
        result = channel.set_rgb(255, 0, 0).set_opacity(0.9)
        assert result is channel

    def test_to_string(self):
        """Test converting color channel to string."""
        channel = ColorChannel(1).set_rgb(255, 0, 0)
        channel_string = channel.to_string()
        assert channel_string is not None
        assert "_" in channel_string
        assert channel_string.endswith("|")


class TestColorUtilities:
    """Test cases for color utility functions."""

    def test_get_default_colors(self):
        """Test getting default color channels."""
        colors = get_default_colors()
        assert len(colors) == 8
        assert all(isinstance(c, ColorChannel) for c in colors)

    def test_make_hsv_string(self):
        """Test creating HSV string."""
        hsv = make_hsv_string(180, 1.0, 0.5)
        assert hsv == "180a1.0a0.5a0a0"
