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

bp = Blueprint('auth', __name__, url_prefix='/auth')

def get_last_row(db):
    cur = db.cursor()
    return cur.lastrowid

def save_image_to_file(img,img_data):
    filename=img
    biteimg = img_data.encode()
    imgdata = biteimg[biteimg.find(b'/9'):]
    im = Image.open(io.BytesIO(base64.b64decode(imgdata))).save(img)

def loadProfileByFaceId(id):
    db = get_db()
    db.execute(
        'SELECT * FROM user  WHERE face_id =?',
        (id)
    )
    row = db.cursor.fetcall()
    return row

def loadProfileByVoiceId(id):
    db = get_db()
    db.execute(
        'SELECT * FROM user  WHERE voice_id =?',
        (id)
    )
    row = db.cursor.fetcall()
    return row

def loadProfiles(fv,ids):
    for ids in ids:
        if fv == 0: #face
            data = loadProfileByFaceId(id)
        else:
            data = loadProfileByVoiceId(id)
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
        Train_Person_Group('users_db')
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
                'INSERT INTO user (uname, ulast, email, birthday, addr, premium, profession, social, interest, music) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (data['uname'], data['ulast'], data['email'], data['birthday'], data['addr'],data['premium'],data['profession'],json.dumps(data['social']),json.dumps(data['interest']),json.dumps(data['music']))
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
        im = Image.open(io.BytesIO(base64.b64decode(imgdata))).save(filename)

        Id_User_Verified = Identify_User()
        #Id_User_Verified =  [file for file in glob.glob('./flaskr/LogUser/*.jpg')]
        #Id_User_Verified = cwd = os.getcwd()
        return jsonify(Id_User_Verified)
    return render_template('auth/login_face_revised.html')

@bp.route('/login_voice', methods=('GET', 'POST'))
def login_voice():
    if request.method == 'POST':
        #return jsonify(request.form)
        #salvare il blob in wav nella cartella

        channels = 1
        sampwidth = 2
        framerate = 42000 


        name = 'flaskr/TestUserVoice/newrec.wav'
        audio = wave.open(name, 'wb')
        audio.setnchannels(channels)
        audio.setsampwidth(sampwidth)
        audio.setframerate(framerate)


        data = request.data
       
        audio.writeframes(data)
        audio.close()
        
        ListaUtenti = Get_All_Profiles()
        return identify_User_Voice(ListaUtenti)

    
 
    return render_template('auth/login_voice_revised.html')


@bp.route('/register_voice', methods=('GET', 'POST'))
def register_voice():
    if request.method == 'POST':
        #return jsonify(request.form)
        #salvare il blob in wav nella cartella

        channels = 1
        sampwidth = 2
        framerate = 42000 


        name = 'flaskr/EnrollUserVoice/newrec.wav'
        audio = wave.open(name, 'wb')
        audio.setnchannels(channels)
        audio.setsampwidth(sampwidth)
        audio.setframerate(framerate)


        data = request.data
       
        audio.writeframes(data)
        audio.close()

        New_User_ID_Voice = Add_User_Voice()
        Operation_ID_URL = Add_Enrollment_To_Single_Profile(New_User_ID_Voice)
        Result_Of_Enrollment = Get_Operation_Status(Operation_ID_URL)
        print("IL RISULTATO DELLA REGISTRAZIONE:",Result_Of_Enrollment) 

        return Result_Of_Enrollment
    return render_template('auth/register_v2.html')

@bp.route('/profile', methods=('GET', 'POST'))
def user_profile():
    #g.users = loadProfiles()
    g.users = [{
            'uname':'John','ulast':'Smith',
            'sx':'M',
            'email':'john.smith@fakemail.com',
            'addr':'via giordano bruno 8, Pisa',
            'profession':'plumber',
            'interest':['Technology','Sport','Travel','Boardgames'],
            'music':['Rock','Punk','Pop'],
            'social':['tw','inst'],
            'premium':0
        },
        {
            'uname':'Teabeany','ulast':'Stone',
            'sx':'F',
            'email':'bean85@fakemail.com',
            'addr':'dirty lake avenue 8, London',
            'profession':'IT counseling group',
            'interest':['Sport','Wine', 'Movie','Disco'],
            'music':['Pop','Classic'],
            'social':['inst','fb'],
            'premium':1
        }]
    return render_template('auth/user_profile.html')
    
