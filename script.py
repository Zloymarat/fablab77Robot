import numpy as np
import cv2

pi = None
try:
    import pigpio
    print("Don't forget to start with sudo pigpiod")

    pi = pigpio.pi()
except:
    print('Sorry, no raspberries here')


#GPIO pin 12 = BCM pin 18 = wiringpi pin 1 
led_pin = 18


faceCascade = cv2.CascadeClassifier('haar.xml')

cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

while True:
    ret, img = cap.read()
    img = cv2.flip(img, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))

    if pi:
        pi.set_PWM_dutycycle(led_pin, len(faces) * 16)
        pi.set_PWM_frequency(4,600)
        pi.set_PWM_dutycycle(4, 128 if len(faces) > 0 else 0)
    
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]  

    cv2.imshow('video',img)

    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break

if pi:
    pi.set_PWM_dutycycle(led_pin, 0)
    pi.set_PWM_dutycycle(4, 0)
cap.release()
cv2.destroyAllWindows()
