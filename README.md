# BeltBuilder

A Python-based simulation engine for modeling conveyor belt grids, item throughput, splitters, underground transports, and item generators. Inspired by Factorio-style logistical belt layouts.

## Features
- **Grid Layout Templates**: Dynamic 2D spatial allocation of belt components.
- **Item Generators & Destroyers**: Control item ingress and egress rates across belt directions.
- **Underground Belts & Splitters**: Simulates color-coded underground routing and multi-lane belt throughput.
- **Directional Routing**: Supports 4-directional flow (North, East, South, West) and dual-sided transport lanes.

## Usage

```python
from beltbuilder import template, generator, belt

# Initialize grid template
grid = template()

# Add item generator and belts
gen = generator(parent=grid, beltside=3, speed=1, direction=0)
grid.AddObject(gen, 0, 0)
```
