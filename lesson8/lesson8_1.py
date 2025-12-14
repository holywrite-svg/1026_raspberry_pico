from machine import Pin
import time
led_pin = 15
led = Pin(led_pin,Pin.OUT)
while True:
    led.toggle()
    time.sleep(0.1)
