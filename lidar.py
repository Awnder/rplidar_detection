# plug in lidar sensor and identify port with ls /dev/tty*

from rplidar import RPLidar
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np

# Initialize LiDAR
PORT_NAME = '/dev/ttyUSB0'  # Update based on setup
lidar = RPLidar(PORT_NAME)

# Parameters for motion detection
THRESHOLD_DISTANCE_CHANGE = 50  # Distance change in mm

# Initialize plot
fig, ax = plt.subplots()
sc = ax.scatter([], [], s=5)
ax.set_xlim(-4000, 4000)
ax.set_ylim(-4000, 4000)
ax.set_aspect('equal', 'box')
ax.grid(True)

def update_plot(scan_data: list) -> tuple:
    """Update the scatter plot with new LiDAR scan data.
    Args:
        scan_data (list): List of tuples containing (angle, distance, quality).
    Returns:
        tuple: Updated scatter plot object.
    """
    angles = np.array([np.deg2rad(angle) for (_, angle, _) in scan_data])
    distances = np.array([distance for (_, _, distance) in scan_data])
    x = distances * np.cos(angles)
    y = distances * np.sin(angles)
    sc.set_offsets(np.c_[x, y])
    return sc,

def update() -> tuple:
    """Update the plot for animation.
    Returns:
        tuple: Updated scatter plot object.
    """
    scan = next(lidar.iter_scans())
    current_avg_distance = detect_motion(scan)
    
    if hasattr(update, 'prev_avg_distance') and current_avg_distance is not None:
        if abs(current_avg_distance - update.prev_avg_distance) > THRESHOLD_DISTANCE_CHANGE:
            print("Motion Detected!")
    
    update.prev_avg_distance = current_avg_distance
    return update_plot(scan)

def detect_motion(scan_data: list) -> float:
    """Detect motion based on average distance from LiDAR scan data.
    Args:
        scan_data (list): List of tuples containing (angle, distance, quality)."
    Returns:
        float: Average distance from the LiDAR scan data, or None if no valid data.    
    """
    distances = np.array([d for (_, _, d) in scan_data if d > 0])
    if len(distances) > 0:
        avg_distance = np.mean(distances)
        return avg_distance
    return None

if __name__ == "__main__":
    try:
        print("Starting LiDAR...")
        ani = FuncAnimation(fig, update, blit=True, interval=100)
        plt.show()
        
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        lidar.stop()
        lidar.disconnect()