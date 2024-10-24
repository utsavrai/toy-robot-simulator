# Toy Robot Simulator

This is a Python application that simulates a toy robot moving on a 5x5 tabletop. The robot receives commands to move, turn, and report its position while ensuring that it doesn't fall off the table.

## Features

- **PLACE X,Y,F**: Places the robot at position (X,Y) on the table, facing direction F (NORTH, SOUTH, EAST, or WEST).
- **MOVE**: Moves the robot one unit forward in the direction it is currently facing.
- **LEFT/RIGHT**: Rotates the robot 90 degrees to the left or right without changing its position.
- **REPORT**: Outputs the current position and direction of the robot.

The robot ignores any commands that would cause it to fall off the table.

## Requirements

- Python 3.x

## Running the Simulator

1. Clone the repository:
   ```bash
   git clone https://github.com/utsavrai/toy-robot-simulator.git
   cd toy-robot-simulator
   ```

2. Run the simulator:
   ```bash
   python robot.py
   ```

   You can provide commands through standard input, such as:
   ```plaintext
   PLACE 0,0,NORTH
   MOVE
   REPORT
   ```

   The expected output for this example is:
   ```plaintext
   0,1,NORTH
   ```

## Running Unit Tests

1. Run the unit tests to verify the simulator's functionality:
   ```bash
   python -m unittest test_robot.py
   ```

