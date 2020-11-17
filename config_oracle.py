#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

app_environment=os.getenv("app_environment", "Production")
api_prefix=os.getenv("API_PREFIX", "/")
database_user = os.getenv("DATABASE_USER")
database_password=os.getenv("DATABASE_PASSWORD")
database_host=os.getenv("DATABASE_HOST")
database_name=os.getenv("DATABASE_NAME")
database_port=os.getenv("DATABASE_PORT")

class Config(object):
    debug = False
    # SQLALCHEMY_DATABASE_URI = ('sqlite:///teste.db')
    # SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(database_user,database_password,database_host,database_port,database_name)
    SQLALCHEMY_DATABASE_URI = "oracle+cx_oracle://{}:{}@{}:{}/?service_name={}".format(database_user,database_password,database_host,database_port,database_name)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def environment_display(env):
    switcher ={ 
        'Production': ['united', 'bootstrap2'],
        'Masked': ['cosmo', 'bootstrap2'],
        'Break-Fix': ['united', 'bootstrap2'],
        'Dev': ['cerulean', 'bootstrap3'],
        'Synthetic-Data': ['cerulean', 'bootstrap3'],
        'QA': ['spacelab', 'bootstrap2']
    }
    return switcher.get(env, "")


app_theme = environment_display(app_environment)[0]
app_bootstrap = environment_display(app_environment)[1]
