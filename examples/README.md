# Examples

This directory contains example scripts demonstrating how to use gmd_api.

## Running the Examples

Make sure you have installed gmd_api:

```bash
pip install -e .
```

Then run any example:

```bash
python examples/basic_example.py
python examples/colorful_example.py
python examples/advanced_example.py
python examples/load_and_modify.py
```

## Examples

### basic_example.py
Shows the basics of creating a level, adding objects, and saving.

### colorful_example.py
Demonstrates how to create and use custom color channels and HSV overrides.

### advanced_example.py
Shows more advanced features including grids, groups, rotations, and scaling.

### load_and_modify.py
Demonstrates how to load an existing level, modify it, and save it back.

## Notes

- All examples create `.gmd` files in the current directory
- These files can be imported into Geometry Dash using GDShare
- The examples use object ID 211 which is a basic block
