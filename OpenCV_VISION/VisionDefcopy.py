import cv2
import sys
import requests
import json
import PySimpleGUI as sg
import vlc, easygui
import ast
import threading
import ctypes
from ctypes.util import find_library
Users_Time_Saved ={  "User1" : {
                        "name" : "",
                        "name_FILM" : "",
                        "temperature" : 0,
                        "minute" : 0
                    },
                    "User2" : {
                        "name" : "",
                        "name_FILM" : "",
                        "temperature" : 0,
                        "minute" : 0
                    },
                    "User3" : {
                        "name" : "",
                        "name_FILM" : "",
                        "temperature" : 0,
                        "minute" : 0
                    },
                    "User4" : {
                        "name" : "",
                        "name_FILM" : "",
                        "temperature" : 0,
                        "minute" : 0
                    },
                    }
Num_Faces = 0
def Vision_LOOP():

    name = ""
    global Users_Time_Saved
    global Num_Faces
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
    test_url_GET_NAME = addr + '/api/get_name'
    test_url_GET_DATA = addr + '/api/get_Additional_data'
    x11 = ctypes.PyDLL("libX11.so")
    x11.XInitThreads()


    # prepare headers for http request
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}
    #global name = ''
    names = ['','','','','','','','','','','']


    while 1:
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
        #       for i in range(0, len(names)):
            #     names[i] = ''

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
                response = requests.post(test_url_GET_NAME, data=img_encoded.tostring(), headers=headers)#PRENDO IL NOME
                #  decode response
                print(response.text)
                if 'User Not Found' in json.loads(response.text):
                    cout = 0
                else:
                    name = json.loads(response.text)

                #name_dict = json.loads(response.text)
                print("il nome e':", name)
                #ORA PRENDO IL JSON DEI DATI
                responseDATA = requests.post(test_url_GET_DATA, data=img_encoded.tostring(), headers=headers)#PRENDO I DATI

                response_DICT = ast.literal_eval(responseDATA.text)
                DATA_ADDITIONAL_DICT= ast.literal_eval(response_DICT[0])
                print("il JSON e'", DATA_ADDITIONAL_DICT)
                print("La temperature e'", DATA_ADDITIONAL_DICT["temperature"])
            if len(name) < 4:
                for t in range(0, len(name)):
                    names[t] = name[t]
                    Users_Time_Saved['User1']['name'] = name[t] #Salvo nella struttura condivisa 
                    Users_Time_Saved['User1']['name_FILM'] = DATA_ADDITIONAL_DICT["movie_name"]
                    Users_Time_Saved['User1']['temperature'] = DATA_ADDITIONAL_DICT["temperature"]
            cv2.putText(img,names[i],(x, y-10), font, 2,(255,255,255),2,cv2.LINE_AA)
            i = i + 1
        cv2.imshow('img', img)
    cap.release()

def VLC_LOOP():
    justOne = 0
    Minute = 0
    Player_IS_ON = 0
    while 1:
        if Users_Time_Saved['User1']['name'] != '' :
            #se l'utente e' stato riconosciuto e il nome preso dal database
            #Film_Name =  Users_Time_Saved['User1']['name_FILM']     
        # fd = open(Film_Name,'r')

            #player = vlc.MediaPlayer(Film_Name)
            #player.set_mrl(Film_Name)

            #media = vlc_instance.media_new(Film_Name)
            
        # player.set_media(media)
        
                if justOne == 0:
                    justOne = 1
                    media = easygui.fileopenbox(title="Choose media to open")
                    Users_Time_Saved['User1']['name_FILM'] = media
                    player = vlc.MediaPlayer(media)

                if Player_IS_ON == 0 and Num_Faces > 0:
                    print("aaaaaaa")
                    Player_IS_ON = 1
                    player.play()
                    if Minute != 0:
                        player.set_time(Minute)
                #elif choice == "Pause":
                    #   player.pause()
                elif Player_IS_ON == 1 and Num_Faces == 0:
                    print("vvvv")
                    Player_IS_ON = 0
                    Minute =  player.get_time()
                    print("PLAYER = ", Minute)
                    player.stop()

                    


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