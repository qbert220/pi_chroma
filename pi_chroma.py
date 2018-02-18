import numpy
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

width = 640
height = 360

camera = PiCamera()
rawCapture = PiRGBArray(camera)
#time.sleep(0.1)

backgroundImage = cv2.imread('background.jpeg')
backgroundImage = cv2.resize(backgroundImage, (width, height))

#Setup window for full screen
cv2.namedWindow("Pi Chroma", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Pi Chroma", cv2.WND_PROP_FULLSCREEN,
                      cv2.WINDOW_FULLSCREEN)

fontFace = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.8
thickness = 2

cv2.imshow('Pi Chroma', backgroundImage)
key = cv2.waitKey(1000)

h_min = 50
h_max = 70
s_min = 100
s_max = 255
v_min = 80
v_max = 255

while True:

    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, format="bgr")
    foregroundImage = rawCapture.array
    foregroundImage = cv2.resize(foregroundImage, (width, height))
#    cv2.imshow('Pi Chroma', foregroundImage)
#    cv2.waitKey()

    hsvImage = cv2.cvtColor(foregroundImage, cv2.COLOR_BGR2HSV)
    backgroundMask = cv2.inRange(hsvImage, numpy.array([h_min, s_min, v_min]),
                                           numpy.array([h_max, s_max, v_max]))
    foregroundMask = cv2.bitwise_not(backgroundMask)

    maskedBackground = cv2.bitwise_and(backgroundImage, backgroundImage,
                                       mask=backgroundMask)
    maskedForeground = cv2.bitwise_and(foregroundImage, foregroundImage,
                                       mask=foregroundMask)
    img = cv2.add(maskedBackground, maskedForeground)

    text = "H {} - {}".format(h_min, h_max)
    cv2.putText(img, text, (50, 50), fontFace, fontScale,
                (255, 255, 255), thickness)
    text = "S {} - {}".format(s_min, s_max)
    cv2.putText(img, text, (50, 80), fontFace, fontScale,
                (255, 255, 255), thickness)
    text = "V {} - {}".format(v_min, v_max)
    cv2.putText(img, text, (50, 110), fontFace, fontScale,
                (255, 255, 255), thickness)

    cv2.line(img, (width / 2 - 5, height / 2),
        (width / 2 + 5, height / 2), (255, 255, 255), 1)
    cv2.line(img, (width / 2, height / 2 - 5),
        (width / 2, height / 2 + 5), (255, 255, 255), 1)
    pixel = hsvImage[height / 2][width / 2]
    text = "HSV = {} {} {}".format(pixel[0], pixel[1], pixel[2])
    img[height/2][width/2]=(0,0,255)
    cv2.putText(img, text, (50, 150), fontFace, fontScale,
                (255, 255, 255), thickness)

    cv2.imshow('Pi Chroma', img)
    key = cv2.waitKey(25)

    if key == ord('a') and h_max > 5:
        h_max -= 5
        if h_max <= h_min:
            h_min = h_max - 5
    if key == ord('s') and h_max < 180:
        h_max += 5
    if key == ord('z') and h_min > 0:
        h_min -= 5
    if key == ord('x') and h_min < 175:
        h_min += 5
        if h_max <= h_min:
            h_max = h_min + 5
    if key == ord('d') and s_max > 5:
        s_max -= 5
        if s_max <= s_min:
            s_min = s_max - 5
    if key == ord('f') and s_max < 255:
        s_max += 5
    if key == ord('c') and s_min > 0:
        s_min -= 5
    if key == ord('v') and s_min < 250:
        s_min += 5
        if s_max <= s_min:
            s_max = s_min + 5
    if key == ord('g') and v_max > 5:
        v_max -= 5
        if v_max <= v_min:
            v_min = v_max - 5
    if key == ord('h') and v_max < 255:
        v_max += 5
    if key == ord('b') and v_min > 0:
        v_min -= 5
    if key == ord('n') and v_min < 250:
        v_min += 5
        if v_max <= v_min:
            v_max = v_min + 5

    if key == 27:
        print("Exiting")
        exit(0)

    print(key)