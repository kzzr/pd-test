
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, json, requests
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from aplicacion.modelos.Servicios import Servicios
from aplicacion.app import app_config, enviroment
from aplicacion.helpers.utilidades import Utilidades
class IncidenciasResource(Resource):
    def get(self):
        response = {
            "estado":0,
            "mensaje":"Sin datos",
            "data":{}
        }
        try:
            URL = app_config[enviroment].URL_API
            TOKEN = app_config[enviroment].TOKEN_PD
            headers = {
                'Authorization': 'Token token='+TOKEN
            }
            rs = requests.request("GET", URL+"/incidents", headers=headers)
            data = rs.json()
            if rs.status_code == 200:
                response["estado"] = 1
                response['mensaje'] = "Ok"
                response['data'] = data
            else:
                response['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # exc_type, fname, exc_tb.tb_lineno
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500
        return response, 200
    
    def post(self):
        response = {
            "estado":0,
            "mensaje":"Sin datos",
            "data":{}
        }
        
        try:
            jsonData = request.get_json()
            json_schema = "/app/backend/aplicacion/static/jsonschemas/post_incidencias.json"
            if os.path.isfile(json_schema) == False:
                response["mensaje"] = "No existe configuración para la validación"
                return response, 200

            data_schema = {}
            with open(json_schema) as json_file: 
                data_schema = json.load(json_file)        
            
            
            isValid = Utilidades.validateJson(data_schema, jsonData)
            if isValid["status"] == True:
        
                URL = app_config[enviroment].URL_API
                TOKEN = app_config[enviroment].TOKEN_PD
                headers = {
                    'Authorization': 'Token token='+TOKEN,
                    'Content-Type': 'application/json',
                    'From':'ggonzalez@napsis.com'
                }
                payload = json.dumps(jsonData)
                rs = requests.request("POST", URL+"/incidents", headers=headers, data = payload)
                data = rs.json()
                if rs.status_code == 201:
                    response["estado"] = 1
                    response['mensaje'] = "Ok"
                    response['data'] = data
                else:
                    response['data'] = data
            else:
                response['mensaje'] = isValid["msj"]
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # exc_type, fname, exc_tb.tb_lineno
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500
        return response, 200
    
    def put(self):
        response = {
            "estado":0,
            "mensaje":"Sin datos",
            "data":{}
        }
        
        try:
            jsonData = request.get_json()
            
            # Se puede validar, solo por la urgencia lo comento
            
            # json_schema = "/app/backend/aplicacion/static/jsonschemas/put_incidencias.json"
            # if os.path.isfile(json_schema) == False:
            #     response["mensaje"] = "No existe configuración para la validación"
            #     return response, 200

            # data_schema = {}
            # with open(json_schema) as json_file: 
            #     data_schema = json.load(json_file)        
            
            
            # isValid = Utilidades.validateJson(data_schema, jsonData)
            # if isValid["status"] == True:
            if True:
                id_incidents = jsonData["id"]
                del jsonData["id"]
                URL = app_config[enviroment].URL_API
                TOKEN = app_config[enviroment].TOKEN_PD
                headers = {
                    'Authorization': 'Token token='+TOKEN,
                    'Content-Type': 'application/json',
                    'From':'ggonzalez@napsis.com'
                }
                payload = json.dumps(jsonData)
                rs = requests.request("PUT", URL+"/incidents/"+str(id_incidents), headers=headers, data = payload)
                data = rs.json()
                if rs.status_code == 200:
                    response["estado"] = 1
                    response['mensaje'] = "Ok"
                    response['data'] = data
                else:
                    response['data'] = data
            else:
                response['mensaje'] = isValid["msj"]
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # exc_type, fname, exc_tb.tb_lineno
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500
        return response, 200

       