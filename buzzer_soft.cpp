#include <wiringPi.h>
#include <softPwm.h>
#include <thread>
#include <atomic>
#include <iostream>

#define SPEAKER_PIN 0 // GPIO17 corresponds to wiringPi pin 0

std::atomic<bool> sound_event(false);

void emit_sound(int frequency = 10000) {
    /**
     * Emit sound using GPIO pin for the speaker.
     * Args:
     *     frequency (int): Frequency of the sound in Hz.
     */
    try {
        while (true) {
            if (sound_event.load()) {
                softPwmWrite(SPEAKER_PIN, 50); // 50% duty cycle
                delayMicroseconds(1000000 / frequency); // Delay for frequency
                softPwmWrite(SPEAKER_PIN, 0); // Turn off
                delayMicroseconds(1000000 / frequency); // Delay for frequency
            } else {
                delay(10); // Small delay to avoid busy-waiting
            }
        }
    } catch (const std::exception &e) {
        std::cerr << "Error in sound thread: " << e.what() << std::endl;
    }
}

int main() {
    try {
        // Initialize wiringPi and set up the speaker pin
        if (wiringPiSetup() == -1) {
            std::cerr << "Failed to initialize wiringPi" << std::endl;
            return 1;
        }

        if (softPwmCreate(SPEAKER_PIN, 0, 100) != 0) {
            std::cerr << "Failed to initialize PWM on pin " << SPEAKER_PIN << std::endl;
            return 1;
        }

        // Start the sound thread
        std::thread sound_thread(emit_sound, 3000);

        // Simulate setting the sound_event flag (e.g., motion detected)
        sound_event.store(true);
        std::this_thread::sleep_for(std::chrono::seconds(5)); // Emit sound for 5 seconds
        sound_event.store(false);

        // Wait for the sound thread to finish (in this case, it won't, so detach it)
        sound_thread.detach();
    } catch (...) {
        std::cerr << "An error occurred" << std::endl;
    } finally {
        // Clean up
        softPwmWrite(SPEAKER_PIN, 0);
    }

    return 0;
}
