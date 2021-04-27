# Add mistyPy directory to sys path
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# First import the RobotGenerator
from mistyPy.GenerateRobot import RobotGenerator

# Creating a new robot generator will rewrite the RobotCommands.py and Websocket.py 
# files to adjust them to the commands and websockets the robot has available
RobotGenerator("192.168.1.12")
