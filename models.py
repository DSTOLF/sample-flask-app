#!/usr/bin/env python3
# -*- coding: utf-8 -*-



from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from safrs import SAFRSBase, SAFRSAPI
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


app = Flask(__name__)
app.config.from_object("config.Config")
db = SQLAlchemy(app)

class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

Models = []

with open("models.yaml", 'r') as stream:
    try:
        model_list = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        sys.exit("Error loading YAML: "+exc)

for class_name,class_def in model_list.items():
    model = Struct(**class_def)
    print("Loading Model Class - "+class_name)
    class_attrs = {}
    for column_name, column_attrs in model.columns.items():
        class_attrs[column_name]=db.Column(getattr(db, column_attrs['data_type'])(column_attrs['data_size']) if 'data_size' in column_attrs  else getattr(db, column_attrs['data_type']),
                                            db.ForeignKey(column_attrs['foreign_key'])if 'foreign_key' in column_attrs  else None,
                                            primary_key=column_attrs['primary_key'] if 'primary_key' in column_attrs else False,
                                            unique = column_attrs['unique'] if 'unique' in column_attrs  else False,
                                            index = column_attrs['index'] if 'index' in column_attrs  else False,
                                            nullable = column_attrs['nullable'] if 'nullable' in column_attrs else True,
                                            doc = column_attrs['doc'] if 'doc' in column_attrs  else None,
                                            )
        if 'identity' in column_attrs  and column_attrs['identity']:
            f = column_name
            class_attrs["doc"]=f
            class_attrs["__repr__"] = lambda cls: '%r' % getattr(cls, getattr(cls, 'doc'))
            class_attrs["__str__"] = lambda cls: '%s' % getattr(cls, getattr(cls, 'doc'))
    if ('relationships' in dir(model)):
        for relation_name, relation_attrs in model.relationships.items():
            class_attrs[relation_name] = db.relationship(relation_attrs['related_class'], 
                                                     back_populates=relation_attrs['back_populates'],
                                                     lazy = relation_attrs['lazy'] if 'lazy' in relation_attrs  else None)

      
    new_class = type(class_name,
                    (SAFRSBase, db.Model),
                    class_attrs)
    Models.append(new_class)

    