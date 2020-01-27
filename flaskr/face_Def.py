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
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
#################################################### LOGGING WITH THE KEYS #############################
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '126503e73c86415ea39302b76fa1b6d8',
}
headers_FromStream = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '126503e73c86415ea39302b76fa1b6d8',
}
os.environ["FACE_SUBSCRIPTION_KEY"] = "126503e73c86415ea39302b76fa1b6d8"
os.environ["FACE_ENDPOINT"]="https://users.cognitiveservices.azure.com/"
# Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
# This key will serve all examples in this document.
KEY = os.environ['FACE_SUBSCRIPTION_KEY']

# Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = os.environ['FACE_ENDPOINT']

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
personGroupId="db_users_d"

def CreatePersonGroupID():
   

    body = dict()
    body["name"] = "U.S.E.R.S"
    body["userData"] = "All the users as different person"
    body = str(body)

    #Request URL 
    FaceApiCreateLargePersonGroup = 'https://users.cognitiveservices.azure.com/face/v1.0/persongroups/'+personGroupId
    # Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.

    try:
        # REST Call 
        response = requests.put(FaceApiCreateLargePersonGroup, data=body, headers=headers) 
        print("RESPONSE:" + str(response.status_code))

    except Exception as e:
        print(e)

def Add_Person(name, Id_On_My_DB):
    body = dict()
    body["name"] = name
    body["userData"] = Id_On_My_DB#UserData è l'id dell'utente nel DB nostro
    body = str(body)

    #Request URL 
    FaceApiCreatePerson = 'https://users.cognitiveservices.azure.com/face/v1.0/persongroups/'+personGroupId+'/persons' 

    try:
        # REST Call 
        response = requests.post(FaceApiCreatePerson, data=body, headers=headers) 
        responseJson = response.json()
        personId = responseJson["personId"]
        print("PERSONID: "+str(personId))
        
    except Exception as e:
        print(e)    

    return personId

def Get_Person(id):
    # Request URL 
    FaceApiGetPerson = 'https://users.cognitiveservices.azure.com/face/v1.0/persongroups/'+personGroupId+'/persons/'+id

    try:
        response = requests.get(FaceApiGetPerson, headers=headers) 
        responseJson = response.json()
        print("This Is "+str(responseJson["name"]))
        
    except Exception as e:
        print(e)
    return responseJson

def Add_Images_to_single_person(id):

    Users_images= [file for file in glob.glob('*.jpg') if file.startswith("New_User")]

    #Request URL 
    FaceApiCreatePerson = 'https://users.cognitiveservices.azure.com/face/v1.0/persongroups/'+personGroupId+'/persons/'+id+'/persistedFaces' 

    for image in Users_images:
        data = open(image, "rb").read()
        body = data
        print(body)
        try:
            # REST Call 
            response = requests.post(FaceApiCreatePerson, data=body, headers=headers_FromStream) 
            responseJson = response.json()
            persistedFaceId = responseJson["persistedFaceId"]
            print("PERSISTED FACE ID: "+str(persistedFaceId))
        
        except Exception as e:
            print(e)

CreatePersonGroupID()
#New_User_Id = Add_Person('dave', '004')

#Person = Get_Person(New_User_Id) #Restituisce l'oggetto person

#print('This is', Person["personId"])
Add_Images_to_single_person('933f3707-5c52-4417-b640-8945d3181089')


getList =  'https://users.cognitiveservices.azure.com/face/v1.0/persongroups/'+personGroupId+'/persons'
response = requests.get(getList, headers = headers)

print(response.json())

