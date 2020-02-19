
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import * 
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
personGroupId="users_db"

def CreatePersonGroupID():#Crea un nuovo PersonGroupID
   

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

def Add_Person(name, Id_On_My_DB):#Dato nome e id sul database, aggiunge una persona e restituise il suo id
    body = dict()
    body["name"] = name
    body["userData"] = Id_On_My_DB
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
        print('Error in ADD_Person:',e)    

    return personId

def Get_Person(id):#Dato l'id restituisce l'intero json della persona
    # Request URL 
    FaceApiGetPerson = 'https://users.cognitiveservices.azure.com/face/v1.0/persongroups/'+personGroupId+'/persons/'+id

    try:
        response = requests.get(FaceApiGetPerson, headers=headers) 
        responseJson = response.json()
        
    except Exception as e:
        print(e)
    return responseJson

def Add_Images_to_single_person(id):#Aggiunge immagini ad una persona, conoscendo l'id

    #Users_images= [file for file in glob.glob('**/*.jpg', recursive = True) if file.startswith("RegUser/NewUser")]
    Users_images = [file for file in glob.glob('./flaskr/RegUser/*.jpg')]


    print(Users_images)
    #Request URL 
    FaceApiAddImage= 'https://users.cognitiveservices.azure.com/face/v1.0/persongroups/'+personGroupId+'/persons/'+id+'/persistedFaces' 

    for image in Users_images:
        data = open(image, "rb").read()
        body = data
        try:
            # REST Call 
            response = requests.post(FaceApiAddImage, data=body, headers=headers_FromStream) 
            responseJson = response.json()
            persistedFaceId = responseJson["persistedFaceId"]
            print("PERSISTED FACE ID: "+str(persistedFaceId))
        except Exception as e:
            print(e)

def Delete_Single_Person(id):#Elimina una persona dato l'id

    #Request URL 
    FaceDeletePersonApi= 'https://users.cognitiveservices.azure.com/face/v1.0/persongroups/'+personGroupId+'/persons/'+id 

    try:
        # REST Call 
        response = requests.delete(FaceDeletePersonApi,headers=headers) 
        responseJson = response.json()
        print(responseJson)
    except Exception as e:
        print(e)

def Delete_EntirePersonGroup(id):#Elimina una intero person group

    #Request URL 
    FaceDeletePersonGroup= 'https://users.cognitiveservices.azure.com/face/v1.0/persongroups/'+id

    try:
        # REST Call 
        response = requests.delete(FaceDeletePersonGroup,headers=headers) 
        responseJson = response.json()
        print(responseJson)
    except Exception as e:
        print(e)

def Delete_All_Person_Groups():#Elimina TUTTI i person groups #TODOO, Doesn't not work

    #Request URL 
    FaceDeletePersonGroup= 'https://users.cognitiveservices.azure.com/face/v1.0/persongroups'

    try:
        # REST Call 
        response = requests.delete(FaceDeletePersonGroup,headers=headers) 
        responseJson = response.json()
        print(responseJson)
    except Exception as e:
        print(e)
    return responseJson



def List_All_Person_Groups():#Mostra tutti i person group presenti

    #Request URL 
    FaceListPersonGroup= 'https://users.cognitiveservices.azure.com/face/v1.0/persongroups'

    try:
        # REST Call 
        response = requests.get(FaceListPersonGroup,headers=headers) 
        responseJson = response.json()
        print(responseJson)
    except Exception as e:
        print(e)
    return responseJson


def List_All_Users_Inside_A_PersonGroup(idGroup):

    getList =  'https://users.cognitiveservices.azure.com/face/v1.0/persongroups/'+idGroup+'/persons'
    response = requests.get(getList, headers = headers)

    print(response.json())

def Train_Person_Group(idGroup):
    body = dict()

    #Request URL 
    FaceApiTrain = 'https://users.cognitiveservices.azure.com/face/v1.0/persongroups/'+idGroup+'/train'

    try:
        # REST Call 
        response = requests.post(FaceApiTrain, data=body, headers=headers) 
        print("RESPONSE:" + str(response.status_code))

    except Exception as e:
        print(e)

def Identify_User():


    #Test_User_Image= [file for file in glob.glob('**/*.jpg', recursive = True) if file.startswith("LogUser/Test_User")] 
    #RIGA SOPRA SOLO SE USO DIRETTAMENTE LA FUNZIONE DA TERMINALE.

    Test_User_Image = [file for file in glob.glob('./flaskr/LogUser/*.jpg')]


    # Request URL 
    FaceApiDetect = 'https://users.cognitiveservices.azure.com/face/v1.0/detect?returnFaceId=true' 
    faceIdsList = []
    for image in Test_User_Image:
        data = open(image, "rb").read()
        body = data

        try:
            # REST Call 
            response = requests.post(FaceApiDetect, data=body, headers=headers_FromStream) 
            responseJson = response.json()
            for x in range(0, len(responseJson)):
                faceId = responseJson[x]["faceId"]
                faceIdsList.append(faceId)
            print("FACE ID: "+str(faceId))

        except Exception as e:
            print('Error is: ',e)

   # faceIdsList = [faceId]
    #Second Phase: Given the test_face ID return the related user

    body = dict()
    body["personGroupId"] = personGroupId
    body["faceIds"] = faceIdsList
    body["maxNumOfCandidatesReturned"] = 1 
    body["confidenceThreshold"] = 0.5
    body = str(body)

    # Request URL 
    FaceApiIdentify = 'https://users.cognitiveservices.azure.com/face/v1.0/identify' 
    Id_Recognized = []
    try:
        # REST Call 
        response = requests.post(FaceApiIdentify, data=body, headers=headers) 
        responseJson = response.json()
        for x in range(0, len(responseJson)): 
            personId = responseJson[x]["candidates"][0]["personId"]
            confidence = responseJson[x]["candidates"][0]["confidence"]
            print("PERSON ID: "+str(personId))
            Id_Recognized.append(personId)
          
    except Exception as e:
        print("Could not detect")
        return "User Not Found"
    return Id_Recognized



def Delete_Reg_Photos(): #Delete all the photos used for registration

    #Test_User_Image= [file for file in glob.glob('**/*.jpg', recursive = True) if file.startswith("RegUser/NewUser")]
    Test_User_Image = [file for file in glob.glob('./flaskr/RegUser/*.jpg')]

    for i in range(len(Test_User_Image)):
        os.remove(Test_User_Image[i])
    Test_User_Image = [file for file in glob.glob('./flaskr/RegUser/*.jpg')]
    if(len(Test_User_Image) == 0):
        return 1
    return 0


def Delete_Log_Photos(): #Delete all the photos used for logging

    #Test_User_Image= [file for file in glob.glob('**/*.jvpg', recursive = True) if file.startswith("LogUser/Test_User")]
    Test_User_Image = [file for file in glob.glob('./flaskr/LogUser/*.jpg')]
    for i in range(len(Test_User_Image)):
        os.remove(Test_User_Image[i])

    Test_User_Image = [file for file in glob.glob('./flaskr/LogUser/*.jpg')]
    if(len(Test_User_Image) == 0):
        return 1
    return 0



#CreatePersonGroupID()
#New_Id =  Add_Person('VerificaVera', '002')

#Person = Get_Person('758aa814-8558-4f3d-a7de-5d5039c4be73') #Restituisce l'oggetto person

#print('This is', Person["name"])
#Add_Images_to_single_person(New_Id)

#Delete_EntirePersonGroup('users_db')
#Delete_Single_Person('dd04d7aa-892b-4d2c-be9e-ab732f5286b8')
#print(List_All_Users_Inside_A_PersonGroup('users_db'))
#print(List_All_Person_Groups())
#Train_Person_Group('users_db')
#Identify_User()
#print(Delete_Reg_Photos())
