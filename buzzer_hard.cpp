#include <wiringPi.h>
#include <softPwm.h>
#include <iostream>

#define PWM_PIN 18 // GPIO18

int main() {
    // Initialize wiringPi
    if (wiringPiSetupGpio() == -1) {
        std::cerr << "Failed to initialize wiringPi!" << std::endl;
        return -1;
    }

    // Set up PWM pin
    pinMode(PWM_PIN, PWM_OUTPUT);

    // Configure PWM frequency and duty cycle
    // int frequency = 40000; // Ultrasonic frequency in Hz (40 kHz)
    int frequency = 2000;
    int range = 100;       // Range for duty cycle (0-100%)
    int dutyCycle = 50;    // Duty cycle percentage

    // Calculate clock divisor and range for desired frequency
    int clockDivisor = 192; // Base clock divisor
    int pwmRange = 19200000 / (clockDivisor * frequency); // Formula: base_freq / (divisor * target_freq)

    pwmSetMode(PWM_MODE_MS);       // Use mark-space mode for stable frequency
    pwmSetClock(clockDivisor);    // Set clock divisor
    pwmSetRange(pwmRange);        // Set range for PWM

    std::cout << "Generating sound at " << frequency << " Hz..." << std::endl;

    pwmWrite(PWM_PIN, (pwmRange * dutyCycle) / 100); // Start PWM with desired duty cycle

    delay(10000); // Keep the sound on for 10 seconds

    pwmWrite(PWM_PIN, 0); // Stop PWM
    std::cout << "Stopped ultrasonic sound." << std::endl;

    return 0;
}
