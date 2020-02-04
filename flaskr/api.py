import functools
import base64
import io
import json
from PIL import Image
from flaskr.face_Def import *
from flaskr.voice_Def import *
import wave
import cv2
import numpy as np 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify,
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/get_name', methods=('GET', 'POST'))
def NameToExternal():
    print('roba')
    if request.method == 'POST':

        r = request
        # convert string of image data to uint8
        nparr = np.fromstring(r.data, np.uint8)
        # decode image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        #return jsonify(request.form)
        #salvare il blob in wav nella cartella
        print('eco')
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
                print("l'id è:",names[user])
            return jsonify(names)

        return jsonify(Id_User_Verified)
    return 0 






