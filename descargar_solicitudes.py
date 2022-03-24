from dotenv import load_dotenv
import os
import requests
import re
from base64 import b64decode
from datetime import date
from concurrent.futures import ProcessPoolExecutor
from liti_log import UtilLog

# C:\DocJairo\desarrollo\consumirApiPy\ve_cons\Scripts\activate


def crear_directorio(sDirectory):
    if not os.path.exists(sDirectory):
        os.mkdir(sDirectory)


class pdfs_radicaciones(object):
    """Obtiene los pdfs de una solicitud de radicaciones"""
    def __init__(self):
        # super(pdfs_radicaciones, self).__init__()
        crear_directorio('logs')
        self.path_logs = 'logs/'
        crear_directorio('pdfs')
        self.path_pdfs = 'pdfs/'
        # Para que funcionen los hilos NLS_LANG
        os.environ["NLS_LANG"] = "SPANISH_SPAIN.UTF8"
        load_dotenv()
        file_log = "descargar-pdfs-" + str(date.today()) + ".log"
        UtilLog.get_instance().set_file_name(self.path_logs + file_log)

        # self.local_path = os.environ.get('local_path')

        self.url = os.environ.get('url')
        self.username = os.environ.get('user_name')
        self.password = os.environ.get('password')
        self.usr_dicc = {
            'username': self.username,
            'password': self.password
        }
        self.token = ""

        print(f"url {self.url}")
        # print(f"local_path {self.local_path}")
        # print(f"init username {self.username}")
        # print(f"init usr_dicc {self.usr_dicc}")

    __instance = None
    Lista = []

    def __str__(self):
        return "pdfs_radicaciones Singleton "

    def __new__(cls):
        if not pdfs_radicaciones.__instance:
            pdfs_radicaciones.__instance = object.__new__(cls)
        return pdfs_radicaciones.__instance

    @staticmethod
    def get_instance():
        if not pdfs_radicaciones.__instance:
            pdfs_radicaciones.__instance = pdfs_radicaciones()
        return pdfs_radicaciones.__instance

    def autentication(self) -> str:
        endpoint = self.url + 'login/'
        # print(f'autentication username ({self.username})')
        # print(f'autentication password ({self.password})')
        # reponse=requests.post(endpoint, auth=(self.username,self.password))
        payload = self.usr_dicc
        reponse = requests.post(endpoint, json=payload)
        # print(f'autentication reponse.status_code {reponse.status_code}')
        # print(f'autentication despues json({reponse.json})')
        # print(f'autentication despues text({reponse.text})')
        if reponse.status_code == 200:
            reponse_json = reponse.json()
            # print(f"get_token json {reponse_json}")
            print(f"autentication token {reponse_json['token']}")
            self.token = reponse_json['token']

    def get_token(self):
        endpoint = self.url + 'refresh-token/'
        headers = {'Content-Type': 'application/json'}
        # ,params={'username',self.username}
        reponse = requests.get(endpoint, headers=headers, params={'username': self.username})
        print(f'get_token reponse.status_code {reponse.status_code}')
        # print(f'get_token reponse {reponse}')
        # reponse_text = reponse.text
        # print(f"get_token json {reponse_text}")

        reponse_json = reponse.json()
        # print(f"get_token json {reponse_json}")

        if reponse.status_code == 200:
            # print(f"get_token token {reponse_json['token']}")
            self.token = reponse_json['token']
            return self.token
        else:
            UtilLog.get_instance().write(f"get_token reponse_json {reponse_json}")

        if reponse_json['expired']:
            self.autentication()
            return self.token
        UtilLog.get_instance().write(reponse_json['error'])

    def getBase64ToPdf(self, nombre_archivo, b64):
        bytes = b64decode(b64, validate=True)

        if bytes[0:4] != b'%PDF':
            raise ValueError('Missing the PDF file signature')

        # Write the PDF contents to a local file
        f = open(self.path_pdfs + nombre_archivo, 'wb')
        f.write(bytes)
        f.close()

    def descargar_pdfs(self, radicacion_id):
        UtilLog.get_instance().write(f"descargar_pdfs radicacion_id {radicacion_id} ")
        endpoint = self.url + 'documentos/'
        token = 'Token ' + self.get_token()
        # print(f"descargar_pdfs " + "b" * 10)
        # token='Token c3a16a55b7ebdc559c65a0e17c58197dc719061f'
        headers = {'Content-Type': 'application/json; charset=UTF-8', 'Authorization': token}
        # reponse=requests.get(endpoint, params={'pk':2})
        # print(f"descargar_pdfs radicacion_id {radicacion_id}")
        reponse = requests.get(endpoint, headers=headers, params={'pk': radicacion_id})
        print(f'descargar_pdfs reponse.status_code {reponse.status_code}')
        # print(reponse)
        # print(reponse.url)
        reponse_list_json = reponse.json()
        # print(f"generar_pdfs list_json {reponse_list_json}")

        if reponse.status_code == 200:
            for json_item in reponse_list_json:
                # print(f"generar_pdfs nombre_archivo {json_item['nombre_archivo']}")
                UtilLog.get_instance().write(f"descargar_pdfs solicitud_id {radicacion_id} nombre_archivo {json_item['nombre_archivo']}")
                # UtilLog.get_instance().write(f"descargar_pdfs solicitud_id {radicacion_id} {json_item}")
                if json_item['error'] == 'ok':
                    self.getBase64ToPdf(json_item['nombre_archivo'], json_item['archivo_64'])
                else:
                    UtilLog.get_instance().write(f"descargar_pdfs solicitud_id {radicacion_id} {json_item}")
            return True
        else:
            UtilLog.get_instance().write(f"descargar_pdfs list_json {reponse_list_json}")
            return False

    def descargar_solicitud(self, radicacion_id):
        # Realiza dos intentos de descarga
        if not self.descargar_pdfs(radicacion_id):
            self.descargar_pdfs(radicacion_id)

    def solo_numeros(self, phrase):
        # Quita los caracteres especiales de las cadenas
        # print(f"quitarCaracteresEspeciales phrase {phrase}")
        allow = '0123456789'
        # print(f"quitarCaracteresEspeciales allow {allow}")
        cadena = re.sub('[^%s]' % allow, '', phrase)
        # print(cadena)
        # print(f"quitarCaracteresEspeciales cadena {cadena}")
        return cadena

    def getListaSolicitudes(self):
        # print(f"getListaSolicitudes {self.local_path}solicitudes.txt")
        lista = []
        # with open(self.local_path + "solicitudes.txt", encoding="utf-8") as fname:
        with open("solicitudes.txt", encoding="utf-8") as fname:
            for solicitud in fname:
                solicitud = self.solo_numeros(solicitud)
                print(f"solicitud ({str(solicitud)})")
                lista.append(solicitud)
        return lista

    def procesar_solicitudes(self):
        lista_solicitudes = self.getListaSolicitudes()
        for solicitud in lista_solicitudes:
            self.descargar_pdfs(solicitud)

    def procesar_solicitudes_hilos(self):
        # print("procesar_solicitudes __name__ ({__name__})")
        if __name__ == '__main__':
            lista_solicitudes = self.getListaSolicitudes()
            cores = int(os.cpu_count() / 2 + 1)
            # UtilLog.get_instance().write("Nucleos a utilizar " + str(cores) + "/" + str(os.cpu_count()))
            UtilLog.get_instance().write(f"lista_solicitudes cantidad {str(len(lista_solicitudes))}")
            with ProcessPoolExecutor(max_workers=cores) as executor:
                [executor.map(self.descargar_solicitud, lista_solicitudes)]

    def run(self):
        # print("Inicio")
        self.autentication()
        # self.get_token()
        # self.descargar_pdfs(2540)
        # self.procesar_solicitudes()
        self.procesar_solicitudes_hilos()


pdfs_radicaciones().run()
