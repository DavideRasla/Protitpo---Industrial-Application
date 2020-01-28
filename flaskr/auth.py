import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
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
    return render_template('auth/Login_Face.html')

@bp.route('/login_voice', methods=('GET', 'POST'))
def login_voice():
    return render_template('auth/Login_Voice.html')


#### Testing ####

@bp.route('/hello', methods=['GET', 'POST'])
def hello():

    # POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        return 'OK', 200

    # GET request
    else:
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers



@bp.route('/test')
def test_page():
    # look inside `templates` and serve `index.html`
    return render_template('index.html')