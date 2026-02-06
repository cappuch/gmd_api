"""Example showing color customization with gmd_api."""

from gmd_api import Level, LevelObject, ColorChannel

# Create a new level
level = Level(name="Colorful Example", description="A level with custom colors")

# Create custom color channels
red_channel = ColorChannel(1).set_rgb(255, 0, 0)
blue_channel = ColorChannel(2).set_rgb(0, 0, 255)
green_channel = ColorChannel(3).set_rgb(0, 255, 0)

level.add_color_channel(red_channel)
level.add_color_channel(blue_channel)
level.add_color_channel(green_channel)

# Create objects with different colors
obj1 = LevelObject(211).move_to(100, 100).set_base_color(1)
obj2 = LevelObject(211).move_to(200, 100).set_base_color(2)
obj3 = LevelObject(211).move_to(300, 100).set_base_color(3)

level.add_object(obj1)
level.add_object(obj2)
level.add_object(obj3)

# Create objects with HSV overrides
for i in range(10):
    obj = (
        LevelObject(211)
        .move_to(100 + i * 50, 200)
        .set_detail_hsv(-180 + i * 36, 1.0, 1.0)
    )
    level.add_object(obj)

# Save the level
level.save("colorful_example.gmd")
print("Level saved to colorful_example.gmd")
