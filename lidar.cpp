#include <RPLidar.h>

// Pin definitions
#define RPLIDAR_MOTOR 3 // PWM pin for the motor control

// Create an instance of RPLidar
RPLidar lidar;

void setup() {
  // Initialize serial communication
  Serial.begin(115200);       // For debugging
  Serial1.begin(460800);      // For RPLidar communication (C1 baud rate)

  // Initialize the motor control pin
  pinMode(RPLIDAR_MOTOR, OUTPUT);
  analogWrite(RPLIDAR_MOTOR, 255); // Start the motor at full speed

  // Initialize the RPLidar
  if (lidar.begin(Serial1)) {
    Serial.println("RPLIDAR detected!");
  } else {
    Serial.println("Failed to connect to RPLIDAR");
    while (1); // Halt execution if LIDAR is not detected
  }
}

void loop() {
  if (IS_OK(lidar.waitPoint())) {
    float distance = lidar.getCurrentPoint().distance; // Distance in mm
    float angle = lidar.getCurrentPoint().angle;       // Angle in degrees

    // Print data to serial monitor
    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.print(" mm, Angle: ");
    Serial.println(angle);
  } else {
    Serial.println("No data received from RPLIDAR");
  }
}