import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
import base64
import wave
import json
import wave, struct, math
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
#################################################### LOGGING WITH THE KEYS #############################
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'ac52b08018554e1aa904c37bd1bba179',
}
headers_FromStream = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': 'ac52b08018554e1aa904c37bd1bba179',
}
os.environ["VOICE_SUBSCRIPTION_KEY"] = "ac52b08018554e1aa904c37bd1bba179"
os.environ["VOICE_ENDPOINT"]="https://usersvoice.cognitiveservices.azure.com/spid/v1.0"
# Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
# This key will serve all examples in this document.
KEY = os.environ['VOICE_SUBSCRIPTION_KEY']

# Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = os.environ['VOICE_ENDPOINT']


##

########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64


def Add_User_Voice():#Aggiunge un profilo e ritorna l'id relativo
    params = urllib.parse.urlencode({
    })


    body = dict()
    body["locale"] = "en-us"
    body = str(body)

    #Request URL 
    VoiceAddProfile = "https://usersvoice.cognitiveservices.azure.com/spid/v1.0/identificationProfiles?%s"


    try:
        # REST Call 
        response = requests.post(VoiceAddProfile, data=body, headers=headers) 

        print("RESPONSE:" + str(response.status_code))
        responseJson = response.json()
        personId = responseJson["identificationProfileId"]
        print("PERSONID: "+str(personId))
            

    except Exception as e:
        print(e)
    
    return personId



def Add_Enrollment_To_Single_Profile(id):# Registra un profilo
    headers_Enrollment = {
    # Request headers
    'Content-Type': 'multipart/form-data',
    'Ocp-Apim-Subscription-Key': 'ac52b08018554e1aa904c37bd1bba179',
    }
    params = urllib.parse.urlencode({
    # Request parameters
    'shortAudio': 'true',#Set true in order to use any audio length (min 1 sec)
    })
 


    with wave.open("./flaskr/EnrollUserVoice/newrec.wav", "rb") as wav_file:    # Open WAV file in read-only mode.
        # Get basic information.
        n_channels = wav_file.getnchannels()      # Number of channels. (1=Mono, 2=Stereo).
        sample_width = wav_file.getsampwidth()    # Sample width in bytes.
        framerate = wav_file.getframerate()       # Frame rate.
        n_frames = wav_file.getnframes()          # Number of frames.
        comp_type = wav_file.getcomptype()        # Compression type (only supports "NONE").
        comp_name = wav_file.getcompname()        # Compression name.
        # Read audio data.
        frames = wav_file.readframes(n_frames)    # Read n_frames new frames.

        
    newframerate = 16000
    # Duplicate to a new WAV file.
    with wave.open("./flaskr/EnrollUserVoice/newrec.wav", "wb") as wav_file:    # Open WAV file in write-only mode.
        # Write audio data.
        nparams = (1, 2, newframerate, n_frames, comp_type, comp_name)
        wav_file.setparams(nparams)
        wav_file.writeframes(frames)

    
    data = open(r'./flaskr/EnrollUserVoice/newrec.wav', 'rb').read()
        
    #fs, data = wavfile.read('./EnrollUserVoice/Rec_New_User.wav')
    body = data 
        #Request URL 
    VoiceEnrollmentProfile = "https://usersvoice.cognitiveservices.azure.com/spid/v1.0/identificationProfiles/"+id+"/enroll?%s" %params

    try:

        response = requests.post(VoiceEnrollmentProfile, data= body, params=params, headers=headers_Enrollment) 

        print("Enrollment, response::" + str(response))
        print(response.headers)
        print(response._content)
        Results_header = response.headers
        print("Enrollment headers",Results_header['Operation-Location'])
    except Exception as e:
        print("ERROR_Enrollment:",e)
   
    return Results_header['Operation-Location'] 

def Get_Operation_Status(url_to_use):
    headers_Simple = {
    'Ocp-Apim-Subscription-Key': 'ac52b08018554e1aa904c37bd1bba179',
    }
    params = urllib.parse.urlencode({

    })

    body = {} 
        #Request URL 
    VoiceGetStatus = url_to_use


    try:
        # REST Call
       # time.sleep(10)
        response = requests.get(VoiceGetStatus, data=body, headers=headers_Simple) 

        json_data = json.loads(response.text)
        Empty = "None"

        while  Empty  in str(json_data['processingResult']): #aspetto finche non ho una risposta
                response = requests.get(VoiceGetStatus, data=body, headers=headers_Simple) 
                json_data = json.loads(response.text)
            
        status = json_data['status']
        print(str(status))
        print("Get_Operation_Status, status code:" + str(response.status_code))
        responseJson = response.json()
       # personId = responseJson["identificationProfileId"]
        print("Get_Operation_Status, results:: "+str(responseJson))
        return json_data['processingResult']['enrollmentStatus']

    except Exception as e:
        print("ERRORE NELLA GET STATUS IN REGISTRAZIONE",e)

def Get_Operation_Status_Identify(url_to_use):
    headers_Simple = {
    'Ocp-Apim-Subscription-Key': 'ac52b08018554e1aa904c37bd1bba179',
    }
    params = urllib.parse.urlencode({

    })

    body = {} 
        #Request URL 
    VoiceGetStatus = url_to_use


    try:
        # REST Call
        #time.sleep(5)

        response = requests.get(VoiceGetStatus, data=body, headers=headers_Simple) 

        
        json_data = json.loads(response.text)
        Empty = "None"

        while  Empty  in str(json_data['processingResult']):#aspetto finche non ho una risposta
                response = requests.get(VoiceGetStatus, data=body, headers=headers_Simple) 
                json_data = json.loads(response.text)
            
        status = json_data['status']
        confidence = json_data['processingResult']['confidence']
        id_Utente_Identificato = json_data['processingResult']['identifiedProfileId']
        print(str(status))
        print(str(confidence))
        print(str(id_Utente_Identificato))
     
        responseJson = response.json()
       # print("Get_Operation_Status, results:: "+str(responseJson))

        if("High" in confidence or "Normal" in confidence):
            print("Utente trovato! ID: ", id_Utente_Identificato)
            return id_Utente_Identificato   

    except Exception as e:
        print("Error in Get_Status_Identify",e)
    return 404 

def identify_User_Voice(lista_utenti_id):

    headers_Enrollment = {
    # Request headers
    'Content-Type': 'multipart/form-data',
    'Ocp-Apim-Subscription-Key': 'ac52b08018554e1aa904c37bd1bba179',
    }
    params = urllib.parse.urlencode({
    # Request parameters
    'shortAudio': 'true',#Set true in order to use any audio length (min 1 sec)
    })



    with wave.open("./flaskr/TestUserVoice/newrec.wav", "rb") as wav_file:    # Open WAV file in read-only mode.
        # Get basic information.
        n_channels = wav_file.getnchannels()      # Number of channels. (1=Mono, 2=Stereo).
        sample_width = wav_file.getsampwidth()    # Sample width in bytes.
        framerate = wav_file.getframerate()       # Frame rate.
        n_frames = wav_file.getnframes()          # Number of frames.
        comp_type = wav_file.getcomptype()        # Compression type (only supports "NONE").
        comp_name = wav_file.getcompname()        # Compression name.
        # Read audio data.
        frames = wav_file.readframes(n_frames)    # Read n_frames new frames.

        assert len(frames) == sample_width * n_frames

    newframerate = 16000
    # Duplicate to a new WAV file.
    with wave.open("./flaskr/TestUserVoice/newrec.wav", "wb") as wav_file:    # Open WAV file in write-only mode.
        # Write audio data.
        nparams = (n_channels, sample_width, newframerate, n_frames, comp_type, comp_name)
        wav_file.setparams(nparams)
        wav_file.writeframes(frames)

    
    data = open(r'./flaskr/TestUserVoice/newrec.wav', 'rb').read()
        
    body = data 
        #Request URL 
    id_Trovati = []
    for id in lista_utenti_id:

        try:
            VoiceIdentifyAPI = "https://usersvoice.cognitiveservices.azure.com/spid/v1.0/identify?identificationProfileIds="+id+"&%s" % params

            response = requests.post(VoiceIdentifyAPI, data= body, params=params, headers=headers_Enrollment) 

            print("Identify response:" + str(response))
            #print("Identify, header:",response.headers)
            Results_header = response.headers
           # print("Identify Url Operation: ",Results_header['Operation-Location'])
        #Guardo lo stato dell'operazione
            id_Trovato = Get_Operation_Status_Identify(Results_header['Operation-Location'])
            if id_Trovato != 404:
                id_Trovati.append(id_Trovato)
                return id_Trovati #THIS MUST BE AN ARRAY IN ORDER TO BE COERENT WITH THE APIs
        except Exception as e:
            print("ERROR_ Identfy:",e)

    return "Nessun Utente trovato" 

def Get_All_Profiles():
    headers_Simple = {
    'Ocp-Apim-Subscription-Key': 'ac52b08018554e1aa904c37bd1bba179',
    }
    params = urllib.parse.urlencode({

    })

    body = dict()
    body["locale"] = "en-us"
    body = str(body) 
        #Request URL 
    GetProfilesAPI = "https://usersvoice.cognitiveservices.azure.com/spid/v1.0/identificationProfiles?%s"

    from ast import literal_eval

    try:
        # REST Call
        #time.sleep(10)
        response = requests.get(GetProfilesAPI, data=body, headers=headers_Simple) 

        json_data = json.loads(response.text)
        t = []
        for x in range(0,len(json_data)):
            t.append(json_data[x]['identificationProfileId'])
        print('Lista ID Utenti: ',t)


            

    except Exception as e:
        print(e)
    
    return t


def Delete_All_Profiles(ListaProfili):
    headers_Enrollment ={ 
    'Ocp-Apim-Subscription-Key': 'ac52b08018554e1aa904c37bd1bba179',
    }
    params = urllib.parse.urlencode({

    })

     
    body = dict()
    body["locale"] = "en-us"
    body = str(body) 
        #Request URL 
  
    for id in ListaProfili:
        try:
            DeleteProfileAPI = "https://usersvoice.cognitiveservices.azure.com/spid/v1.0/identificationProfiles/"+id

            response = requests.delete(DeleteProfileAPI, data= body, params=params, headers=headers_Enrollment) 

            print("Delete_ALL_PROFILE, response:" + str(response))
            # print("Delete, header:",response.headers)

        except Exception as e:
            print("ERROR_Delete_ALL_Profile:",e)

    return response.headers 

def Get_A_Profile(id):
    headers_Enrollment ={ 
    'Ocp-Apim-Subscription-Key': 'ac52b08018554e1aa904c37bd1bba179',
    }
    params = urllib.parse.urlencode({

    })

     
    body = dict()
    body["locale"] = "en-us"
    body = str(body) 
        #Request URL 
  
    try:
        GetProfileAPI = "https://usersvoice.cognitiveservices.azure.com/spid/v1.0/identificationProfiles/"+id

        response = requests.get(GetProfileAPI, data= body, params=params, headers=headers_Enrollment) 
        responseJson = response.json()
        print("Profile JSON:" + str(responseJson))
        # print("Delete, header:",response.headers)

    except Exception as e:
        print("ERROR_GetProfile:",e)

    return


def Delete_A_Profile(id):
    headers_Enrollment ={ 
    'Ocp-Apim-Subscription-Key': 'ac52b08018554e1aa904c37bd1bba179',
    }
    params = urllib.parse.urlencode({

    })

     
    body = dict()
    body["locale"] = "en-us"
    body = str(body) 
        #Request URL 
  

    try:
        DeleteProfileAPI = "https://usersvoice.cognitiveservices.azure.com/spid/v1.0/identificationProfiles/"+id

        response = requests.delete(DeleteProfileAPI, data= body, params=params, headers=headers_Enrollment) 

        print("Delete_A_PROFILE, response:" + str(response))
        # print("Delete, header:",response.headers)

    except Exception as e:
        print("ERROR_Delete_A_Profile:",e)

    return response.headers 

#New_User_ID = Add_User_Voice()

#Operation_ID_URL = Add_Enrollment_To_Single_Profile(New_User_ID)
#Get_Operation_Status(Operation_ID_URL)

#Get_A_Profile(New_User_ID)

#ListaUtenti = Get_All_Profiles()
#print(identify_User_Voice(ListaUtenti))
#Get_Operation_Status(Operation_Identification_Url)
#Delete_All_Profiles(ListaUtenti)
#Delete_A_Profile(New_User_ID)
#ListaUtenti = Get_All_Profiles()
#ListaUtenti = Get_All_Profiles()
#print(ListaUtenti)
#Operation_Id = identify_User_Voice(ListaUtenti)
#Get_Operation_Status(Operation_Id)




