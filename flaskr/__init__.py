import os

from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

def create_app(test_cfg = None):
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    if test_cfg is None:
        app.config.from_pyfile('config.py', silent=True)
    else: 
         app.config.from_mapping(test_cfg)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/')
    def st():
        return redirect(url_for('auth.start'))
    
    #@app.after_request
    #def apply_caching(response):
    #    response.headers["X-Frame-Options"] = "allow-from https://www.google.com/*"
    #    response.headers['Access-Control-Allow-Origin'] = '*'
    #    return response

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import api
    app.register_blueprint(api.bp)
    return app