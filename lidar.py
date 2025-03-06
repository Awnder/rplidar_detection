# plug in lidar sensor and identify port with ls /dev/tty*

from rplidar import RPLidar
import numpy as np

# Initialize LiDAR
PORT_NAME = '/dev/ttyUSB0'  # Update based on setup
lidar = RPLidar(PORT_NAME)

# Parameters for motion detection
THRESHOLD_DISTANCE_CHANGE = 50  # Distance change in mm

def detect_motion(scan_data):
    distances = np.array([d for (_, _, d) in scan_data if d > 0])
    if len(distances) > 0:
        avg_distance = np.mean(distances)
        return avg_distance
    return None

try:
    print("Starting LiDAR...")
    prev_avg_distance = None

    for scan in lidar.iter_scans():
        current_avg_distance = detect_motion(scan)
        
        if prev_avg_distance is not None and current_avg_distance is not None:
            if abs(current_avg_distance - prev_avg_distance) > THRESHOLD_DISTANCE_CHANGE:
                print("Motion Detected!")
        
        prev_avg_distance = current_avg_distance

except KeyboardInterrupt:
    print("Stopping...")
finally:
    lidar.stop()
    lidar.disconnect()