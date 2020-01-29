import functools
import base64
import io
import json
from PIL import Image
from flaskr.face_Def import *


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify,
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def get_last_row(db):
    cur = db.cursor()
    return cur.lastrowid

def save_image_to_file(img,img_data):
    filename=img
    biteimg = img_data.encode()
    imgdata = biteimg[biteimg.find(b'/9'):]
    im = Image.open(io.BytesIO(base64.b64decode(imgdata))).save(img)
    

@bp.route('/start', methods=('GET', 'POST'))
def start():
     #return render_template('auth.html')
     return render_template('index.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST' and request.form['op'] == 'saveimg':
        save_image_to_file("flaskr/RegUser/User1.jpg",request.form['file1'])
        save_image_to_file("flaskr/RegUser/User2.jpg",request.form['file2'])
        save_image_to_file("flaskr/RegUser/User3.jpg",request.form['file3'])
        New_User_Id = Add_Person("Andrea","01")
        Add_Images_to_single_person(New_User_Id)
        Train_Person_Group('user_db')
        return jsonify('ok')
    if request.method == 'POST' and request.form['op'] == 'reg_new_user':
        data = json.loads(request.form['user_data'])
        db = get_db()
        error = None

        if db.execute(
            'SELECT id FROM user WHERE email = ?', (data['email'],)
        ).fetchone() is not None:
            error = 'Email {} is already registered.'.format(data['email'])

        if error is None:
            db.execute(
                'INSERT INTO user (uname, ulast, email, birthday, addr, social, interest, music) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (data['uname'], data['ulast'], data['email'], data['birthday'], data['addr'],json.dumps(data['social']),json.dumps(data['interest']),json.dumps(data['music']))
            )
            db.commit()
            row_id = get_last_row(db)
        else:
            return jsonify(error)

        if request.form['img_loaded'] == 1:
            save_image_to_file("flaskr/RegUser/User1.jpg",request.form['file1'])
            save_image_to_file("flaskr/RegUser/User2.jpg",request.form['file2'])
            save_image_to_file("flaskr/RegUser/User3.jpg",request.form['file3'])
            New_User_Id = Add_Person(data['uname'],row_id)
            Add_Images_to_single_person(New_User_Id)
            Train_Person_Group('user_db') 
            db.execute(
                'UPDATE user SET face_id=? WHERE id =?',
                (New_User_Id,row_id)
            )
            db.commit()

        return jsonify('ok')

            #return redirect(url_for('auth.start'))
        
        #flash(error)


    return render_template('auth/register_v2.html')

@bp.route('/login_face', methods=('GET', 'POST'))
def login_face():
    if request.method == 'POST':
        filename='flaskr/LogUser/Test_User.jpg'
        #biteimg = bytes(request.form['file'],encoding="ascii")
        biteimg = request.form['file'].encode()
        imgdata = biteimg[biteimg.find(b'/9'):]
       # im = Image.open(io.BytesIO(base64.b64decode(imgdata))).save(filename)

        Id_User_Verified = Identify_User()
       # Id_User_Verified =  [file for file in glob.glob('./flaskr/LogUser/*.jpg')]
        #Id_User_Verified = cwd = os.getcwd()
        return jsonify(Id_User_Verified)
    return render_template('auth/login_face_revised.html')

@bp.route('/login_voice', methods=('GET', 'POST'))
def login_voice():
    if request.method == 'POST':
        return jsonify(request.form['userID'], request.form['file'])
    return render_template('auth/login_voice_revised.html')
