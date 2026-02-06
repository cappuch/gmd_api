# gmd_api

A simple, Pythonic API to create `.gmd` files for GDShare.

This removes the necessity to interact with the save file directly and allows for easy level sharing as a bonus. The API provides a high-level interface for creating and manipulating Geometry Dash levels programmatically.

[![CI](https://github.com/veprogames/gmd_api/workflows/CI/badge.svg)](https://github.com/veprogames/gmd_api/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Simple API**: Intuitive, fluent interface with method chaining
- **Full GMD Support**: Create, load, save, and modify GMD level files
- **Type Hints**: Full type annotations for better IDE support
- **Well Documented**: Comprehensive docstrings and examples
- **No Dependencies**: Uses only Python standard library
- **Extensible**: Easy to add support for new object properties

## Installation

Using a virtual environment (venv, conda, micromamba, etc.) is recommended:

```bash
# From PyPI (when published)
pip install gmd_api

# From GitHub
pip install git+https://github.com/veprogames/gmd_api

# For development
git clone https://github.com/veprogames/gmd_api
cd gmd_api
pip install -e .
pip install -r requirements-dev.txt
```

You can also add it to your `requirements.txt`:
```
git+https://github.com/veprogames/gmd_api@main
```

## Quick Start

```py
from gmd_api import Level, LevelObject, ColorChannel

# Create a new level
level = Level(name="My First Level", description="Created with gmd_api!")

# Add some objects
for i in range(10):
    obj = LevelObject(211).move_to(100 + i * 30, 100)
    level.add_object(obj)

# Configure level settings
level.inner().set_platformer(True).set_background_id(12)
level.set_official_song_id(22)

# Save the level
level.save("my_level.gmd")
```

## Example

This adds a 30x30 grid of differently colored blocks, sets the song to Explorers (won't play) and makes you having spent over 30 hours in the editor.

```py
from gmd_api.level import Level
from gmd_api.level_object import LevelObject
from gmd_api.color import ColorChannel

lvl = Level(name="~* Bypassing the Title Limits of the Client *~")

for x in range(30):
    for y in range(30):
        obj = LevelObject(211) \
            .move_to(15 + 30 * x, 15 + 30 * y) \
            .set_detail_hsv(-180 + (60 * x + 60 * y) % 360, 1.0, 1.0)
        lvl.add_object(obj)

channel = ColorChannel(1).set_rgb(255, 0, 0)
lvl.add_color_channel(channel)

lvl.inner() \
    .set_platformer() \
    .set_background_id(12) \
    .set_middleground_id(2)

lvl.set_time_spent(123456) \
    .set_official_song_id(22)

lvl.save("next.gmd")
```

## Documentation

- [Contributing Guide](CONTRIBUTING.md) - Guidelines for contributing to the project
- [Examples](examples/) - More example scripts demonstrating various features
- API documentation is available in the code as docstrings

### Main Classes

- **`Level`**: Represents a complete GMD level file with metadata and objects
- **`LevelObject`**: Represents a single object in the level (blocks, spikes, triggers, etc.)
- **`ColorChannel`**: Represents a color channel definition
- **`InnerLevelString`**: Represents the inner level data (objects, colors, settings)

### Key Features

#### Method Chaining
Most methods return `self`, allowing for fluent, chainable API calls:

```py
level = Level() \
    .set_name("My Level") \
    .set_official_song_id(10) \
    .set_time_spent(3600)
```

#### Object Positioning and Styling
```py
obj = LevelObject(211) \
    .move_to(100, 200) \
    .rotate_to(45) \
    .scale_to(1.5, 1.5) \
    .set_detail_hsv(180, 1.0, 1.0)
```

#### Color Channels
```py
channel = ColorChannel(1).set_rgba(255, 100, 50, 0.8)
level.add_color_channel(channel)
```

#### Loading and Modifying Levels
```py
level = Level.load("existing_level.gmd")
level.add_object(LevelObject(211).move_to(500, 500))
level.save("modified_level.gmd")
```

## Important Notes

⚠️ **This is a low-level interface.** There are helper methods, but no safeguards against missing or malformed data. Your game can crash when opening a level with malformed data.

- Always test your generated levels in Geometry Dash
- Use the example scripts as templates for your own levels
- Refer to the Geometry Dash modding community for object IDs and property keys

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/veprogames/gmd_api
cd gmd_api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=gmd_api --cov-report=html

# Run specific test file
pytest tests/test_level.py
```

### Code Quality

```bash
# Format code
black .
isort .

# Lint code
flake8 gmd_api

# Type check
mypy gmd_api
```

## Contributing

Contributions are welcome! Please read the [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### Areas for Contribution

- Adding support for more object properties
- Improving documentation and examples
- Adding more test coverage
- Performance optimizations
- Bug fixes

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Geometry Dash modding community for reverse engineering the level format
- Inspired by various GD level editing tools and libraries

## Related Projects

- [GDShare](https://github.com/GDColon/GDShare) - The original tool for sharing GMD files
- Other Geometry Dash level editing libraries and tools
