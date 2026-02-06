"""Example showing how to load and modify existing levels with gmd_api."""

from gmd_api import Level, LevelObject

# First, create a sample level to load
print("Creating a sample level...")
sample_level = Level(name="Original Level", description="This will be modified")
sample_level.add_object(LevelObject(211).move_to(100, 100))
sample_level.save("sample_level.gmd")
print("Sample level created: sample_level.gmd")

# Load the level
print("\nLoading the level...")
loaded_level = Level.load("sample_level.gmd")
print(f"Loaded level: {loaded_level.properties.get('k2', 'Unnamed')}")

# Modify the level
print("\nModifying the level...")
loaded_level.set_name("Modified Level")
loaded_level.set_description("This level has been modified")

# Add more objects
for i in range(5):
    obj = LevelObject(211).move_to(200 + i * 50, 150)
    loaded_level.add_object(obj)

print(f"Added {len(loaded_level.inner_string.objects) - 1} new objects")

# Save the modified level
loaded_level.save("modified_level.gmd")
print("\nModified level saved to modified_level.gmd")
