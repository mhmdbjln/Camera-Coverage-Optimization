# Camera Placement and Coverage Optimization with Obstacles

A Python/Pygame grid simulation for placing a limited number of cameras to cover as many randomly generated target cells as possible while excluding obstacle cells from camera placement and coverage.

## Simulation setup

The supplied `Camera.py` snapshot uses:

- A 15 × 15 grid.
- 30 randomly generated target points.
- A maximum of 5 cameras.
- Up to 5 user-drawn obstacle segments, each with a maximum length of 3 cells.
- A camera coverage range of 1 cell in each direction (a 3 × 3 square, clipped at grid boundaries).

Users can draw horizontal or vertical obstacles by selecting two grid cells, then run the placement routine or reset the simulation. The interface displays targets, cameras, obstacles, covered cells, and summary statistics.

## Greedy placement

The Greedy routine repeatedly evaluates candidate camera positions and selects a free cell whose coverage contains the largest number of currently uncovered target points. The procedure stops when all targets are covered, no additional useful placement is found, or the camera limit is reached.

## Note about the A* button

The interface also includes a button labeled `A*`. In the current source snapshot, this routine does not implement the conventional A* graph-search procedure with an open set, path-cost updates, and state expansion. It is an experimental heuristic option and should not be considered a canonical A* implementation.

Obstacles prevent cameras from being placed on obstacle cells and remove those cells from the coverage set. They do not currently model line-of-sight occlusion behind an obstacle.

## Requirements

- Python 3
- Pygame

Install and run:

```bash
pip install -r requirements.txt
python Camera.py
```

## License

No license has been specified.
