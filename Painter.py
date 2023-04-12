import os
import cv2 as cv
import numpy as np
import HandTrackingModule as htm

capture = cv.VideoCapture(0)
capture.set(3, 1280)
capture.set(4, 720)

detector = htm.handDetector(detectCon = 0.7)

#############
brushThickness = 10
drawColor = (0,0,255)
xp, yp = 0,0
draw = True
rectCoord1, rectCoord2 = (0,0), (0,0)
rectFlag = 1
#############

rootPath = "Select"
myList = os.listdir(rootPath)
overlayList = []

for imgPath in myList:
    imgArray = cv.imread(f"{rootPath}/{imgPath}")
    overlayList.append(imgArray)

tipLids = [4, 8, 12, 16, 20]
header = overlayList[1]

canvas = np.zeros((720, 1280,3), dtype = "uint8")

while True:
    #1. Read Image
    isTrue, img = capture.read()
    img = cv.flip(img, 1)

    img = cv.GaussianBlur(img, (3,3), cv.BORDER_DEFAULT)
    #img = cv.Canny(img, 125, 175)
    
    #2. Landmarks detection
    img = detector.findHands(img, draw = True)
    #3. Authenticity of Fingers
    lmList = detector.findPos(img, draw = False)
    if len(lmList):
        #Index and Middle Finger landmarks
        indexX, indexY = lmList[8][1:]
        middleX, middleY = lmList[12][1:]

        fingers = detector.fingersUp() 
    #4. Two Fingers Up: Selection Mode or Pointing Finger Up: Drawing Mode or nothing 
        if fingers[1]:
            if fingers[2]:
                xp, yp = indexX, indexY
                cv.rectangle(img, (indexX, indexY-25), (middleX, middleY+25), (0,255,255), cv.FILLED)
                #Checking for the click
                if middleY >= 570:
                    draw = True
                    brushThickness = 10
                    if 0 <= indexX < 75:
                        header = overlayList[0]
                    elif 75 <= indexX < 225:
                        header = overlayList[1]
                        drawColor = (0,0,255)
                    elif 225 <= indexX < 375:
                        header = overlayList[2]
                        drawColor = (0,255,0)
                    elif 375 <= indexX < 525:
                        header = overlayList[3]
                        drawColor = (255,0,0)
                    elif 525 <= indexX < 675:
                        header = overlayList[4]
                        drawColor = (255,255,255)
                    elif 675 <= indexX < 825:
                        header = overlayList[5]
                        draw = False
                        canvas = np.zeros((720, 1280, 3), dtype = "uint8")
                        """if (abs(indexX - middleX) < 50) or (abs(indexY - middleY)< 50):
                            if fingers[3]:
                                if rectFlag:
                                    rectCoord1 = indexX, indexY
                                    rectFlag = 0
                                else:
                                    rectCoord2 = indexX, indexY
                                cv.rectangle(canvas, rectCoord1, rectCoord2, drawColor, cv.FILLED)
                        """
                    elif 825 <= indexX < 975:
                        header = overlayList[6]
                        draw = False
                    elif 975 <= indexX < 1125:
                        header = overlayList[7]
                        drawColor = (0,0,0)
                        brushThickness = 50
                    elif 1125 <= indexX <= 1280:
                        header = overlayList[8]
                        draw = False
            else:
                if xp == 0 and yp == 0:
                    xp, yp = indexX, indexY
                #else:
                    #xp, yp = indexX, indexY
                if draw:
                    cv.circle(img, (indexX, indexY), 15, (0, 255, 255), cv.FILLED)    
                    cv.line(img, (xp, yp), (indexX, indexY), drawColor, brushThickness)
                    cv.line(canvas, (xp, yp), (indexX, indexY), drawColor, brushThickness)
                    xp, yp = indexX, indexY


    gray = cv.cvtColor(canvas, cv.COLOR_BGR2GRAY)
    _, imgInverse = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV)
    imgInverse = cv.cvtColor(imgInverse, cv.COLOR_GRAY2BGR)

    img = cv.bitwise_and(img, imgInverse)
    img = cv.bitwise_or(img, canvas)
    
    img[570: 720, 0:1280] = header
    key = 0xFF
    if cv.waitKey(10) & key == 27:
        break
    cv.imshow("Video", img)
    cv.waitKey(1)
