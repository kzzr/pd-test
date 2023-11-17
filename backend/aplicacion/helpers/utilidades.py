import datetime
import hashlib
from jsonschema import validate, ValidationError

class Utilidades():

    @staticmethod
    def mayusculas(texto):
        try:
            return str(texto).upper()
        except Exception as e:
            return texto

    @staticmethod
    def formatoFecha(fecha):
        dia = str(fecha.day)
        dia = "0"+dia if len(dia) == 1 else dia
        mes = str(fecha.month)
        mes = "0"+mes if len(mes) == 1 else mes
        anio = str(fecha.year)
        fechaFormateada =  dia + "-" + mes + "-" + anio
        return fechaFormateada

    """
    Valida fecha en formato dd-mm-YYYY
    """
    @staticmethod
    def validarDate(date_text, formato):
        try:
            if str(date_text) != datetime.datetime.strptime(str(date_text), formato).strftime(formato):
                raise ValueError
            return True
        except ValueError:
            return False
    
    @staticmethod
    def getToken():
        date_format_str="%Y-%m-%d %H:%M:%S.%f"
        given_time = datetime.datetime.strptime(str(datetime.datetime.now()), date_format_str)
        final_time = given_time + datetime.timedelta(hours=-4)
        now = final_time.date()

        arr = bytes(str(now), 'utf-8')
        valid_token = hashlib.sha256(arr).hexdigest()
        data = {
            "token":valid_token,
            "log":final_time
        }
        return data
 
    
    @staticmethod
    def validateJson(jsonSchema, jsonData):
        rs = {}
        rs["status"] = True
        rs["msj"] = "OK"
        try:
            validate(instance=jsonData, schema=jsonSchema)
        except ValidationError as err:
            rs["status"] = False
            rs["msj"] = err.message
        return rs