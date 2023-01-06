import cv2 as cv
import mediapipe as mp
import time 

class handDetector():
    def __init__(self, mode=False, maxHands = 2,modelComplexity = 0, detectionCon = .7, trackCons = .7):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCons
        self.modelComplex = modelComplexity
        
        self.mpHands =  mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
    
    def find_Hands(self, frame, draw = True):
        rgbFrame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(rgbFrame)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame,   handLms, self.mpHands.HAND_CONNECTIONS)
        return frame
    def find_Position(self, frame, handNo = 0, draw = True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                height, width, channel = frame.shape
                cx, cy = int(lm.x*width), int(lm.y*height)
                self.lmList.append([id, cx,cy])
        return self.lmList
    def count_Finger(self):
        tipsIds = (4,8,12,16,20)
        if len(self.lmList) != 0:
            fingers = []
            if self.lmList[tipsIds[0]][1] < self.lmList[tipsIds[0]-1][1]:
                    fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1,5):
                if self.lmList[tipsIds[id]] [2] < self.lmList[tipsIds[id]-2] [2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            return fingers
def frame_rate(initialTime):
    currentTime = time.time()
    fps = 1//(currentTime - initialTime)
    initialTime = currentTime
    return str(int(fps)), initialTime

def main():
    webCam = cv.VideoCapture(0)
    detector = handDetector()
    initialTime = 0
    try:
        while True:
            isTrue, frame= webCam.read() 
            # frame = cv.flip(frame,1) #inverting the frame
            frame = detector.find_Hands(frame)
            lmList = detector.find_Position(frame)
            if len(lmList) != 0:
                finger=detector.count_Finger()
                if finger == [0,1,1,0,0]:
                    cv.putText(frame, "Scissor", (10,400),thickness=1,color=(0,0,255), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=.5)
                elif finger == [1,1,1,1,1]:
                    cv.putText(frame, "Paper",(10,400), thickness=1,color=(0,0,255), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=.5)
                elif finger == [0,0,0,0,0]:
                    cv.putText(frame, "Rock",(10,400), thickness=1,color=(0,0,255), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=.5)
                else:
                    cv.putText(frame, "Not Define",(10,400), thickness=1,color=(0,0,255), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=.5)
                print(finger)
            else:
                cv.putText(frame, "No Hand Present", (10,400), thickness=1,color=(0,0,255), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=.5)
            fps,initialTime=frame_rate(initialTime)
            cv.putText(frame, fps, (10,70),thickness=2,color=(0,0,255),fontFace=cv.FONT_HERSHEY_TRIPLEX,fontScale=1) #put frame rate
            cv.imshow("Stone Paper Scissor", frame) #displaying the frame
            if cv.waitKey(1) & 0xFF==ord('d'):
                break
    except:
        main()
    webCam.realese()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()