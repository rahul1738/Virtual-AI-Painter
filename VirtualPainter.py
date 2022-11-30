import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

#######################
brushThickness = 15
eraserThickness = 50
#######################

folderPath = "HeaderFiles"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))
header = overlayList[0]
drawColor = (255, 0, 255)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector= htm.handDetector(detectionCon=0.85)
xp, yp= 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)
while True:
    #1.Import image
    success, img = cap.read()
    img = cv2.flip(img,1)



    #2.Find Hand Landmark`s
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList)!=0:

        # print(lmList)
        #tip of index and middle fingers

        x1,y1= lmList[8][1:]
        x2, y2 = lmList[12][1:]




        #3. Check which fingers are up

        fingers=detector.fingersUp()
        # print(fingers)


        #4. If selection mode- Two Fingers are up
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            print("Selection Mode")
            # checking for the click
            if y1 < 126:
                if 220< x1 < 320:
                    header= overlayList[0]
                    drawColor=(255, 0, 255)
                elif 330<x1<450:
                    header= overlayList[1]
                    drawColor = (255, 255, 0)
                elif 470<x1<600:
                    header= overlayList[2]
                    drawColor = (0, 255, 0)
                elif 630<x1<890:
                    header= overlayList[3]
                    drawColor = (0, 170, 210)

                elif 900<x1<1050:
                    header= overlayList[4]
                    drawColor = (0, 0, 255)

                elif 1060<x1<1280:
                    header= overlayList[5]
                    drawColor = (0, 0, 0)

            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)


        #5. If Drawing Mode- Index finger is up
        if fingers[1] and fingers[2]== False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp==0 and yp==0:
                xp, yp = x1, y1
            if drawColor==(0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img ,(xp,yp),(x1,y1),drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)




    #setting the header image
    img[0:126,0:1280]= header

    cv2.imshow("Image",img)
    # cv2.imshow("Canvas", imgCanvas)
    # cv2.imshow("Inv", imgInv)
    if cv2.waitKey(1)== ord('d'):
        break




