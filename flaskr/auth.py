import functools
import base64
import io
from PIL import Image


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify,
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/start', methods=('GET', 'POST'))
def start():
     #return render_template('auth.html')
     return render_template('index.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        uname = request.form['uname']
        ulast = request.form['ulast']
        email = request.form['email']
        db = get_db()
        error = None

        if db.execute(
            'SELECT id FROM user WHERE email = ?', (email,)
        ).fetchone() is not None:
            error = 'Email {} is already registered.'.format(email)

        if error is None:
            db.execute(
                'INSERT INTO user (uname, ulast, email) VALUES (?, ?, ?)',
                (uname, ulast, email)
            )
            db.commit()
            return redirect(url_for('auth.start'))

        flash(error)


    return render_template('auth/register_v2.html')

@bp.route('/login_face', methods=('GET', 'POST'))
def login_face():
    if request.method == 'POST':
        filename='user_login.jpeg'
        #biteimg = bytes(request.form['file'],encoding="ascii")
        biteimg = request.form['file'].encode()
        imgdata = biteimg[biteimg.find(b'/9'):]
        im = Image.open(io.BytesIO(base64.b64decode(imgdata))).save(filename)
        return jsonify(request.form['userID'], request.form['file'])
    return render_template('auth/login_face_revised.html')

@bp.route('/login_voice', methods=('GET', 'POST'))
def login_voice():
    if request.method == 'POST':
        return jsonify(request.form['userID'], request.form['file'])
    return render_template('auth/login_voice_revised.html')