import functools
import base64
import io
import json
from PIL import Image
from flaskr.face_Def import *
from flaskr.voice_Def import *
import wave

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
        #return jsonify(request.form)
        #salvare il blob in wav nella cartella
        print('eco')
        Filename='flaskr/LogUser/Test_User.jpg'
        #biteimg = bytes(request.form['file'],encoding="ascii")
        biteimg = request.form['file'].encode()
        imgdata = biteimg[biteimg.find(b'/9'):]
        im = Image.open(io.BytesIO(base64.b64decode(imgdata))).save(filename)

        Id_User_Verified = Identify_User()
        #Id_User_Verified =  [file for file in glob.glob('./flaskr/LogUser/*.jpg')]
        #Id_User_Verified = cwd = os.getcwd()
        return jsonify(Id_User_Verified)
    return 






