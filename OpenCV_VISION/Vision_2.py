import asyncio
import cv2
import sys
import requests
import json
import PySimpleGUI as sg
import threading
import vlc, easygui


# Create a single vlc.Instance() to be share by (possible) multiple players.
Users_Time_Saved ={  "User1" : {
                        "name" : "",
                        "name_FILM" : "",
                        "minute" : 0
                    },
                    "User2" : {
                        "name" : "",
                        "name_FILM" : "",
                        "minute" : 0
                    },
                    "User3" : {
                        "name" : "",
                        "name_FILM" : "",
                        "minute" : 0
                    },
                    "User4" : {
                        "name" : "",
                        "name_FILM" : "",
                        "minute" : 0
                    },
                    }
Num_Faces = 0


def Vision_LOOP():
        # Load the cascade
    name = ""
    print("ciao2")
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
    addr = 'http://localhost:5000'
    test_url = addr + '/api/get_name'

    # prepare headers for http request
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}
    #global name = ''
    names = ['','','','','','','','','','','']
    print("cai")
    while True:
        # Read the frame
        _, img = cap.read()
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        Num_Faces = len(faces)
    
        if old_faces != len(faces) and len(faces) != 0:
            count+=1
        else:
            count = 0
        # Draw the rectangle around each face
        print(len(faces))
        if len(faces) == 0:
            old_faces = 0
            for i in range(0, len(names)):
                names[i] = ''
    
        i = 0
        for (x, y, w, h) in faces:
            rect = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            font = cv2.FONT_HERSHEY_PLAIN
            if count > 10:#se per 10 frame riconosco un cambio nel numero di  facce
                # encode image as jpeg
                count = 0
                old_faces = len(faces)
                _, img_encoded = cv2.imencode('.jpg', img)
                # send http request with image and receive response
                response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
              #  decode response
                print(json.loads(response.text))
                if 'User Not Found' in json.loads(response.text):
                    old_faces = 0#obbligo a riprovare
                    count = 11

                name = json.loads(response.text)
                print("il nome e':", name)
            if len(name) < 4:
                for t in range(0, len(name)):
                    names[t] = name[t]
                    Users_Time_Saved['User1']['name'] = name[t] #Salvo nella struttura condivisa 

        cv2.putText(img,names[i],(x, y-10), font, 2,(255,255,255),2,cv2.LINE_AA)
        i = i + 1

        cv2.imshow('img', img)
        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k==8:
            break
    # Release the VideoCapture object
    cap.release()
 
def VLC_LOOP():
    Users_Time_Saved['User1']['name_FILM'] = "./File_Video_2.mp4"
    Users_Time_Saved['User1']['name'] = "Dave" 
    if Users_Time_Saved['User1']['name'] != '' and  Users_Time_Saved['User1']['name_FILM'] != '' :
        #se l'utente e' stato riconosciuto e il nome preso dal database
        Film_Name =  Users_Time_Saved['User1']['name_FILM'] 


        #print(media) 
        #media = easygui. fileopenbox(title="Choose media to open")
        vlc_instance = vlc.Instance('--no-audio', '--fullscreen')
        player = vlc_instance.media_player_new()
        media = vlc_instance.media_new(Film_Name)
        player.set_media(media)
        while True:
            choice = easygui.buttonbox(title="Vision 2.0",msg="Press Play to start",choices=["Play","Pause","Stop","New"])
            print(choice)
            if choice == "Play":
            # if Users_Time_Saved['User1']['minute'] != 0:
                #    player.set_time(float(Users_Time_Saved['User1']['minute']))
                player.play()
            elif choice == "Pause":
                player.pause()
            elif choice == "Stop":
                Users_Time_Saved['User1']['minute'] = player.get_position()
                print("il tempo è:", Users_Time_Saved['User1']['minute'])
                player.stop()
            elif choice == "New":
                media = easygui.fileopenbox(title="Choose media to open")
                player = vlc.MediaPlayer(media)
            else:
                break

if __name__ == "__main__":
    # creating thread
    t1 = threading.Thread(target=Vision_LOOP, args=())
    t2 = threading.Thread(target=VLC_LOOP, args=())
    print("ciao")
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
 
    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()
 
    # both threads completely executed
    print("Done!")