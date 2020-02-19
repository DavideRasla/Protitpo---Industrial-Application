import functools
import base64
import io
import json
from PIL import Image
from flaskr.face_Def import *
from flaskr.voice_Def import *
import wave
import cv2
from flask import jsonify
import numpy as np
from datetime import datetime 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify,
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')
dateTimeObj_init = datetime.now()

@bp.route('/get_name', methods=('GET', 'POST'))
def NameToExternal():
    print("API: Get_Name()")
    if request.method == 'POST':

        dateTimeObj = datetime.now()
        difference = dateTimeObj - dateTimeObj_init
        print("VISION called after: ", difference)
        
        r = request
        # convert string of image data to uint8
        nparr = np.fromstring(r.data, np.uint8)
        # decode image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        #return jsonify(request.form)
        #salvare il blob in wav nella cartella
        
        Filename='flaskr/LogUser/Test_User.jpg'

        cv2.imwrite(Filename,img)
        names = []
        Id_User_Verified = Identify_User()
        #Id_User_Verified =  [file for file in glob.glob('./flaskr/LogUser/*.jpg')]
        #Id_User_Verified = cwd = os.getcwd()
        if 'User Not Found' not in Id_User_Verified:
            for user in range(0, len(Id_User_Verified)):
                db = get_db()
                cur = db.cursor()
                name = cur.execute(
                    'SELECT uname FROM user WHERE faceid =(?)',(str(Id_User_Verified[user]),))
                row = cur.fetchone()
                names.append(row[0])
                #name = ''
                print("The name is:",names[user])

            return jsonify(names)

        return jsonify(Id_User_Verified)

@bp.route('/get_Additional_data', methods=('GET', 'POST'))
def DataToExternal():
    print("API: Data_To_External()")
    if request.method == 'POST':

        r = request
        # convert string of image data to uint8
        nparr = np.fromstring(r.data, np.uint8)
        # decode image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        #return jsonify(request.form)
        #salvare il blob in .jpg nella cartella
        
        Filename='flaskr/LogUser/Test_User.jpg'

        cv2.imwrite(Filename,img)
        print('Immagine ricevuta da VISION correttamente e scritta in LogUser. ')
        UserSData = []
        Id_User_Verified = Identify_User()
        #Id_User_Verified =  [file for file in glob.glob('./flaskr/LogUser/*.jpg')]
        #Id_User_Verified = cwd = os.getcwd()
        if 'User Not Found' not in Id_User_Verified:
            for user in range(0, len(Id_User_Verified)):
                db = get_db()
                cur = db.cursor()
                id_row = cur.execute('SELECT id FROM user WHERE faceid = (?)',(str(Id_User_Verified[user]),))
                id = cur.fetchone()[0]
                print("l'id nella tabella additional data e':",id)

                userData = cur.execute(
                    "SELECT AD.userdata FROM additionaldata AD JOIN user U WHERE AD.id =(?)",(str(id),)) #USO L'ID PER ACCEDERE AL JSON CORRETTO
                row = cur.fetchone()
                UserSData.append(row[0])
 
                print("Il JSON contenente gli user data e il nome e'",UserSData[user])
            return jsonify(UserSData)
        
        return jsonify(Id_User_Verified)
    return 0 






