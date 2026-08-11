# BeltBuilder

An automated optimization engine and simulation framework for discovering optimal conveyor belt configurations, routing topologies, and item throughput in the game **Factorio**.

## Purpose & Architecture
In Factorio, designing high-throughput belt balancers, multi-lane splits, and underground transport layouts can be complex. **BeltBuilder** models Factorio's logistics grid to automatically discover and evaluate optimal belt configurations based on:

- **Throughput Maximization**: Simulates item movement across dual belt lanes (left/right sides) to minimize bottlenecks.
- **Automated Configuration Discovery**: Generates 2D spatial grid layouts and evaluates optimal placement of splitters, underground transports, item generators, and destroyers.
- **Directional Routing Engine**: Supports 4-directional flow (North, East, South, West) with subterranean distance mapping for underground belt pairs.

## Features
- **Grid Layout Engine**: Dynamic 2D spatial allocation (`template` class) for placing logistics components.
- **Splitters & Underground Belts**: Simulates color-coded underground routing and multi-lane splitters.
- **Item Flow Mechanics**: Models discrete item movement rates (`item`, `bside`, `generator` classes) relative to belt speeds and lane limits.

## Usage Example

```python
from beltbuilder import template, generator, belt

# Initialize Factorio grid template
grid = template()

# Add item generator and belts to evaluate throughput
gen = generator(parent=grid, beltside=3, speed=1, direction=0)
grid.AddObject(gen, 0, 0)

# Create belt and evaluate routing optimization
b = belt(parent=grid, color=1, direction=0)
grid.AddObject(b, 0, 1)

print(f"Grid bounds allocated: {len(grid.layout)}x{len(grid.layout[0])}")
```
