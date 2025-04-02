from os import path
from datetime import datetime
from rplidar import RPLidar

BAUD_RATE: int = 115200
TIMEOUT: int = 1

PATH = "/dev/ttyUSB0"

if __name__ == "__main__":
    if path.exists(PATH):
        print(f'Lidar found at {PATH}.')
        lidar = RPLidar(PATH, baudrate=BAUD_RATE, timeout=TIMEOUT)

        info = lidar.get_info()

        for key, value in info.items():
            print(f"{key}: {value}")
        
        health = lidar.get_health()
        print(f"Health: {health}")

        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
    else:
        print(f"No Lidar found at {PATH}.")