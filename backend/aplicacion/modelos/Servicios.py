# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Float, Integer, LargeBinary, String, Table, Text
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


import os, sys, json
from aplicacion.db import db


class Servicios(db.Model):
    __tablename__ = 'cliente'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    identificacion = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    razon_social = db.Column(db.String(150))
    activo = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    token_auth = db.Column(db.String(45), nullable=False)
    logo = db.Column(db.Text)
    url_web = db.Column(db.Text)
    id_pais = db.Column(db.Integer, primary_key=True, nullable=False, index=True)
    #CRUD

    @classmethod
    def get_data(cls, _id):
        query =  cls.query.filter_by(id=_id).first()
        return query

    @classmethod
    def insert_data(cls, dataJson):
        query = Cliente( 
            identificacion = dataJson['identificacion'],
            nombre = dataJson['nombre'],
            razon_social = dataJson['razon_social'],
            activo = dataJson['activo'],
            token_auth = dataJson['token_auth'],
            logo = dataJson['logo'],
            url_web = dataJson['url_web'],
            id_pais = dataJson['id_pais'],
            )
        Cliente.guardar(query)
        if query.id:                            
            return  query.id
        return  None

    @classmethod
    def update_data(cls, _id, dataJson):
        query = cls.query.filter_by(id=_id).first()
        if query:
            if 'identificacion' in dataJson:
                query.identificacion = dataJson['identificacion']
            if 'nombre' in dataJson:
                query.nombre = dataJson['nombre']
            if 'razon_social' in dataJson:
                query.razon_social = dataJson['razon_social']
            if 'activo' in dataJson:
                query.activo = dataJson['activo']
            if 'token_auth' in dataJson:
                query.token_auth = dataJson['token_auth']
            if 'logo' in dataJson:
                query.logo = dataJson['logo']
            if 'url_web' in dataJson:
                query.url_web = dataJson['url_web']
            if 'id_pais' in dataJson:
                query.id_pais = dataJson['id_pais']
            db.session.commit()
            if query.id:                            
                return query.id
        return  None

    @classmethod
    def delete_data(cls, _id):
        query = cls.query.filter_by(id=_id).first()
        if query:
            Cliente.eliminar(query)
            if query.id:                            
                return query.id
        return  None

    def guardar(self):
        db.session.add(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def checktoken(cls, token):
        datos = None
        try:
            sql =   f""" SELECT * FROM cliente WHERE token_auth = '{token}' AND activo = 1 """
            query = db.session.execute(sql)

            if query:
                for data in query:
                    datos = {
                        "id": data["id"],
                        "identificacion": data["identificacion"],
                        "nombre": data["nombre"],
                        "razon_social": data["razon_social"],
                        "activo": data["activo"],
                        "token_auth": data["token_auth"],
                        "logo": data["logo"],
                        "url_web": data["url_web"],
                        "id_pais": data["id_pais"],
                    }
                    break
            return datos

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            print(msj)
            return None
        
    
