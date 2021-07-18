import cv2
import os
from keras.models import load_model
import numpy as np
from pygame import mixer
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from twilio.rest import Client
from tkinter import *
window = Tk()
window.geometry("400x400")
def getval():
    mixer.init()
    sound = mixer.Sound('alarm.wav')
    face = cv2.CascadeClassifier('haar cascade files\haarcascade_frontalface_alt.xml')
    leye = cv2.CascadeClassifier('haar cascade files\haarcascade_lefteye_2splits.xml')
    reye = cv2.CascadeClassifier('haar cascade files\haarcascade_righteye_2splits.xml')
    model = load_model('models/datamodel.h5')
    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    count=0
    value=0
    rpred=[99]
    lpred=[99]
    while(True):
        ret, frame = cap.read()
        height,width = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face.detectMultiScale(gray,minNeighbors=5,scaleFactor=1.1,minSize=(25,25))
        left_eye = leye.detectMultiScale(gray)
        right_eye =  reye.detectMultiScale(gray)
        cv2.rectangle(frame, (0,height-50) , (200,height) , (0,0,0) , thickness=cv2.FILLED )
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y) , (x+w,y+h) , (100,100,100) , 1 )
        for (x,y,w,h) in right_eye:
            r_eye=frame[y:y+h,x:x+w]
            count=count+1
            r_eye = cv2.cvtColor(r_eye,cv2.COLOR_BGR2GRAY)
            r_eye = cv2.resize(r_eye,(24,24))
            r_eye= r_eye/255
            r_eye=  r_eye.reshape(24,24,-1)
            r_eye = np.expand_dims(r_eye,axis=0)
            rpred = model.predict_classes(r_eye)
            break
        for (x,y,w,h) in left_eye:
            l_eye=frame[y:y+h,x:x+w]
            count=count+1
            l_eye = cv2.cvtColor(l_eye,cv2.COLOR_BGR2GRAY)
            l_eye = cv2.resize(l_eye,(24,24))
            l_eye= l_eye/255
            l_eye=l_eye.reshape(24,24,-1)
            l_eye = np.expand_dims(l_eye,axis=0)
            lpred = model.predict_classes(l_eye)
            break
        if(rpred[0]==0 and lpred[0]==0):
            value=value+1
            # detected closed eyes so labeling 'Closed'.
            cv2.putText(frame,"Closed",(10,height-20), font, 1,(255,255,255),1,cv2.LINE_AA)
        else:
            value=value-1
            # when  eyes are open.
            cv2.putText(frame,"Open",(10,height-20), font, 1,(255,255,255),1,cv2.LINE_AA)
        # check if driver has been driving for more than 4 hours(14400 seconds) continuously through runtime.
        if time.perf_counter()>14400:
            cv2.putText(frame, "You have been driving for long time, take rest.", (10, height - 40), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
            # notify driver to take rest.
            mixer.Sound('takerest.wav').play()
        if(value<0):
            value=0
        cv2.putText(frame,'Value:'+str(value),(100,height-20), font, 1,(255,255,255),1,cv2.LINE_AA)
        if(value>15):
        # driver's eyes are closed so start alarm.
            try:
                sound.play()
            except:
                pass
            #  if driver still doesn't open eyes. Start location driver.
            if value>30:
                options = Options()
                options.add_argument("--use-fake-ui-for-media-stream")
                timeout = 20
                driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=options)
                driver.get("https://mycurrentlocation.net/")
                wait = WebDriverWait(driver, timeout)
                time.sleep(3)
                longitude = driver.find_elements_by_xpath('//*[@id="longitude"]')
                longitude = [x.text for x in longitude]
                longitude = str(longitude[0])
                latitude = driver.find_elements_by_xpath('//*[@id="latitude"]')
                latitude = [x.text for x in latitude]
                latitude = str(latitude[0])
                driver.quit()
                # send location message through API.
                client = Client("ACbc59b6e25fda32fdf5436fb82f0dd1bc", "64435dec641b1a3d3c7306af29681d1a")
                client.messages.create(to="+916264670065",from_="+14178150473",body="person is in sleep while driving. The location details are: "+"[ "+latitude+" , "+longitude+" ]")
        else:
            # driver's eyes are open so stop alarm.
            sound.stop()
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            #  user pressed 'q' so stop the program.
            break
    cap.release()
    cv2.destroyAllWindows()

Label(window,text="Welcome to the Sleep Detection Program").grid(row=0,column=0)
Label(window,text="Instructions:").grid(row=1,column=0)
Label(window,text="1. Press the below button to get started. To exit anytime press 'q'.", justify=LEFT).grid(row=2,column=0)
Label(window,text="2. When turned on the program will capture your face continuously. ", justify=LEFT).grid(row=3,column=0)
Label(window,text="3. We have a value that will start increasing if you close your eye.", justify=LEFT).grid(row=4,column=0)
Label(window,text="4. If eyes are closed for more than 15 value system will beep alarm.", justify=LEFT).grid(row=5,column=0)
Label(window,text="5. If value increases above 30 system will send your location detail\nto the programmed number.", justify=LEFT).grid(row=6,column=0)
Label(window,text="6. When you open your eyes value decreases automatically.           ", justify=LEFT).grid(row=7,column=0)
Label(window,text="7. Driving for a long time is not healthy. We will notify you to rest\nwhen you have driven continuously for 4 hours.", justify=LEFT).grid(row=8,column=0)
Button(window, text="Turn on", command=getval).grid(row=9, column=0)
window.mainloop()