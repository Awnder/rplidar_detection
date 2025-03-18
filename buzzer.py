# plug in lidar sensor and identify port with ls /dev/tty*

import RPi.GPIO as GPIO
import threading

# Initialize GPIO for speaker
SPEAKER_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(SPEAKER_PIN, GPIO.OUT)
PWM = GPIO.PWM(SPEAKER_PIN, 3000)  # Set frequency to 3000 Hz
sound_event = threading.Event()

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

if __name__ == "__main__":
    try:
        sound_thread = threading.Thread(target=emit_sound, args=(3000,), daemon=True)
        sound_thread.start()
        
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        sound_event.clear()
        GPIO.cleanup()