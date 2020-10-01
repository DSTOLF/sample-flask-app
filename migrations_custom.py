#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from models import db, Models, app
from faker import Faker
from random import randint
import re

fake = Faker('pt_BR')

COMPANIES_LIST = [
        {'nomeempresa'      : 'Delphix Brasil', 
          'email'           : 'demo@delphix.com',
          'fone'            : fake.phone_number(),
          'documento_fiscal': '25.530.832/0001-40',  
          'endereco'        : 'Avenida Das Nacoes Unidas, 14171 - 15 andar',
          'bairro'          : 'Vila Gertrudes',
          'cep'             : '04794-000',
          'cidade'          : 'São Paulo',
          'estado'          : 'SP',
          'pais'            : 'BR'},
        {'nomeempresa'      : 'Indústria e Serviços Limitados', 
          'email'           : 'faleconosco@br.isl.com',
          'fone'            : fake.phone_number(),
          'documento_fiscal': '33.372.251/0001-56',  
          'endereco'        : 'Rua Tutoia, 1157',
          'bairro'          : 'Vila Mariana',
          'cep'             : '04007-900',
          'cidade'          : 'São Paulo',
          'estado'          : 'SP',
          'pais'            : 'BR'},
        {'nomeempresa'      : 'Indústria e Serviços Limitados', 
          'email'           : 'faleconosco@br.isl.com',
          'fone'            : fake.phone_number(),
          'documento_fiscal': '33372251012839',  
          'endereco'        : 'Rua Tutoia, 1157',
          'bairro'          : 'Vila Mariana',
          'cep'             : '04007-900',
          'cidade'          : 'São Paulo',
          'estado'          : 'SP',
          'pais'            : 'BR'},
        {'nomeempresa'      : 'Indústria e Serviços Limitados', 
          'email'           : 'faleconosco@br.isl.com',
          'fone'            : fake.phone_number(),
          'documento_fiscal': '33.372.251/0126-77',  
          'endereco'        : 'Rua Tutoia, 1157',
          'bairro'          : 'Vila Mariana',
          'cep'             : '04007-900',
          'cidade'          : 'São Paulo',
          'estado'          : 'SP',
          'pais'            : 'BR'},
        {'nomeempresa'      : 'ARCOS DOURADOS COMERCIO DE ALIMENTOS LTDA', 
          'email'           : 'falaconosco@arcosdourados.com.br',
          'fone'            : fake.phone_number(),
          'documento_fiscal': '42.591.651/0001-43',  
          'endereco'        : 'Alameda Amazonas, 253',
          'bairro'          : 'Alphaville Industrial',
          'cep'             : '06454-070',
          'cidade'          : 'Barueri',
          'estado'          : 'SP',
          'pais'            : 'BR'},
        {'nomeempresa'      : 'ARCOS DOURADOS COMERCIO DE ALIMENTOS LTDA', 
          'email'           : 'falaconosco@arcosdourados.com.br',
          'fone'            : fake.phone_number(),
          'documento_fiscal': '42591651000305',  
          'endereco'        : 'Alameda Amazonas, 253',
          'bairro'          : 'Alphaville Industrial',
          'cep'             : '06454070',
          'cidade'          : 'Barueri',
          'estado'          : 'SP',
          'pais'            : 'BR'},
        {'nomeempresa'      : 'ARCOS DOURADOS COMERCIO DE ALIMENTOS LTDA', 
          'email'           : 'falaconosco@arcosdourados.com.br',
          'fone'            : fake.phone_number(),
          'documento_fiscal': '42591651/0002-24',  
          'endereco'        : 'Alameda Amazonas, 253',
          'bairro'          : 'Alphaville Industrial',
          'cep'             : '06454070',
          'cidade'          : 'Barueri',
          'estado'          : 'SP',
          'pais'            : 'BR'},
        {'nomeempresa'      : 'ARCOS DOURADOS COMERCIO DE ALIMENTOS LTDA', 
          'email'           : 'falaconosco@arcosdourados.com.br',
          'fone'            : fake.phone_number(),
          'documento_fiscal': '425916510004-96',  
          'endereco'        : 'Alameda Amazonas, 253',
          'bairro'          : 'Alphaville Industrial',
          'cep'             : '06454070',
          'cidade'          : 'Barueri',
          'estado'          : 'SP',
          'pais'            : 'BR'},
        {'nomeempresa'      : 'Lojas Artiodátilo', 
          'email'           : 'sac@artiodatilo.com.br',
          'fone'            : fake.phone_number(),
          'documento_fiscal': '09.055.134/0001-84',  
          'endereco'        : 'Avenida das Nações Unidas, 13797',
          'bairro'          : 'Vila Gertrudes',
          'cep'             : '04794-000',
          'cidade'          : 'São Paulo',
          'estado'          : 'SP',
          'pais'            : 'BR'},
        {'nomeempresa'      : 'Lojas Artiodátilo', 
          'email'           : 'sac@artiodatilo.com.br',
          'fone'            : fake.phone_number(),
          'documento_fiscal': '09.055.134/0005-08',  
          'endereco'        : 'Avenida Cem S/N, Sala 154',
          'bairro'          : 'Terminal Intermodal da Serra',
          'cep'             : '29161-384',
          'cidade'          : 'Serra',
          'estado'          : 'ES',
          'pais'            : 'BR'}
    ]

with app.app_context():
    # Reload tables
    # db.drop_all()
    db.create_all()
    for i in range(len(COMPANIES_LIST)):
        company = Models[0](**COMPANIES_LIST[i])
        db.session.commit()
        # Make 10 fake employees
        for i in range(10):
            emp_args = { 
                'nome': fake.first_name(), 
                'sobrenome': fake.last_name(), 
                'email': fake.free_email(), 
                'telefone': fake.phone_number() , 
                'endereco': fake.street_address(), 
                'codigo_postal': fake.postcode(), 
                'bairro': fake.bairro(),
                'cidade': fake.city(), 
                'estado': fake.estado_sigla(), 
                'pais': 'BR',  
                'documento_fiscal': fake.cpf(), 
                'documento_empresa': company.documento_fiscal
            }
            # Save in database
            employee = Models[1](**emp_args)
            db.session.commit()


