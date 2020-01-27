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
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
#################################################### LOGGING WITH THE KEYS #############################
headers = {
    'Content-Type': 'application/json',
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
   
# Used in the Person Group Operations,  Snapshot Operations, and Delete Person Group examples.
# You can call list_person_groups to print a list of preexisting PersonGroups.
# SOURCE_PERSON_GROUP_ID should be all lowercase and alphanumeric. For example, 'mygroupname' (dashes are OK).
PERSON_GROUP_ID = 'users_db'

# Used for the Snapshot and Delete Person Group examples.
TARGET_PERSON_GROUP_ID = str(uuid.uuid4()) # assign a random ID (or name it anything)

################################################## Creating the PersonGroup, just the first time ###############################

# Create empty Person Group. Person Group ID must be lower case, alphanumeric, and/or with '-', '_'.
print('Person group:', PERSON_GROUP_ID)
#face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID) #remove the comment in order to re-create the DB


# Define the users
Users = face_client.person_group_person.create(PERSON_GROUP_ID, "Users")


def Add_User():

    '''
    Detect faces and register to correct person
    '''
    # Find all jpeg images of the new user in working directory
    Users_images= [file for file in glob.glob('*.jpg') if file.startswith("Users")]

    # Add to a woman person
    for image in Users_images: 
        u = open(image, 'r+b')
        face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, Users.person_id, u)


        '''
    Train PersonGroup
    '''
    print()
    print('Training the person group...')
    # Train the person group
    face_client.person_group.train(PERSON_GROUP_ID)

    while (True):
        training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
        print("Training status: {}.".format(training_status.status))
        print()
        if (training_status.status is TrainingStatusType.succeeded):
            break
        elif (training_status.status is TrainingStatusType.failed):
            sys.exit('Training the person group has failed.')
        time.sleep(5)


def Identify_User():
    '''
    Identify a face against a defined PersonGroup
    '''
    # Group image for testing against
    group_photo = 'Test_User.jpg'
    IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)))
    # Get test image
    test_image_array = glob.glob(os.path.join(IMAGES_FOLDER, group_photo))
    image = open(test_image_array[0], 'r+b')

    # Detect faces
    face_ids = []
    faces = face_client.face.detect_with_stream(image)
    for face in faces:
        face_ids.append(face.face_id)



        # Identify faces
    results = face_client.face.identify(face_ids, PERSON_GROUP_ID)
    print('Identifying faces in {}'.format(os.path.basename(image.name)))
    print('Results ',results[0])

    if len(results[0].candidates) == 0 :
     print('No person identified in the person group for faces from {}.'.format(os.path.basename(image.name)))
    else:
        for person in results:
            if len(person.candidates) != 0 :
                print('Person for face ID {} is identified in {} with a confidence of {}.'.format(person.face_id, os.path.basename(image.name), person.candidates[0].confidence)) # Get topmost confidence score
    
    FaceApiGetPerson = 'https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/'+PERSON_GROUP_ID+'/persons/'+results[0].face_id

    try:
        response = requests.get(FaceApiGetPerson, headers=headers) 
        responseJson = response.json()
        print("This Is "+str(responseJson["name"]))
    except Exception as e:
        print(e)
    
#Add_User()
Identify_User()