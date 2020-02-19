import machine
import time

# The Azure LED is on pin IO33
LED_AZURE = 33
led = machine.Pin(LED_AZURE, machine.Pin.OUT)

for i in range(10):
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)
