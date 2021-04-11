'''
Author: Karim Q.
Date: 4/11/21
'''
import cv2
import math
import mediapipe
from pynput.mouse import Button, Controller

Mouse = Controller()

Acc = 0.7
HandDetection = mediapipe.solutions.hands.Hands(False, 1, Acc, Acc)
HandDrawer = mediapipe.solutions.drawing_utils
HandConnector = mediapipe.solutions.hands.HAND_CONNECTIONS
PressedLeft = False
PressedRight = False
VidCap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#Shit Camera Can't Do 1080p
VidCap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
VidCap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

def Positions(Img):
    Found = HandDetection.process(Img).multi_hand_landmarks
    Height, Width = Img.shape[:2]
    if Found:
        return [(int(pos.x*Width), int(pos.y*Height)) for pos in Found[0].landmark]
    return None

def DrawHands(Img):
    Found = HandDetection.process(Img).multi_hand_landmarks
    if Found:
        [HandDrawer.draw_landmarks(Img, i, HandConnector) for i in Found]

def DrawLines(Img, Pos):
    cv2.line(Img, (Pos[4][0], Pos[4][1]), (Pos[17][0], Pos[17][1]), (0, 0, 139), 2)
    cv2.line(Img, (Pos[12][0], Pos[12][1]), (Pos[0][0], Pos[0][1]), (139, 0, 0), 2)

def DrawPressedLeft(Img, Pos):
    cv2.line(Img, (Pos[4][0], Pos[4][1]), (Pos[17][0], Pos[17][1]), (0, 0, 255), 6)

def DrawPressedRight(Img, Pos):
    cv2.line(Img, (Pos[12][0], Pos[12][1]), (Pos[0][0], Pos[0][1]), (255, 0, 0), 6)

while True:
    Check, Cap = VidCap.read()
    Cap = cv2.flip(Cap, 1)
    Cap = cv2.resize(Cap, (1920, 1080))

    Pos = Positions(Cap)
    DrawHands(Cap)

    if Pos: 
        DrawLines(Cap, Pos)

        DistLeftClick = int(math.hypot(Pos[17][0]-Pos[4][0], Pos[17][1]-Pos[4][1]))
        DistRightClick = int(math.hypot(Pos[0][0]-Pos[12][0], Pos[0][1]-Pos[12][1]))

        Mouse.position = Pos[8]

        if DistLeftClick>95:
            if PressedLeft:
                Mouse.release(Button.left)
                PressedLeft = False
        else:
            if not PressedLeft:
                Mouse.press(Button.left)
                PressedLeft = True
            DrawPressedLeft(Cap, Pos)
        if DistRightClick>210:
            if PressedRight:
                Mouse.release(Button.right)
                PressedRight = False
        else:
            if not PressedRight:
                Mouse.press(Button.right)
                PressedRight = True
            DrawPressedRight(Cap, Pos)
        
        print(DistLeftClick, DistRightClick)

    cv2.imshow("Rec...", Cap)
    cv2.waitKey(1)
