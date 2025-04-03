from os import path
from datetime import datetime
from rplidar import RPLidar

BAUD_RATE: int = 115200
TIMEOUT: int = 2

PATH = "COM5"

if __name__ == "__main__":
    if path.exists(PATH):
        print(f'Lidar found at {PATH}.')
        lidar = RPLidar(PATH, baudrate=BAUD_RATE, timeout=TIMEOUT)

        # info = lidar.get_info()

        # for key, value in info.items():
        #     print(f"{key}: {value}")
        
        # health = lidar.get_health()
        # print(f"Health: {health}")
        lidar.connect()
        print("Lidar connected.")

        health = lidar.get_health()
        print(f"Health checked {health}.")

        info = lidar.get_info()
        print(f"Info checked {info}.")
        # lidar.start_motor()
        # print("Motor started.")
        # lidar.start_scan()
        # print("Scanning started.")

        lidar.stop()
        print("Scanning stopped.")
        lidar.stop_motor()
        print("Motor stopped.")
        lidar.disconnect()
        print("Lidar disconnected.")
    else:
        print(f"No Lidar found at {PATH}.")