# test_toy_robot_simulator.py

import unittest
from robot import RobotSimulator, Direction

class TestToyRobotSimulator(unittest.TestCase):
    """Unit tests for the Toy Robot Simulator."""

    def setUp(self):
        """Initialize a new RobotSimulator before each test."""
        self.simulator = RobotSimulator()

    def test_example_a(self):
        """Test example a from the specification."""
        commands = [
            "PLACE 0,0,NORTH",
            "MOVE",
            "REPORT"
        ]
        for command in commands[:-1]:
            self.simulator.execute_command(command)
        output = self.simulator.robot.report()
        self.assertEqual(output, "0,1,NORTH")

    def test_example_b(self):
        """Test example b from the specification."""
        commands = [
            "PLACE 0,0,NORTH",
            "LEFT",
            "REPORT"
        ]
        for command in commands[:-1]:
            self.simulator.execute_command(command)
        output = self.simulator.robot.report()
        self.assertEqual(output, "0,0,WEST")

    def test_example_c(self):
        """Test example c from the specification."""
        commands = [
            "PLACE 1,2,EAST",
            "MOVE",
            "MOVE",
            "LEFT",
            "MOVE",
            "REPORT"
        ]
        for command in commands[:-1]:
            self.simulator.execute_command(command)
        output = self.simulator.robot.report()
        self.assertEqual(output, "3,3,NORTH")

    def test_ignore_commands_before_place(self):
        """Test that commands before the first PLACE are ignored."""
        commands = [
            "MOVE",
            "LEFT",
            "RIGHT",
            "REPORT",
            "PLACE 0,0,NORTH",
            "MOVE",
            "REPORT"
        ]
        outputs = []
        for command in commands:
            output = self.simulator.execute_command(command)
            if output is not None:
                outputs.append(output)
        self.assertEqual(outputs[-1], "0,1,NORTH")

    def test_invalid_place_commands(self):
        """Test that invalid PLACE commands are ignored."""
        commands = [
            "PLACE -1,0,NORTH",
            "PLACE 0,6,EAST",
            "PLACE 0,0,NORTHEAST",
            "PLACE 5,5,SOUTH",
            "PLACE 2,2,WEST"
        ]
        for command in commands:
            self.simulator.execute_command(command)
        output = self.simulator.robot.report()
        self.assertEqual(output, "2,2,WEST")

    def test_boundary_movements(self):
        """Test that the robot does not move off the table edges."""
        commands = [
            "PLACE 0,0,SOUTH",
            "MOVE",
            "REPORT",
            "PLACE 0,0,WEST",
            "MOVE",
            "REPORT",
            "PLACE 4,4,NORTH",
            "MOVE",
            "REPORT",
            "PLACE 4,4,EAST",
            "MOVE",
            "REPORT"
        ]
        expected_outputs = ["0,0,SOUTH", "0,0,WEST", "4,4,NORTH", "4,4,EAST"]
        outputs = []
        for command in commands:
            output = self.simulator.execute_command(command)
            if command.strip().upper() == "REPORT" and output is not None:
                outputs.append(output)
        self.assertEqual(outputs, expected_outputs)

    def test_multiple_place_commands(self):
        """Test that subsequent PLACE commands reset the robot's position."""
        commands = [
            "PLACE 1,2,SOUTH",
            "PLACE 0,0,NORTH",
            "MOVE",
            "PLACE 2,2,EAST",
            "MOVE",
            "LEFT",
            "MOVE",
            "REPORT"
        ]
        for command in commands:
            self.simulator.execute_command(command)
        output = self.simulator.robot.report()
        self.assertEqual(output, "3,3,NORTH")

    def test_invalid_commands(self):
        """Test that invalid commands are ignored."""
        commands = [
            "PLACE 0,0,NORTH",
            "MOVE",
            "JUMP",
            "TURN",
            "REPORT"
        ]
        for command in commands[:-1]:
            self.simulator.execute_command(command)
        output = self.simulator.robot.report()
        self.assertEqual(output, "0,1,NORTH")

    def test_case_insensitivity(self):
        """Test that the simulator handles commands regardless of case."""
        commands = [
            "place 0,0,north",
            "MoVe",
            "report"
        ]
        for command in commands[:-1]:
            self.simulator.execute_command(command)
        output = self.simulator.robot.report()
        self.assertEqual(output, "0,1,NORTH")

    def test_no_initial_place(self):
        """Test that commands before the first valid PLACE are ignored."""
        commands = [
            "MOVE",
            "LEFT",
            "REPORT",
            "PLACE 1,2,EAST",
            "MOVE",
            "REPORT"
        ]
        outputs = []
        for command in commands:
            output = self.simulator.execute_command(command)
            if command.strip().upper() == "REPORT" and output is not None:
                outputs.append(output)
        self.assertEqual(outputs[-1], "2,2,EAST")

    def test_full_rotation(self):
        """Test that rotating four times returns the robot to its original direction."""
        commands = [
            "PLACE 1,1,NORTH",
            "LEFT",
            "LEFT",
            "LEFT",
            "LEFT",
            "REPORT",
            "RIGHT",
            "RIGHT",
            "RIGHT",
            "RIGHT",
            "REPORT"
        ]
        expected_outputs = ["1,1,NORTH", "1,1,NORTH"]
        outputs = []
        for command in commands:
            output = self.simulator.execute_command(command)
            if command.strip().upper() == "REPORT" and output is not None:
                outputs.append(output)
        self.assertEqual(outputs, expected_outputs)

    def test_movement_after_rotation(self):
        """Test that movement and rotations are handled correctly."""
        commands = [
            "PLACE 1,1,NORTH",
            "RIGHT",
            "MOVE",
            "RIGHT",
            "MOVE",
            "RIGHT",
            "MOVE",
            "RIGHT",
            "MOVE",
            "REPORT"
        ]
        for command in commands:
            self.simulator.execute_command(command)
        output = self.simulator.robot.report()
        self.assertEqual(output, "1,1,NORTH")

    def test_report_at_edge(self):
        """Test reporting when the robot is at the edge of the table."""
        commands = [
            "PLACE 0,4,NORTH",
            "REPORT"
        ]
        for command in commands:
            self.simulator.execute_command(command)
        output = self.simulator.robot.report()
        self.assertEqual(output, "0,4,NORTH")

    def test_invalid_direction(self):
        """Test that invalid directions are not accepted."""
        commands = [
            "PLACE 0,0,NORTHWEST",
            "REPORT",
            "PLACE 0,0,SOUTH",
            "REPORT"
        ]
        outputs = []
        for command in commands:
            output = self.simulator.execute_command(command)
            if command.strip().upper() == "REPORT" and output is not None:
                outputs.append(output)
        self.assertEqual(outputs[-1], "0,0,SOUTH")

    def test_place_off_table(self):
        """Test that placing the robot off the table is ignored."""
        commands = [
            "PLACE 6,6,NORTH",
            "REPORT",
            "PLACE -1,-1,SOUTH",
            "REPORT"
        ]
        outputs = []
        for command in commands:
            output = self.simulator.execute_command(command)
            if output is not None:
                outputs.append(output)
        self.assertEqual(outputs, [])

    def test_movement_blocked_at_edge(self):
        """Test that the robot does not move beyond the table boundaries."""
        commands = [
            "PLACE 0,0,SOUTH",
            "MOVE",
            "MOVE",
            "REPORT"
        ]
        for command in commands:
            self.simulator.execute_command(command)
        output = self.simulator.robot.report()
        self.assertEqual(output, "0,0,SOUTH")

    def test_combined_commands(self):
        """Test a complex sequence of commands."""
        commands = [
            "PLACE 2,2,EAST",
            "MOVE",
            "MOVE",
            "LEFT",
            "MOVE",
            "REPORT",
            "MOVE",
            "RIGHT",
            "MOVE",
            "REPORT"
        ]
        expected_outputs = ["4,3,NORTH", "4,4,EAST"]
        outputs = []
        for command in commands:
            output = self.simulator.execute_command(command)
            if command.strip().upper() == "REPORT" and output is not None:
                outputs.append(output)
        self.assertEqual(outputs, expected_outputs)

if __name__ == '__main__':
    unittest.main()
