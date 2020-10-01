#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import RelationshipProperty
from sqlalchemy import inspect
from models import db, Models, app
from faker import Faker
from random import randint
from sqlalchemy.schema import MetaData
import re

arglist={}

meta=MetaData()
meta.reflect(bind=db.engine)

processed = []

# def is_foreign_key(table_name, col_name):
#     return table_name+"."+col_name in [e.target_fullname for e in meta.tables[table_name].foreign_keys]

def add_model_instance(model_class, amount=10, parent=None):
    # print(model_class.__name__)
    with app.app_context():
        insp = inspect(model_class)
        insp=inspect(model_class)
        children=[]
        child={}
        has_parent=False
        has_child=False
        insp=inspect(model_class)
        fk_column = ""
        parent_column = ""
        for prop in insp.iterate_properties:
            if isinstance(prop, RelationshipProperty):
                if prop.direction.__str__()=="symbol('ONETOMANY')":
                    has_child=True
                    child=prop.argument()
                    children.append(child)
                if (parent and prop.direction.__str__()=="symbol('MANYTOONE')"):
                    for e in meta.tables[model_class.__tablename__].foreign_keys:
                        has_parent=True
                        fk_column = e.parent.__str__().split(".")[1] # foreign key column
                        parent_column = e.target_fullname.split(".")[1] # parent column
        for i in range(amount):
            arglist={}
            for attr in filter(lambda x: x.name != "id", insp.c):
                # if is_foreign_key(model_class.__tablename__, attr.name):
                #     arglist[attr.name]=getattr(parent, )
                if (attr.name == fk_column and has_parent):
                    arglist[attr.name]=getattr(parent, parent_column)
                    continue
                fakerMethod=attr.doc.split('-')[0]
                fakerLocale=attr.doc.split('-')[1]
                fake = Faker(fakerLocale)
                arglist[attr.name]=getattr(fake, fakerMethod)()
            new_object=model_class(**arglist)
            db.session.commit()
            if (has_child):
                add_model_instance(child, amount, new_object )
    processed.append(model_class.__name__)

with app.app_context():
    # Reload tables
    # db.drop_all()
    db.create_all()

for model_class in Models:
    if model_class.__name__ in processed:
        continue
    add_model_instance(model_class=model_class)
    

# print(dir(Models[0]))


# if model_class.__name__ in processed:
#         return 1


