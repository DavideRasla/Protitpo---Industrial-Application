import cv2
import sys
import requests
import json
import PySimpleGUI as sg
import vlc, easygui
import ast
import threading
import ctypes
import time
from ctypes.util import find_library

x11 = ctypes.PyDLL("libX11.so")
x11.XInitThreads()


############################### DATA STRUCTURES ####################################
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
                    }
Num_Faces = 0
old_faces = 0
def Vision_LOOP():
    
    global Users_Time_Saved
    global Num_Faces
    global old_faces
    cap = cv2.VideoCapture(0)
    name = ""
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    count = 0
    img = 0
    frame = img
    url = 'https://0.0.0.0:5000/api/get_name'
    addr = 'https://0.0.0.0:5000'
    test_url_GET_NAME = addr + '/api/get_name'
    test_url_GET_DATA = addr + '/api/get_Additional_data'



    # prepare headers for http request
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}
    #global name = ''
    names = ['','','','']


    while 1:
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
        # Draw the rectangle around each face

        if len(faces) == 0:
            old_faces = 0


        num_users_max = 0
        NotFound = 0
        for (x, y, w, h) in faces:
            if num_users_max < 2:
                rect = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                font = cv2.FONT_HERSHEY_PLAIN
                if count > 10:#se per 10 frame riconosco un cambio nel numero di  facce
                    # encode image as jpeg
                    print(len(faces))
                    count = 0
                    old_faces = len(faces)

                    _, img_encoded = cv2.imencode('.jpg', img)

                    response = requests.post(test_url_GET_NAME, data=img_encoded.tostring(), headers=headers,verify=False)#PRENDO IL NOME
                    print(response.text)
                    if 'User Not Found' in json.loads(response.text):
                        NotFound = 1
                        break

                    name = json.loads(response.text)
                    print("il nome e':", name)

                    responseDATA = requests.post(test_url_GET_DATA, data=img_encoded.tostring(), headers=headers,verify=False)#PRENDO I DATI
                    print(responseDATA.text) 
                    response_DICT = ast.literal_eval(responseDATA.text)
                    print(response_DICT)
                    DATA_ADDITIONAL_DICT= ast.literal_eval(response_DICT[0])
                    print("il JSON e'", DATA_ADDITIONAL_DICT)
                #  print("La temperature e'", DATA_ADDITIONAL_DICT["temperature"])

                    Num_Faces = len(name)
                    print("la len name è", len(name))
                    if len(name) == 1:
                        names[0] = name[0]
                        Users_Time_Saved['User1']['name'] = name[0] #Salvo nella struttura condivisa 
                        Users_Time_Saved['User1']['name_FILM'] = DATA_ADDITIONAL_DICT["movie_name"]
                        Users_Time_Saved['User1']['temperature'] = DATA_ADDITIONAL_DICT["temperature"]
                       
                    if len(name) == 2:

                        names[0] = name[0]
                        Users_Time_Saved['User1']['name'] = name[0] #Salvo nella struttura condivisa 
                        Users_Time_Saved['User1']['name_FILM'] = DATA_ADDITIONAL_DICT["movie_name"]
                        Users_Time_Saved['User1']['temperature'] = DATA_ADDITIONAL_DICT["temperature"]
                    
                        names[1] = name[1]
                        Users_Time_Saved['User2']['name'] = name[1] #Salvo nella struttura condivisa 
                        Users_Time_Saved['User2']['name_FILM'] = DATA_ADDITIONAL_DICT["movie_name"]
                        Users_Time_Saved['User2']['temperature'] = DATA_ADDITIONAL_DICT["temperature"]
                
                if NotFound == 0:
                    cv2.putText(img,names[num_users_max],(x, y-10), font, 2,(255,255,255),2,cv2.LINE_AA)
                    num_users_max = num_users_max + 1
        cv2.imshow('img', img)
    #finewhile
        k = cv2.waitKey(30) & 0xff
        if k==8:
            break
    cap.release()

def VLC_LOOP():
    First_Time = 0
    Player_IS_ON = 0
    Minute = 0
    OldFaces_Filmed = 0
    Name_Player_ONVIDEO = ''
    global old_faces
    while 1:

        if First_Time == 0:
            media = easygui.fileopenbox(title="Choose media to open")
            Users_Time_Saved['User1']['name_FILM'] = media
            player = vlc.MediaPlayer(media)
            First_Time = 1
            Name_Player_ONVIDEO = Users_Time_Saved['User1']['name']

        # if media is not on AND there are more than 1 face in the video AND it's the same face
        if Player_IS_ON == 0 and old_faces > 0 and Name_Player_ONVIDEO == Users_Time_Saved['User1']['name']:
            print("Start Video")
            Player_IS_ON = 1
            player.play()
            if Minute != 0:
                player.set_time(Minute)
        elif Player_IS_ON == 1 and old_faces == 0 and Name_Player_ONVIDEO == Users_Time_Saved['User1']['name']:
            print("Pause Video")
            Player_IS_ON = 0
            Minute = player.get_time()
            player.pause()
            count = 0
            while old_faces == 0: #aspetto 3 secondi e poi stoppo il video
                 time.sleep(1)
                 count = count + 1
                 if count == 3:
                     print("Stop after 3 seconds")
                     Minute =  player.get_time()
                     player.stop()
        elif  Player_IS_ON == 1 and Name_Player_ONVIDEO != Users_Time_Saved['User1']['name']:
            Name_Player_ONVIDEO = Users_Time_Saved['User1']['name']
            Minute = player.get_time()
            player.stop()
            Player_IS_ON == 0
            media = easygui.fileopenbox(title="Choose media to open")
           # Users_Time_Saved['User1']['name_FILM'] = media
            player = vlc.MediaPlayer(media)


                    


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