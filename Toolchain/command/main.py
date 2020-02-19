from machine import Pin, PWM
import time
import sys

# The Azure LED is on pin IO33
LED_AZURE = 33
led = Pin(LED_AZURE, Pin.OUT)

# The piezo speaker (buzzer) is on pin IO27
BUZ_IO27 = 27
buzzer = Pin(BUZ_IO27, Pin.OUT)

# Must match PC connection
# For some reason I could not make this work
# uart = UART(2)
# uart.init(baudrate=115200, bits=8, parity=0, stop=1, timeout=1000, timeout_char=100)


def flash(n=3):
    for i in range(n):
        led.on()
        time.sleep(0.2)
        led.off()
        time.sleep(0.2)


def beep(tone=440):
    beeper = PWM(buzzer, freq=tone, duty=512)
    time.sleep(0.5)
    beeper.deinit()


flash()
while True:
    # Read one command from the sender
    msg = sys.stdin.readline()

    if msg != "":
        if msg == "on\n":
            led.on()
        elif msg == "off\n":
            led.off()
        elif msg == "beep\n":
            beep()
        else:
            flash()
