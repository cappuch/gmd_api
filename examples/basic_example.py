"""Basic example of creating a simple level with gmd_api."""

from gmd_api import ColorChannel, Level, LevelObject

# Create a new level
level = Level(name="Basic Example", description="A simple level created with gmd_api")

# Add a few blocks in a line
for i in range(10):
    obj = LevelObject(211).move_to(100 + i * 30, 100)
    level.add_object(obj)

# Set level properties
level.set_official_song_id(10).set_time_spent(300)

# Configure inner level settings
level.inner().set_platformer(False).set_background_id(1)

# Save the level
level.save("basic_example.gmd")
print("Level saved to basic_example.gmd")
