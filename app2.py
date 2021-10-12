import pandas as pd 
import streamlit as st
import numpy as np
from imutils.video import VideoStream
import argparse
import datetime
from datetime import datetime
import imutils
import time
import cv2

def wbs(img):
    result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    return result

def main(vidddddddddddddd):
    t1 ,t2 ,t3,t4 = 30,0,40,0
    vibbb,vibbb1,vibbb2,vibbb3 = 0,0,0,0
    # stframe1 , charr1 = st.beta_columns(2)
    stframe = st.empty()
    charr = st.empty()
    
    vs = cv2.VideoCapture(vidddddddddddddd)
    firstFrame = None
    while True:
        ret ,frame = vs.read()
        frame = wbs(frame)
        
        text = "STILL"
        vibbb = 10
        if ret is False:
            break
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        if firstFrame is None:
            firstFrame = gray
            continue
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        for c in cnts:
            if cv2.contourArea(c) < 10000: 
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "MOVING"
            vibbb = 5
        cv2.putText(frame, "Camera Status: {}".format(text), (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        #     (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        
        now = datetime.now()
        t = now.strftime("%H:%M:%S")
        df = pd.DataFrame({
        'date': [f'{t3}',f'{t2}', f'{t1}', f'{t}'],
        'second column': [ vibbb3 , vibbb2 , vibbb1 , vibbb ]
        })

        vibbb3 = vibbb2
        vibbb2 = vibbb1
        vibbb1 = vibbb
        t3 = t2
        t2 = t1
        t1 = t

        df = df.rename(columns={'date':'index'}).set_index('index')
        # cv2.imshow("Security Feed", frame)
        stframe.image(frame, channels="BGR")
        charr.line_chart(df)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray1 = cv2.GaussianBlur(gray, (21, 21), 0)
        firstFrame = gray1.copy()
    vs.release()
    cv2.destroyAllWindows()

st.header("MOTION DETECTION")

st.sidebar.success("Motion Detection APP")
st.sidebar.info("Press Run for Live Streaming")
wc = st.sidebar.button("Run")

if (wc):
    main(0)
