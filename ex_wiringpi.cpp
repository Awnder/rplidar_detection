#include <wiringPi.h> // Include WiringPi library!
#include <softPwm.h>
#include <cstdio>

# define PWM_PIN 17

int main(void)
{
  // uses BCM numbering of the GPIOs and directly accesses the GPIO registers.
  wiringPiSetupGpio();

  softPwmCreate(17, 0, 100);

  while (true) {
    for (int i = 0; i <= 100; i++) {
      softPwmWrite(17, i);
      delay(10);
    }
    for (int i = 100; i >= 0; i--) {
      softPwmWrite(17, i);
      delay(10);
    }
  }

  return 0;
}