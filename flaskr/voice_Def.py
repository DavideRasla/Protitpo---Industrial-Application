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
    'shortAudio': 'true',#Set true in order to use any audio length (min 1 sec)
    })
 

   #Reg_Voice_FileName= [file for file in glob.glob('**/*.wav', recursive = True) if file.startswith("EnrollUserVoice/Rec_New_User")]
   # #print(Reg_Voice_FileName)
    #w = wave.open('./EnrollUserVoice/newrec.wav', 'wb')
    #binary_wav = w.readframes(w.getnframes())
    #w.setparams(1,2,16000)
     
    #w.setnchannels(1)
   # w.setsampwidth(2)
    #w.setframerate(16000)#These settings are required by the azure API
    #w.close()
    #guardo caratteristiche audio

  #  wav_file = wave.open('./EnrollUserVoice/newrec.wav', 'rb')
   # print('Il frame rate è: ', wav_file.getframerate())
    #print('Channels: ', wav_file.getnchannels())
    #print('sample width: ', wav_file.getsampwidth())

#    wav_file.close()

    with wave.open("./EnrollUserVoice/newrec.wav", "rb") as wav_file:    # Open WAV file in read-only mode.
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
    with wave.open("./EnrollUserVoice/newrec.wav", "wb") as wav_file:    # Open WAV file in write-only mode.
        # Write audio data.
        nparams = (n_channels, sample_width, newframerate, n_frames, comp_type, comp_name)
        wav_file.setparams(nparams)
        wav_file.writeframes(frames)

    
    data = open(r'./EnrollUserVoice/newrec.wav', 'rb').read()
        
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
    'Ocp-Apim-Subscription-Key': 'f08811df201948ed9074dccd4c288c53',
    }
    params = urllib.parse.urlencode({

    })

    body = {} 
        #Request URL 
    VoiceGetStatus = url_to_use


    try:
        # REST Call
        time.sleep(10)
        response = requests.get(VoiceGetStatus, data=body, headers=headers_Simple) 

        print("Get_Operation_Status, status code:" + str(response.status_code))
        responseJson = response.json()
       # personId = responseJson["identificationProfileId"]
        print("Get_Operation_Status, results:: "+str(responseJson))
            

    except Exception as e:
        print(e)
   
   # return personId

def identify_User_Voice(id):

    headers_Enrollment = {
    # Request headers
    'Content-Type': 'multipart/form-data',
    'Ocp-Apim-Subscription-Key': 'f08811df201948ed9074dccd4c288c53',
    }
    params = urllib.parse.urlencode({
    # Request parameters
    'shortAudio': 'true',#Set true in order to use any audio length (min 1 sec)
    })



    with wave.open("./TestUserVoice/newrec.wav", "rb") as wav_file:    # Open WAV file in read-only mode.
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
    with wave.open("./TestUserVoice/newrec.wav", "wb") as wav_file:    # Open WAV file in write-only mode.
        # Write audio data.
        nparams = (n_channels, sample_width, newframerate, n_frames, comp_type, comp_name)
        wav_file.setparams(nparams)
        wav_file.writeframes(frames)

    
    data = open(r'./TestUserVoice/newrec.wav', 'rb').read()
        
    body = data 
        #Request URL 
    VoiceIdentifyAPI = "https://usersvoice.cognitiveservices.azure.com//spid/v1.0/identify?identificationProfileIds="+id+"&%s" % params

    try:

        response = requests.post(VoiceIdentifyAPI, data= body, params=params, headers=headers_Enrollment) 

        print("Identify response:" + str(response))
        print("Identify, header:",response.headers)
        Results_header = response.headers
        print("Identify Url Operation: ",Results_header['Operation-Location'])
    except Exception as e:
        print("ERROR_Enrollment:",e)

    return Results_header['Operation-Location'] 

New_User_ID = Add_User_Voice()
Operation_ID_URL = Add_Enrollment_To_Single_Profile(New_User_ID)
Get_Operation_Status(Operation_ID_URL)
Operation_Identification_Url = identify_User_Voice(New_User_ID)
Get_Operation_Status(Operation_Identification_Url)
