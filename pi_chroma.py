import numpy
import cv2
import time

backgroundImage = cv2.imread('background.jpeg')
backgroundImage = cv2.resize(backgroundImage, (640, 360))

foregroundImage = cv2.imread('image.jpeg')

#Setup window for full screen
cv2.namedWindow("Pi Chroma", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Pi Chroma", cv2.WND_PROP_FULLSCREEN,
                      cv2.WINDOW_FULLSCREEN)

fontFace = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
thickness = 3

cv2.imshow('Pi Chroma', backgroundImage)
cv2.waitKey()

cv2.imshow('Pi Chroma', foregroundImage)
cv2.waitKey()

h_min = 50
h_max = 70
s_min = 100
s_max = 255
v_min = 100
v_max = 255

while True:

    hsvImage = cv2.cvtColor(foregroundImage, cv2.COLOR_BGR2HSV)
    backgroundMask = cv2.inRange(hsvImage, numpy.array([h_min, s_min, v_min]),
                                           numpy.array([h_max, s_max, v_max]))
    foregroundMask = cv2.bitwise_not(backgroundMask)

    maskedBackground = cv2.bitwise_and(backgroundImage, backgroundImage,
                                       mask=backgroundMask)
    maskedForeground = cv2.bitwise_and(foregroundImage, foregroundImage,
                                       mask=foregroundMask)
    img = cv2.add(maskedBackground, maskedForeground)

    text = "{} - {}".format(h_min, h_max)
    cv2.putText(img, text, (50, 50), fontFace, fontScale,
                (255, 255, 255), thickness)
    text = "{} - {}".format(s_min, s_max)
    cv2.putText(img, text, (50, 100), fontFace, fontScale,
                (255, 255, 255), thickness)
    text = "{} - {}".format(v_min, v_max)
    cv2.putText(img, text, (50, 150), fontFace, fontScale,
                (255, 255, 255), thickness)

    cv2.imshow('Pi Chroma', img)
    key = cv2.waitKey()

    if key == ord('a'):
        h_max -= 5
    if key == ord('s'):
        h_max += 5
    if key == ord('z'):
        h_min -= 5
    if key == ord('x'):
        h_min += 5
    if key == ord('d'):
        s_max -= 5
    if key == ord('f'):
        s_max += 5
    if key == ord('c'):
        s_min -= 5
    if key == ord('v'):
        s_min += 5
    if key == ord('g'):
        v_max -= 5
    if key == ord('h'):
        v_max += 5
    if key == ord('b'):
        v_min -= 5
    if key == ord('n'):
        v_min += 5

    if key == 27:
        print("Exiting")
        exit(0)

    print(key)