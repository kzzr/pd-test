#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,click,json

from aplicacion.enviroment import env
#Se establece enviroment como argumento
enviroment = env

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_restful import Api
from aplicacion.config import app_config
from aplicacion.db import db
from aplicacion.redis import redis
from aplicacion.helpers.utilidades import Utilidades
from aplicacion.recursos.Servicios import ServiciosResource
from aplicacion.recursos.Incidencias import IncidenciasResource
from aplicacion.recursos.Prioridades import PrioridadesResource
from aplicacion.recursos.Escalar import EscalarResource

# IMPORTACIÓN DE RECURSOS

app = Flask(__name__)
CORS(app)
db.init_app(app)


#Se setean variables de configuracion segun ambiente(env)
app.config.from_object(app_config[enviroment])
redis.init_app(app)
api = Api(app)

TOKEN = None
@app.before_request
def verifica_token():
    if request.method!='OPTIONS':
        rsps = {
            "estado":0,
            "mensaje":"",
            "data":{}
        }
        print(request.endpoint)
        try:
            if request.url.find('/static') >= 0:
                True
            
            elif request.endpoint not in  ['token']:
                if request.headers.get('Authorization'):
                    AUTHORIZATION = request.headers.get('Authorization').replace("Bearer ", "")
                    data_token = Utilidades.getToken()
                    valid_token = data_token["token"]
                    if valid_token != AUTHORIZATION:
                        rsps["mensaje"] = 'Acceso denegado, Token inválido code: 103'
                        rsps["log_datetime"] = str(data_token["log"])
                        return jsonify(rsps),403
                else:
                    rsps["mensaje"] = 'Acceso denegado, cliente sin autorizacion code: 101'
                    return jsonify(rsps),403
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # exc_type, fname, exc_tb.tb_lineno
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            print(msj)
            rsps["mensaje"] = 'Acceso denegado, Error en la verificación code: 104'
            return jsonify(rsps),403


# SE DEFINEN LOS ENDPOINTS Y LA CLASE QUE SE ENCARGARÁ DE PROCESAR CADA SOLICITUD
api.add_resource(ServiciosResource, '/servicios')
api.add_resource(IncidenciasResource, '/incidencias')
api.add_resource(PrioridadesResource, '/prioridades')
api.add_resource(EscalarResource, '/escalation_policies')

#Se carga host 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/token')
def token():
    rsps = {
            "estado":1,
            "mensaje": "OK",
            "data": Utilidades.getToken()
        }
    return jsonify(rsps),200

#Se carga host 
app.run(host='0.0.0.0',port=5014)
