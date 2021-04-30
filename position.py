from mpu9250 import MPU9250
from machine import I2C, Pin
from time import sleep, time_ns as time
from math import degrees, cos, sin, radians, atan2

id = 0
sda = Pin(0)
scl = Pin(1)

i2c = I2C(id=id, scl=scl, sda=sda)

print(i2c.scan())
m = MPU9250(i2c)

print("Calibrating")
m.ak8963.calibrate()
print("Calibration complete.")

# data variables
poll_interval = 0.1
roll = 0.0
pitch = 0.0
yaw = 0.0
heading = 0.0
roll_rate = 0.0
pitch_rate = 0.0
yaw_rate = 0.0
magnetic_deviation = -48

# Dampening Variables
roll_total = 0.0
roll_run = [0] * 10
heading_cos_total = 0.0
heading_sin_total = 0.0
heading_cos_run = [0] * 30
heading_sin_run = [0] * 30

# timers
timer_one = 0
timer_three = 0
timer_print = time()
timer_damp = time()

while True:
    output = time()
    if (output - timer_damp) > .1:
        roll = round(degrees(m.acceleration[0]),1)
        pitch = round(degrees(m.acceleration[1]),1)
        yaw = round(degrees(m.acceleration[2]),1)
        roll_rate = round(degrees(m.gyro[0]),1)
        pitch_rate = round(degrees(m.gyro[1]),1)
        yaw_rate = round(degrees(m.gyro[2]),1)

        if yaw < 90.1:
            heading = yaw + 270 - magnetic_deviation
        else:
            heading = yaw - 90 - magnetic_deviation
        if heading > 360.0:
            heading = heading - 360.0

        # dampening functions
        roll_total = roll_total - roll_run[timer_one]
        roll_run[timer_one] = roll
        roll_total = roll_total + roll_run[timer_one]
        roll = roll_total / 10
        heading_cos_total = heading_cos_total - heading_cos_run[timer_three]
        heading_sin_total = heading_sin_total - heading_sin_run[timer_three]
        heading_cos_run[timer_three] = cos(radians(heading))
        heading_sin_run[timer_three] = sin(radians(heading))
        heading_cos_total = heading_cos_total + heading_cos_run[timer_three]
        heading_sin_total = heading_sin_total + heading_sin_run[timer_three]
        heading = round(degrees(atan2(heading_sin_total/30, heading_cos_total/30)),1)
        if heading < 0.1:
            heading = heading + 360.0
        
        timer_damp = output
        timer_one += 1
        if timer_one == 10:
            timer_one = 0
        timer_three += 1
        if timer_three == 30:
            timer_three = 0
        
        timer_print = output
        sleep(poll_interval*1.0/1000.0)

        # print("acceleration",m.acceleration, "heading", m.magnetic, "gyro", m.gyro)
        print("heading", heading, "roll", roll, "pitch", pitch,"yaw",yaw)
