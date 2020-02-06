#!/bin/bash
export FLASK_APP=flaskr
export FLASK_ENV=development


flask init-db

#localhost 
#flask run

#externally visible
flask run --host=10.42.0.1 --cert=adhoc
