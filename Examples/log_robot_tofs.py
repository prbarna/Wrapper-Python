# Add mistyPy directory to sys path
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mistyPy.Robot import Robot
from mistyPy.Events import Events
from time import time

ROBOT_IP = "192.168.1.12"

misty_robot = Robot(ROBOT_IP)

tof_condition_lookup = {
    "rfr": {"Property": "SensorPosition", "Inequality": "=", "Value": "Right"},
    "rfc": {"Property": "SensorPosition", "Inequality": "=", "Value": "Center"},
    "rfl": {"Property": "SensorPosition", "Inequality": "=", "Value": "Left"},
    "rbb": {"Property": "SensorPosition", "Inequality": "=", "Value": "Back"},
    "efr": {"Property": "SensorPosition", "Inequality": "=", "Value": "DownFrontRight"},
    "efl": {"Property": "SensorPosition", "Inequality": "=", "Value": "DownFrontLeft"},
    "ebr": {"Property": "SensorPosition", "Inequality": "=", "Value": "DownBackRight"},
    "ebl": {"Property": "SensorPosition", "Inequality": "=", "Value": "DownBackLeft"}
    }


def log_tof_reading(message):
    tof_message = message["message"]

    print(f"{tof_message['created'][:-1].replace('T',' ')},{tof_message['sensorId']},{tof_message['distanceInMeters']},{tof_message['status']},{tof_message['inHazard']},{tof_message['signal']},{tof_message['sigma']}", file=f)
    f.flush()


if __name__ == "__main__":
    f = open(f"new_firmware_tof_logs_{time()}.csv", "w")
    print("time,sensor id,distance,status,in hazard,signal,sigma", file=f)

    try:
        # Subscribe to the tofs individually so each message from each tof is written to a new line
        front_right = misty_robot.RegisterEvent("frontright", Events.TimeOfFlight, condition=[tof_condition_lookup["rfr"]], keep_alive=True, callback_function=log_tof_reading, debounce=5)
        front_center = misty_robot.RegisterEvent("frontcenter", Events.TimeOfFlight, condition=[tof_condition_lookup["rfc"]], keep_alive=True, callback_function=log_tof_reading, debounce=5)
        front_left = misty_robot.RegisterEvent("frontleft", Events.TimeOfFlight, condition=[tof_condition_lookup["rfl"]], keep_alive=True, callback_function=log_tof_reading, debounce=5)
        back_range = misty_robot.RegisterEvent("back", Events.TimeOfFlight, condition=[tof_condition_lookup["rbb"]], keep_alive=True, callback_function=log_tof_reading, debounce=5)
        down_front_right = misty_robot.RegisterEvent("downfrontright", Events.TimeOfFlight, condition=[tof_condition_lookup["efr"]], keep_alive=True, callback_function=log_tof_reading, debounce=5)
        down_front_left = misty_robot.RegisterEvent("downfrontleft", Events.TimeOfFlight, condition=[tof_condition_lookup["efl"]], keep_alive=True, callback_function=log_tof_reading, debounce=5)
        down_back_right = misty_robot.RegisterEvent("downbackright", Events.TimeOfFlight, condition=[tof_condition_lookup["ebr"]], keep_alive=True, callback_function=log_tof_reading, debounce=5)
        down_back_left = misty_robot.RegisterEvent("downbackleft", Events.TimeOfFlight, condition=[tof_condition_lookup["ebl"]], keep_alive=True, callback_function=log_tof_reading, debounce=5)

        # Use the KeepAlive() function if you want to keep the main thread alive, otherwise the event threads will also get killed once processing has stopped
        misty_robot.KeepAlive()

    except Exception as ex:
        print(ex)
    finally:
        f.close()
        # Unregister from all events or the spawned threads won't get killed
        misty_robot.UnregisterAllEvents()
        