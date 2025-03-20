# plug in lidar sensor and identify port with ls /dev/tty*

from rplidar import RPLidar
import RPi.GPIO as GPIO
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import threading

# Initialize GPIO for speaker
SPEAKER_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(SPEAKER_PIN, GPIO.OUT)
PWM = GPIO.PWM(SPEAKER_PIN, 3000)  # Set frequency to 3000 Hz
sound_event = threading.Event()

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

def emit_sound(frequency: int = 3000) -> None:
    """Emit sound using GPIO pin for the speaker.
    Args: 
        frequency (int): Frequency of the sound in Hz.
    """
    try:
        while True:
            PWM.ChangeFrequency(frequency)  # Set frequency for PWM
            PWM.start(50)  # Start PWM with 50% duty cycle (volume)
            sound_event.wait()  # Wait for the event to be set/unset (motion detected/ceased)
            PWM.stop()
            sound_event.clear()
    except Exception as e:
        print(f"Error in sound thread: {e}")
    finally:
        PWM.stop()

def update() -> tuple:
    """Public handler to update the plot for animation.
    Retrieves the latest LiDAR scan data, detects motion, and updates the scatter plot.
    If motion is detected, sound event triggers.
    Returns:
        tuple: Updated scatter plot object.
    """
    scan = next(lidar.iter_scans()) # iterator yielding list[quality, angle, distance]
    current_avg_distance = detect_motion(scan)

    if hasattr(update, 'prev_avg_distance') and current_avg_distance is not None:
        if abs(current_avg_distance - update.prev_avg_distance) > THRESHOLD_DISTANCE_CHANGE:
            print("Motion Detected!")
            sound_event.set()

    update.prev_avg_distance = current_avg_distance
    return _update_plot(scan)

def _update_plot(scan_data: list) -> tuple:
    """Private method to update the scatter plot with new LiDAR scan data.
    Args:
        scan_data (list): List of tuples containing (quality, angle, distance).
    Returns:
        tuple: Updated scatter plot object.
    """
    angles = np.array([np.deg2rad(angle) for (_, angle, _) in scan_data])
    distances = np.array([distance for (_, _, distance) in scan_data])
    x = distances * np.cos(angles)
    y = distances * np.sin(angles)
    sc.set_offsets(np.c_[x, y])
    return sc,

def detect_motion(scan_data: list) -> float:
    """Detect motion based on average distance from LiDAR scan data.
    Args:
        scan_data (list): List of tuples containing (quality, angle, distance)."
    Returns:
        float: Average distance from the LiDAR scan data, or None if no valid data.    
    """
    distances = np.array([distance for (_, _, distance) in scan_data if distance > 0])
    if len(distances) > 0:
        avg_distance = np.mean(distances)
        return avg_distance
    return None

if __name__ == "__main__":
    try:
        sound_thread = threading.Thread(target=emit_sound, args=(3000,), daemon=True)
        sound_thread.start()

        print("Starting LiDAR...")
        ani = FuncAnimation(fig, update, blit=True, interval=100)
        plt.show()
        
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        sound_event.clear()
        lidar.stop()
        lidar.disconnect()
        GPIO.cleanup()