from enum import Enum
from dataclasses import dataclass
from typing import Optional, Tuple
import logging

# Constants
DEFAULT_TABLE_SIZE = 5
DEFAULT_LOG_LEVEL = logging.WARNING

# Configure logging
logging.basicConfig(level=DEFAULT_LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

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
    def __init__(self, width: int = DEFAULT_TABLE_SIZE, height: int = DEFAULT_TABLE_SIZE):
        """
        Initialize the table with given width and height.
        The default is a 5x5 grid.
        """
        if width <= 0 or height <= 0:
            raise ValueError("Table dimensions must be positive integers")
        self.width = width
        self.height = height

    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if a position is within the table boundaries."""
        return 0 <= x < self.width and 0 <= y < self.height

class Robot:
    """Class to represent the robot with actions it can perform."""
    def __init__(self, table: Table):
        """Initialize the robot with a reference to the table."""
        self.table = table
        self.position: Optional[Position] = None

    def place(self, x: int, y: int, direction: Direction) -> bool:
        """
        Place the robot at a specific position and direction on the table.
        Returns True if placement is successful, False otherwise.
        """
        if self.table.is_valid_position(x, y):
            self.position = Position(x, y, direction)
            return True
        else:
            logging.warning(f"Invalid placement at ({x}, {y})")
            return False

    def move(self) -> None:
        """Move the robot one unit forward in the direction it is currently facing."""
        if not self.is_placed():
            return
        new_position = self.position.move_forward()
        if self.table.is_valid_position(new_position.x, new_position.y):
            self.position = new_position
        else:
            logging.warning("Move ignored to prevent falling off the table")

    def left(self) -> None:
        """Rotate the robot 90 degrees to the left without changing its position."""
        if not self.is_placed():
            return
        self.position.direction = self.position.direction.rotate_left()

    def right(self) -> None:
        """Rotate the robot 90 degrees to the right without changing its position."""
        if not self.is_placed():
            return
        self.position.direction = self.position.direction.rotate_right()

    def report(self) -> Optional[str]:
        """Output the robot's current position and facing direction."""
        if not self.is_placed():
            return None
        output = f"{self.position.x},{self.position.y},{self.position.direction.value}"
        print(output)
        return output  # Return for testing purposes

    def is_placed(self) -> bool:
        """Check if the robot has been placed on the table."""
        return self.position is not None

class RobotSimulator:
    """Class to parse and execute commands for the robot simulator."""
    def __init__(self):
        """Initialize the simulator with a robot and a table."""
        self.robot = Robot(Table())
        self.command_history = []  # Store command history

    def execute_command(self, command: str) -> Tuple[bool, Optional[str]]:
        """
        Parse and execute a command.
        Returns a tuple (success: bool, output: Optional[str]).
        Logs any invalid commands or errors during execution.
        """
        command = command.strip()
        if not command:
            return False, None

        try:
            command_upper = command.upper()
            if command_upper.startswith('PLACE'):
                parts = command_upper.split()
                if len(parts) == 2:
                    args = parts[1].split(',')
                    if len(args) == 3:
                        x = int(args[0])
                        y = int(args[1])
                        direction = Direction(args[2])
                        success = self.robot.place(x, y, direction)
                        return success, None
                    else:
                        logging.warning(f"Invalid PLACE arguments: {parts[1]}")
                        return False, None
            elif command_upper == 'MOVE':
                self.robot.move()
                return True, None
            elif command_upper == 'LEFT':
                self.robot.left()
                return True, None
            elif command_upper == 'RIGHT':
                self.robot.right()
                return True, None
            elif command_upper == 'REPORT':
                output = self.robot.report()
                return True, output
            else:
                # Log a warning if the command is not recognized
                logging.warning(f"Unrecognized command: {command}")
                return False, None
        except (ValueError, KeyError) as e:
            logging.error(f"Error processing command '{command}': {e}")
            return False, None


def main():
    """Main function to run the robot simulator."""
    import sys
    simulator = RobotSimulator()
    try:
        for line in sys.stdin:
            simulator.execute_command(line)
    except (KeyboardInterrupt, SystemExit):
        print("\nSimulation terminated.")

if __name__ == '__main__':
    main()
