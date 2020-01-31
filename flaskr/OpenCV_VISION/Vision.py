import cv2
import sys
import requests

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# To capture video from webcam. 
cap = cv2.VideoCapture(0)
# To use a video file as input 
# cap = cv2.VideoCapture('filename.mp4')
old_faces = 0
count = 0
img = 0
frame = img
url = 'http://127.0.0.1:5000/api/get_name'

while True:
    # Read the frame
    _, img = cap.read()
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if old_faces != len(faces) and len(faces) != 0:
       count+=1
    else:
        count = 0
      
    if count > 8:#se per 8 frame riconosco un cambio nel numero di  facce
       old_faces = len(faces)
       imencoded = cv2.imencode(".jpg", frame)[1]
       body = str(imencoded)
       print('send')
       x = requests.post(url, data = body)
       count = 0


    print(len(faces))
    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # Display
    cv2.imshow('img', img)
    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k==8:
        break
# Release the VideoCapture object
cap.release()