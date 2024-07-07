import tracestack
from math import *
import math
from cProfile import label
import tkinter as tk 
from tkinter import *
from tkinter import ttk
from turtle import left, update 
from PIL import ImageTk, Image
import cv2
from matplotlib import image
import numpy as np
import mediapipe as mp
import time, datetime  #for delay functions
import microcontroller as mic
from ctypes.wintypes import RGB
from tkinter import filedialog

window = Tk()

window.title("RoboCar control using Hand Gestures")
# bg="C:/Users/DELL/Pictures/Saved Pictures/pxfue.jpg"
window.configure(bg = "skyblue")

titleba = Label(window, text="Hand Gestured control RC car", font=("Calibri",30), bg="black", 
            fg="white", relief=GROOVE).place(relx=0.5,rely=0.1, anchor ="center")

f1= LabelFrame(window, bg="red").place(relx=0.5,rely=0.5) #this is vid background
L1 = Label(f1, height = 600 , width = 660 ,bg="white")
L1.place(relx=0.5,rely=0.5, anchor = 'center') #ive placed it in center and u can change color too

Label(window,text="Choose your video:",font=("Calibri",25),bg="black",fg="white").place(relx=0.05,rely=0.2) # here is the label corner

v=StringVar()
str(v.get())

VIDEOS=[("Play vid1","VID_2.mp4",0.05,0.3),
        ("Play vid2","RoboCar control using Hand Gestures 2023-05-13 14-06-06.mp4",0.05,0.35)]


Label(window,text="2021-MC-10 M. Sufyan ",font=("Calibri",20),bg="black",fg="white").place(relx=0.75,rely=0.2)
Label(window,text="2021-MC-17 Hammad Sajjad",font=("Calibri",20),bg="black",fg="white").place(relx=0.75,rely=0.25)
#---------------------
vidadd=StringVar() # will have to make a function with main loop so it doesnt crash, chech izzi;s code
vidadd.set("VID_2.mp4") #setting default video
livevar=IntVar() #variable for live vid too, this depends on ur computer camera
livevar.set(0)

#---------------------this is for selecting vid
def video_click(address):
    global cap
    #Label(win,text=address).place(x=700,y=500) # To check adress
    if address==0:
        cap = cv2.VideoCapture(0)
        vidadd.set(" ")
    else:
        vidadd.set(address)
        cap = cv2.VideoCapture(vidadd.get())

# # global direction
# direction = 'Up'

# for our radiobuttton
for name,address,x,y in VIDEOS:
    Radiobutton(window,text=name,variable=vidadd,value=address).place(relx=x,rely=y)

# Live and Recorded video switching and placement   
Button(window,text="Select",bg="white",command=lambda:video_click(vidadd.get())).place(relx=0.05,rely=0.45)
Button(window,text="Open Webcam",bg="black",fg="white",command=lambda:video_click(livevar.get())).place(relx=0.05,rely=0.5)

#------------------for destroying windows
def close():
    window.destroy()
#exit button 
Button(f1, text="Exit the Application", bg='white', fg='black', font=("Calibri", 14, "bold"), command=close).place(relx=0.11, rely=0.8, anchor ="center")
#------------------
mp_draw=mp.solutions.drawing_utils
mp_hand=mp.solutions.hands

tipIds=[4,8,12,16,20]
hands = mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture("VID_2.mp4")


def Video():

    ret,img=cap.read()
    img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results=hands.process(img)
    img.flags.writeable=True
    
    lmList=[]
    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            myHands=results.multi_hand_landmarks[0]
            for id, lm in enumerate(myHands.landmark):
                h,w,c=img.shape
                cx,cy= int(lm.x*w), int(lm.y*h)
                lmList.append([id,cx,cy])
            mp_draw.draw_landmarks(img, hand_landmark, mp_hand.HAND_CONNECTIONS)
    if len(lmList) >= 3:
        p1 = lmList[0]
        p2 = lmList[1]
        p3 = lmList[2]

        # Calculate the angle
        angle = calculate_angle(p1, p2, p3)
        print("Angle:", angle)
    fingers=[]
    if len(lmList)!=0:
        
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        total=fingers.count(1)

        direction = mic.RCCAR(total)

        if total==0:
        
            cv2.putText(img, "BRAKE", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                2, (255, 0, 0), 5)
            print("brake")
        

        if total==5:

            cv2.putText(img, " FORWARD", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                2, (255, 0, 0), 5)
            print("forward")

        if total==2:

            cv2.putText(img, " RIGHT", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                2, (255, 0, 0), 5)
            print("right")


        if total==3:
            
            cv2.putText(img, " LEFT", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                2, (255, 0, 0), 5)
            print("left")

        if total==4:
            
            cv2.putText(img, "REVERSE", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                2, (255, 0, 0), 5)
            print("REVERSE")


        #cv2.imshow("Frame",image)
        k=cv2.waitKey(1)
        # if k==ord('q'):
        #     break

    return img
    #####################
def calculate_angle(p1, p2, p3):
    """Calculate the angle between three landmarks."""
    x1, y1 = p1[1], p1[2]
    x2, y2 = p2[1], p2[2]
    x3, y3 = p3[1], p3[2]

    # Calculate the angle using vector operations
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    angle = round(angle, 2)

    # Ensure the angle is positive
    if angle < 0:
        angle += 360

    return angle

def select_img():
    image = Image.fromarray(Video())
    
    finalImage = ImageTk.PhotoImage(image)
    L1.configure(image=finalImage)
    L1.image = finalImage
    window.after(1, select_img)

# Assuming you have three landmarks stored in variables p1, p2, and p3

select_img()
window.mainloop()