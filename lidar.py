from rplidar import RPLidar
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize LiDAR
PORT_NAME = '/dev/ttyUSB0'  # Update based on setup
lidar = RPLidar(PORT_NAME)

# Parameters for motion detection
THRESHOLD_DISTANCE_CHANGE = 50  # Distance change in mm

# Initialize plot
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
sc = ax.scatter([], [], s=10, c='red')
ax.set_ylim(0, 6000)  # Adjust based on LiDAR range

def update(frame):
    scan = next(lidar.iter_scans())
    angles = np.radians([angle for (_, angle, _) in scan])
    distances = np.array([distance for (_, _, distance) in scan])
    
    sc.set_offsets(np.c_[angles, distances])
    return sc,

try:
    print("Starting LiDAR visualization...")
    ani = FuncAnimation(fig, update, interval=50, blit=True)
    plt.show()

except KeyboardInterrupt:
    print("Stopping...")
finally:
    lidar.stop()
    lidar.disconnect()
