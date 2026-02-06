"""Example showing advanced level features with gmd_api."""

from gmd_api import ColorChannel, Level, LevelObject

# Create a new level
level = Level(name="~* Advanced Example Level *~", description="Demonstrating advanced features")

# Create a grid of blocks with different properties
for x in range(20):
    for y in range(10):
        obj = (
            LevelObject(211)
            .move_to(100 + x * 30, 100 + y * 30)
            .rotate_to((x + y) * 15 % 360)
            .scale_to(0.5 + (x % 5) * 0.1, 0.5 + (y % 5) * 0.1)
            .set_detail_hsv((x * 18) % 360 - 180, 1.0, 1.0)
        )
        level.add_object(obj)

# Add objects to groups for triggers
grouped_obj = LevelObject(211).move_to(500, 500).set_groups([1, 2, 3])
level.add_object(grouped_obj)

# Configure level settings
level.inner().set_platformer(True).set_background_id(12).set_middleground_id(2).set_ground_id(3)

# Set level metadata
level.set_official_song_id(22).set_time_spent(123456)

# Save the level
level.save("advanced_example.gmd")
print("Level saved to advanced_example.gmd")
