import tracestack
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

def video_click():
    if 
    cap = cv2.VideoCapture(0)


def mfileopen():
    
    global file_name
    
    file1=filedialog.askopenfile()
    file_name=file1.name

def close():
    
    window.destroy()

def Video():

    lmList=[]
    
    ret,img=cap.read()
    img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results=hands.process(img)
    img.flags.writeable=True

    if results.multi_hand_landmarks:
        
        for hand_landmark in results.multi_hand_landmarks:
            
            myHands=results.multi_hand_landmarks[0]
            
            for id, lm in enumerate(myHands.landmark):
                
                h,w,c=img.shape
                cx,cy= int(lm.x*w), int(lm.y*h)
                lmList.append([id,cx,cy])
                
            mp_draw.draw_landmarks(img, hand_landmark, mp_hand.HAND_CONNECTIONS)

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
        
        if total==5:

            cv2.putText(img, " FORWARD", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                2, (255, 0, 0), 5)

        if total==2:

            cv2.putText(img, " RIGHT", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                2, (255, 0, 0), 5)

        if total==3:

            cv2.putText(img, " LEFT", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                2, (255, 0, 0), 5)

        if total==4:
            
            cv2.putText(img, "REVERSE", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                2, (255, 0, 0), 5)

        k=cv2.waitKey(1)

    return img

def select_img():
    
    image = Image.fromarray(Video())
    
    finalImage = ImageTk.PhotoImage(image)
    L1.configure(image=finalImage)
    L1.image = finalImage
    
    window.after(1, select_img)

direction = 'Up'

window = Tk()

window.title("RoboCar control using Hand Gestures")
window.configure(bg = "skyblue")

titleba = Label(window, text="Gestured control RC car", font=("Calibri",30), bg="black", 
            fg="white", relief=GROOVE).place(relx=0.5,rely=0.1, anchor ="center")

f1= LabelFrame(window, bg="red").place(relx=0.5,rely=0.5) 
L1 = Label(f1, height = 600 , width = 660 ,bg="white")
L1.place(relx=0.5,rely=0.5, anchor = 'center') 

Label(window,text="Choose your video:",font=("Calibri",25),bg="black",fg="white").place(relx=0.05,rely=0.2) 

v=StringVar()
str(v.get())

Label(window,text="2021-MC-10 M. Sufyan ",font=("Calibri",20),bg="black",fg="white").place(relx=0.75,rely=0.2)
Label(window,text="2021-MC-17 Hammad Sajjad",font=("Calibri",20),bg="black",fg="white").place(relx=0.75,rely=0.25)
#---------------------
vidadd=StringVar() # will have to make a function with main loop so it doesnt crash, chech izzi;s code
livevar=IntVar() 
livevar.set(0)

Button(window,text='Browse',bg='black',fg='white',width=10,font=('bold',15),command=mfileopen).place(relx=0.05,rely=0.31)
   
Button(window,text="Open Webcam",bg="black",fg="white",command=lambda:video_click(livevar.get())).place(relx=0.05,rely=0.5)

Button(f1, text="Exit the Application", bg='white', fg='black', font=("Calibri", 14, "bold"), command=close).place(relx=0.11, rely=0.8, anchor ="center")

mp_draw=mp.solutions.drawing_utils
mp_hand=mp.solutions.hands

tipIds=[4,8,12,16,20]

hands = mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture("handgesturevid2.mkv")

select_img()
window.mainloop()
