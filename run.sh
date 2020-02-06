#!/bin/bash
export FLASK_APP=flaskr
export FLASK_ENV=development


flask init-db

#localhost 
#flask run

#externally visible
flask run --host=0.0.0.0
