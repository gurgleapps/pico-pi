#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"

#define BUTTON_PIN 16
#define LED_PIN 25

int main() {
    stdio_init_all();
    printf("GurgleApps.com Button Test\n");
    gpio_init(BUTTON_PIN);
    gpio_set_dir(BUTTON_PIN, GPIO_IN);
    gpio_pull_down(BUTTON_PIN);
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    while (true) {
        if (!gpio_get(BUTTON_PIN)) {
            gpio_put(LED_PIN, 0);
        } else {
            gpio_put(LED_PIN, 1);
        }
        sleep_ms(250);
    }
}