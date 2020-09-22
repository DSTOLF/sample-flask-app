#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  This demo application demonstrates the functionality of the safrs documented REST API
  After installing safrs with pip, you can run this app standalone:
  $ python3 demo_relationship.py [Listener-IP]
  This will run the example on http://Listener-Ip:5000
  - A database is created and a user is added
  - A rest api is available
  - swagger documentation is generated
"""
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
try:
    from flask_admin import Admin
    from flask_admin.contrib import sqla
except:
    print("Failed to import flask-admin")
from safrs import SAFRSBase, SAFRSAPI, SAFRSRestAPI
from models import db, Models
from config import api_prefix, app_theme, app_bootstrap, app_environment
import os
from safrs.api_methods import search, startswith, duplicate  # rpc methods




db = SQLAlchemy()

# This html will be rendered in the swagger UI
description = """
<a href=http://jsonapi.org>Json:API</a> compliant API built with https://github.com/thomaxxl/safrs <br/>
- <a href="https://github.com/thomaxxl/safrs/blob/master/examples/demo_pythonanywhere_com.py">Source code of this page</a><br/>
- <a href="/ja/index.html">reactjs+redux frontend</a>
- <a href="/admin/person">Flask-Admin frontend</a>
- Auto-generated swagger spec: <a href=/api/swagger.json>swagger.json</a><br/>
- <a href="/swagger_editor/index.html?url=/api/swagger.json">Swagger2 Editor</a> (updates can be added with the SAFRSAPI "custom_swagger" argument)
"""

def create_api(app, HOST="localhost", PORT=5000, API_PREFIX=api_prefix):
    
    # Add startswith methods so we can perform lookups from the frontend
    SAFRSBase.startswith = startswith
    # Needed because we don't want to implicitly commit when using flask-admin
    SAFRSBase.db_commit = False
    api = SAFRSAPI(app, host=HOST, port=PORT, prefix=API_PREFIX)
    for model in Models:
        dir(model)
        api.expose_object(model)
    # see if we can add the flask-admin views
    try:
        admin = Admin(app,name=app_environment, url="/admin",  template_mode=app_bootstrap)
        for model in Models:
            admin.add_view(sqla.ModelView(model, db.session))
    except Exception as exc:
        print(f"Failed to add flask-admin view {exc}")
    print("Starting API: http://{}:{}/{}".format(HOST, PORT, API_PREFIX))


def create_app(config_filename=None, host="localhost/"):
    app = Flask(__name__)
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config.from_object("config.Config")
    app.config['FLASK_ADMIN_SWATCH'] = app_theme
    # prod - united
    # masked - cosmo
    # break-fix - united
    # dev - cerulean 
    # qa - spacelab

    db.init_app(app)

    with app.app_context():
        create_api(app, host)
    return app

# address where the api will be hosted, change this if you're not running the app on localhost!
host = sys.argv[1] if sys.argv[1:] else "0.0.0.0"
app = create_app(host=host)

if __name__ == "__main__":
    app.run(host=host)
