# Logging has been configured in PuTTY for all session output
# Simply connect to the COM port with PuTTY and the output will be logged to light.log
from machine import I2C, Pin
from micropython import const
import bh1750fvi
import utime

# Alternative driver
# from bh1750 import BH1750

# IO Pin numbers on U1 connecting to I2C0_SCL and I2C0_SDA which make up the I2C bus that the light sensor is
# connected to
I2C0_SCL = const(26)
I2C0_SDA = const(25)

scl = Pin(I2C0_SCL)
sda = Pin(I2C0_SDA)
i2c = I2C(-1, scl=scl, sda=sda)

while True:
    lux = bh1750fvi.sample(i2c)
    print(lux)
    utime.sleep(1)

# Alternative driver
# s = BH1750(i2c)
# while True:
#     print(s.luminance(BH1750.CONT_HIRES_1))
#     time.sleep(1)
