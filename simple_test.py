

from machine import I2C, Pin
from math import sqrt, atan2, pi, copysign, sin, cos
from mpu9250 import MPU9250
from time import sleep

# addresses 
MPU = 0x68
id = 0
sda = Pin(0)
scl = Pin(1)

# 
# create the I2C
i2c = I2C(id=id, scl=scl, sda=sda)

# Scan the bus
print(i2c.scan())
m = MPU9250(i2c)

while True:
    print("x", m.acceleration[0],"y", m.acceleration[1], "z", m.acceleration[2])
