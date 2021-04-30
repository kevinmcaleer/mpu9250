from machine import I2C, Pin
from math import sqrt, atan2, pi, copysign
from mpu9250 import MPU9250
from time import sleep

# addresses 

MPU = 0x68

id = 0
sda = Pin(0)
scl = Pin(1)

i2c = I2C(id=id, scl=scl, sda=sda)

print(i2c.scan())
m = MPU9250(i2c)

acc_x = m.acceleration[0]
acc_y = m.acceleration[1]
acc_z = m.acceleration[2]

print(acc_x, acc_y, acc_z)

# scaling_gyro = 131
# scaling_acc = 16384
# scaling_mag = 0.6
# scaling_temp = 321
# offset_temp = 800

# Bias

# prin /t(acc_x_new_bias, acc_y_new_bias, acc_z_new_bias)
m.ak8963.calibrate(count=10)

acc_x = m.acceleration[0]
acc_y = m.acceleration[1]
acc_z = m.acceleration[2]
acc_x_bias = acc_x
acc_y_bias = acc_y
acc_z_bias = acc_z

def get_reading():
    x = m.acceleration[0]
    y = m.acceleration[1]
    z = m.acceleration[2]
    # acc_x_new_bias = (acc_x_bias - acc_x)
    # acc_y_new_bias = (acc_y_bias - acc_y)
    # acc_z_new_bias = (acc_z_bias - acc_z)

    roll_rad = atan2(-x, sqrt((z*z)+(y*y)))
    pitch_rad = atan2(z, copysign(y,y)*sqrt((0.01*x*x)+(y*y)))

    pitch_degree = pitch_rad*180/pi
    roll_degree = roll_rad*180/pi
    # x = acc_x_new_bias
    # y = acc_y_new_bias
    # z = acc_z_new_bias
    pitch = pitch_degree
    roll = roll_degree
    return x, y, z, pitch, roll 

while True:
    # print(m.magnetic)
    x, y, z, pitch, roll = get_reading()
    print("Pitch",round(pitch,1), "Roll",round(roll, 1))
    sleep(0.2)
