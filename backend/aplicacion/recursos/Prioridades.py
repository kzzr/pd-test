
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, json, requests
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from aplicacion.modelos.Servicios import Servicios
from aplicacion.app import app_config, enviroment

class PrioridadesResource(Resource):
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
            rs = requests.request("GET", URL+"/priorities", headers=headers)
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

