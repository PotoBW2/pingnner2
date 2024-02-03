import sys
import os
from bdatos import obtener_direccion

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def calcular_ping(raiz, id, nombre):
    while raiz.tv_servidores.condicional:
        direccion = bdatos.obtener_direccion(nombre)
        tiempo_de_espera = ping_en_profundidad(raiz.tv_servidores.hilos[id]["pings"], direccion)
        pinear2(raiz, id)
        eliminar_pings_vencidos(raiz.tv_servidores.hilos[id]["pings"])
        esperar(tiempo_de_espera)