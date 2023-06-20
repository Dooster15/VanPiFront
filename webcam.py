import numpy as np
import cv2 as cv
import time
while True:
    try:
        cap = cv.VideoCapture(0)
        # Define the codec and create VideoWriter object
        fourcc = cv.VideoWriter_fourcc(*'XVID')
        #out = cv.VideoWriter('output.avi', fourcc, 20.0, (640,  480))
        while cap.isOpened():
            start = time.time()
            ret, frame = cap.read()
            end = time.time()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            
            # write the flipped frame
            start1 = time.time()
            #out.write(frame)
            frame = frame[200:400,0:640]
            frame = cv.flip(frame, 1)
            frame = cv.resize(frame,(0, 0),fx=2, fy=2, interpolation = cv.INTER_NEAREST)
            end1 = time.time()
            start2 = time.time()
            cv.imshow('frame', frame)
            end2 = time.time()
            if cv.waitKey(1) == ord('q'):
                break
            end3 = time.time()
            print(f"time0: {end-start},time1: {end1-start1},time2: {end2-start2},timeTotal: {end3-start}")
        # Release everything if job is finished
        cap.release()
        #out.release()
    except:
        time.sleep(1)
        pass