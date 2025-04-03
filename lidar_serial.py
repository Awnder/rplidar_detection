import serial
import struct
import time

# Replace 'COM_PORT' with your actual COM port
COM_PORT = '/dev/ttyUSB0'  # For Windows, e.g., 'COM3'; For Linux, e.g., '/dev/ttyUSB0'
BAUD_RATE = 115200  # Default baud rate for RPLIDAR

def read_lidar_data():
    with serial.Serial(COM_PORT, BAUD_RATE, timeout=1) as ser:
        time.sleep(2)  # Allow time for the connection to establish
        
        while True:
            # Read data from the lidar
            data = ser.read(7)  # Read 7 bytes
            if len(data) == 7:
                # Unpack data
                header, distance, angle, quality = struct.unpack('<BHHB', data)
                if header == 0xA5:  # Check for the correct header
                    print(f"Distance: {distance}, Angle: {angle}, Quality: {quality}")

if __name__ == "__main__":
    try:
        read_lidar_data()
    except KeyboardInterrupt:
        print("Program terminated.")
