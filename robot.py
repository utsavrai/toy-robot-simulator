# toy_robot_simulator.py

from enum import Enum
from dataclasses import dataclass
from typing import Optional
import logging

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

class Direction(Enum):
    """Enumeration for the four cardinal directions with rotation methods."""
    NORTH = 'NORTH'
    EAST = 'EAST'
    SOUTH = 'SOUTH'
    WEST = 'WEST'

    def rotate_left(self) -> 'Direction':
        """Rotate the direction 90 degrees to the left."""
        rotations = {
            Direction.NORTH: Direction.WEST,
            Direction.WEST: Direction.SOUTH,
            Direction.SOUTH: Direction.EAST,
            Direction.EAST: Direction.NORTH
        }
        return rotations[self]

    def rotate_right(self) -> 'Direction':
        """Rotate the direction 90 degrees to the right."""
        rotations = {
            Direction.NORTH: Direction.EAST,
            Direction.EAST: Direction.SOUTH,
            Direction.SOUTH: Direction.WEST,
            Direction.WEST: Direction.NORTH
        }
        return rotations[self]

@dataclass
class Position:
    """Dataclass to represent the robot's position and facing direction."""
    x: int
    y: int
    direction: Direction

    def move_forward(self) -> 'Position':
        """Calculate the new position when the robot moves forward."""
        moves = {
            Direction.NORTH: (0, 1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, -1),
            Direction.WEST: (-1, 0)
        }
        dx, dy = moves[self.direction]
        return Position(self.x + dx, self.y + dy, self.direction)

class Table:
    """Class to represent the tabletop dimensions and validity checks."""
    def __init__(self, width: int = 5, height: int = 5):
        """
        Initialize the table with given width and height.
        The default is a 5x5 grid.
        """
        self.width = width
        self.height = height

    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if a position is within the table boundaries."""
        return 0 <= x < self.width and 0 <= y < self.height

class Robot:
    """Class to represent the robot with actions it can perform."""
    def __init__(self, table: Table):
        """
        Initialize the robot with a reference to the table.
        Initially, the robot is not placed on the table.
        """
        self.table = table
        self.position: Optional[Position] = None

    def place(self, x: int, y: int, direction: Direction):
        """
        Place the robot at a specific position and direction on the table.
        Ignores the command if the position is invalid.
        """
        if self.table.is_valid_position(x, y):
            self.position = Position(x, y, direction)

    def move(self):
        """Move the robot one unit forward in the direction it is currently facing."""
        if not self.is_placed():
            return
        new_position = self.position.move_forward()
        if self.table.is_valid_position(new_position.x, new_position.y):
            self.position = new_position

    def left(self):
        """Rotate the robot 90 degrees to the left without changing its position."""
        if not self.is_placed():
            return
        self.position.direction = self.position.direction.rotate_left()

    def right(self):
        """Rotate the robot 90 degrees to the right without changing its position."""
        if not self.is_placed():
            return
        self.position.direction = self.position.direction.rotate_right()

    def report(self):
        """Output the robot's current position and facing direction."""
        if not self.is_placed():
            return
        output = f"{self.position.x},{self.position.y},{self.position.direction.value}"
        print(output)
        return output  # Return for testing purposes

    def is_placed(self) -> bool:
        """Check if the robot has been placed on the table."""
        return self.position is not None

import logging

# Set up logging configuration (you can adjust the level and format as needed)
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

class RobotSimulator:
    """Class to parse and execute commands for the robot simulator."""
    def __init__(self):
        """Initialize the simulator with a robot and a table."""
        self.robot = Robot(Table())

    def execute_command(self, command: str):
        """
        Parse and execute a command.
        Returns the output of REPORT command if applicable.
        Logs any invalid commands or errors during execution.
        """
        command = command.strip()
        if not command:
            return
        
        try:
            command = command.upper()
            if command.startswith('PLACE'):
                parts = command.split()
                if len(parts) == 2:
                    args = parts[1].split(',')
                    if len(args) == 3:
                        x = int(args[0])
                        y = int(args[1])
                        direction = Direction(args[2])
                        self.robot.place(x, y, direction)
                    else:
                        logging.warning(f"Invalid PLACE arguments: {parts[1]}")
            elif command == 'MOVE':
                self.robot.move()
            elif command == 'LEFT':
                self.robot.left()
            elif command == 'RIGHT':
                self.robot.right()
            elif command == 'REPORT':
                return self.robot.report()
            else:
                logging.warning(f"Unknown command: {command}")
        except (ValueError, KeyError) as e:
            logging.error(f"Error processing command '{command}': {e}")
        
        return None


def main():
    """Main function to run the robot simulator."""
    import sys
    simulator = RobotSimulator()
    for line in sys.stdin:
        simulator.execute_command(line)

if __name__ == '__main__':
    main()
