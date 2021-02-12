import pigpio

print("Don't forget to start with sudo pigpiod")

pi = pigpio.pi()

pi.set_PWM_dutycycle(18, 128)
