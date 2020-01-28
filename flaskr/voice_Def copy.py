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
import wave, struct, math
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
#################################################### LOGGING WITH THE KEYS #############################
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'f08811df201948ed9074dccd4c288c53',
}
headers_FromStream = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': 'f08811df201948ed9074dccd4c288c53',
}
os.environ["VOICE_SUBSCRIPTION_KEY"] = "f08811df201948ed9074dccd4c288c53"
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
    'Ocp-Apim-Subscription-Key': 'f08811df201948ed9074dccd4c288c53',
    }
    params = urllib.parse.urlencode({
    # Request parameters
    'shortAudio': 'false',#Set true in order to use any audio length (min 1 sec)
    })
 

    Reg_Voice_FileName= [file for file in glob.glob('**/*.wav', recursive = True) if file.startswith("EnrollUserVoice/Rec_New_User")]
    #print(Reg_Voice_FileName)
    w = wave.open('./EnrollUserVoice/Rec_New_User.wav', 'wb')
    #binary_wav = w.readframes(w.getnframes())
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(16000)#These settings are required by the azure API





    data = open(r'./EnrollUserVoice/Rec_New_User.wav', 'rb') 
    
    #fs, data = wavfile.read('./EnrollUserVoice/Rec_New_User.wav')
    body = data 
        #Request URL 
    VoiceEnrollmentProfile = "https://usersvoice.cognitiveservices.azure.com/spid/v1.0/identificationProfiles/"+id+"/enroll?%s"


    try:
        # REST Call
        with open('./EnrollUserVoice/Rec_New_User.wav', 'rb') as file:
            response = requests.post(VoiceEnrollmentProfile, data=file, headers=headers_Enrollment) 

        print("wRESPONSE:" + str(response))
        responseJson = response.json()
       # personId = responseJson["identificationProfileId"]
        print("PERSONID: "+str(responseJson))

            

    except Exception as e:
        print("ERROR:",e)
   
   # return personId

def Get_Operation_Status(id):

    params = urllib.parse.urlencode({

    })



    body = {} 
        #Request URL 
    VoiceGetStatus = "https://usersvoice.cognitiveservices.azure.com/spid/v1.0/operations/"+id+"?%s"


    try:
        # REST Call 
        response = requests.get(VoiceGetStatus, data=body, headers=headers) 

        print("RESPONSE:" + str(response.status_code))
        responseJson = response.json()
       # personId = responseJson["identificationProfileId"]
        print("PERSONID: "+str(responseJson))
            

    except Exception as e:
        print(e)
   
   # return personId



New_User_ID = Add_User_Voice()
Add_Enrollment_To_Single_Profile(New_User_ID)
Get_Operation_Status(New_User_ID)


