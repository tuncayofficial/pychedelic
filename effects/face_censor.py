import cv2 as cv
import numpy as np
import time

from processors.face_detection import FateDetector

faceDetector = FateDetector()

class FaceBlur:
    
    def __init__(self):
        self.name = "FaceBlur Effect"

        self.frames = []
        self.processed_frames = []

        self.complexities = []
        self.threshold = None

        self.start_time = time.time()

    def add_frame(self, frame):
        self.frames.append(frame)
        complexity = self.calculate_complexity(frame)
        self.complexities.append(complexity)

        if len(self.complexities) > 10 and self.threshold == None:
            self.threshold = np.mean(self.complexities)
            print("Current Tracker threshold has set to " + str(self.threshold))

    def calculate_complexity(self, frame):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        variance = np.var(gray)

        return np.log1p(variance)

    def process_current_frame(self, frame, complexity):
        faces = faceDetector.detect(frame)

        for (x,y,h,w) in faces:    
            first_pixel = frame[y, x].copy()
            #frame[y:y+h, x:x+w] = first_pixel
            frame[y:y+h, x:x+w] = cv.blur(frame[y:y+h, x:x+w], ((20, 80)))

        return frame

    