import cv2 as cv
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode = False, maxhands = 2, modelComplexity = 1, detectCon = 0.5, trackCon = 0.5):
        '''
        Mode: False, Detect and Track if confidence is high True, 
        Detect and Track even with low confidence 
        maxhands = 2
        minimum detection confidence = 0.5
        minimum tracking confidence = 0.5
        '''

        self.mode = mode
        self.maxhands = maxhands
        self.detectCon = detectCon
        self.trackCon = trackCon
        self.modelComplex = modelComplexity
        self.tipLids = [4, 8, 12, 16, 20]

        #initialize the mediapipe module for hand tracking module
        self.myHands = mp.solutions.hands
        #Parameters includes static_image_mode = | False ---> just detection (tracks if confidence is high) | True ---> Detect and Track |
        #max_num_hands = maximum number of hands that can be detected
        self.hands = self.myHands.Hands(self.mode, self.maxhands, self.modelComplex,  self.detectCon, self.trackCon)
        #Helps in drawing the landmarks in the image (which may be tedious task for us to calculate and draw on the image)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw = True):
        #convert image from BGR Channel to RGB Channel for mediapipe
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        #Process the image and in return gives the object containing handlandmarks
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for self.handlmks in self.results.multi_hand_landmarks:
                    if draw:
                        self.mpDraw.draw_landmarks(img, self.handlmks, self.myHands.HAND_CONNECTIONS)
        return img

    def findPos(self, img, handNo = 0, draw = True ):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            #List of lm of particular hand
            myhand = self.results.multi_hand_landmarks[handNo]
            for ID, LM in enumerate(self.handlmks.landmark):
                h, w, c = img.shape
                cx, cy = int(LM.x*w), int(LM.y*h)
                self.lmList.append([ID, cx, cy])
                #if draw:
                    #cv.circle(img, (cx, cy), 7, (100, 0, 0), cv.FILLED)
        return self.lmList

    def fingersUp(self):
        fingers = []

        #Thumb
        if self.lmList[self.tipLids[0]][1] > self.lmList[self.tipLids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for ID in range(1,5):
            if self.lmList[self.tipLids[ID]][2] < self.lmList[self.tipLids[ID]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
            
                       
        
                

#if hands.process returns the landmarks then draw the landmarks on the image    
#NOTE 1
# Goes each of the objects and check the ID (to identify the different points of the hand)  LM (contains the landmark ratio of the points)
#LM contains x and y coordinate ration which must be multiplied with the width and height of the image

def main():
    #Access to the webcam
    video = cv.VideoCapture(0)
    #FPS: Frames Per Second
    pTime = 0
    cTime = 0
    fps = 0
    detector = handDetector()
    while True:
        #read the image from camera
        success, img = video.read()
        img = detector.findHands(img, True)
        posList = detector.findPos(img)
        if len(posList)!=0:
            print(posList)
        #Calculate the FPS with the help of current time and previous time
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        #display fps on the image:  image   text    font    scale   color   thickness
        cv.putText(img, str(int(fps)), (10,50), cv.FONT_HERSHEY_PLAIN, 3,
                   (0, 255, 255), 3)
        
        #displaying the image with landmarks of hand processed by mediapipe
        cv.imshow("Image", img)
        cv.waitKey(1)

if __name__ == "__main__":
    main()
























