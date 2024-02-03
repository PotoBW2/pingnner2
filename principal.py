from tkinter import *
from tkinter import ttk
from bdatos import cargar_servidores, cargar_hijos_que_no_son_padre, guardar_pin, maximo_ping, minimo_ping, \
    promedio_ping, perdida_ping, reiniciar_pines, buscar_padre, primera_desconexion, guardar_primera_desconexion
import threading
from utiles import resource_path
from ping3 import ping
from time import sleep, time

raiz = Tk()
raiz.title("Pingnner v2.00")
raiz.resizable(False, False)
raiz.iconbitmap(resource_path("image/logo2.ico"))

f_principal = ttk.Frame(raiz, padding=10, )
f_principal.grid()

reiniciar_pines()

raiz.tv_servidores = ttk.Treeview(f_principal, columns=("name", 'PROM', 'MAX', 'MIN', 'LOST'))
raiz.tv_servidores.grid(column=0, row=0)
raiz.tv_servidores.heading('name', text='Nombre')
raiz.tv_servidores.heading('PROM', text='Promedio')
raiz.tv_servidores.heading('MAX', text='Máximo')
raiz.tv_servidores.heading('MIN', text="Mínimo")
raiz.tv_servidores.heading('LOST', text="Pérdida")
raiz.tv_servidores.column('#0', width=35, )
raiz.tv_servidores.column('name', width=120)
raiz.tv_servidores.column('PROM', width=60)
raiz.tv_servidores.column('MAX', width=55)
raiz.tv_servidores.column('MIN', width=50)
raiz.tv_servidores.column('LOST', width=50)

for elem in cargar_servidores():
    raiz.tv_servidores.insert('', 'end', str(elem[0]), text=str(elem[0]),
                              values=(elem[1], "---", "---", "---", "---"))

def pineador(tupla):
    pin = ping(tupla[2], timeout=4)
    if type(pin) in (float, int):
        pin = round(pin, 3) * 1000
    else:
        pin = None
    inicio = time()
    guardar_pin(pin, tupla[0])
    raiz.tv_servidores.set(tupla[0], 'PROM', str(promedio_ping(tupla[0])) + "ms")
    raiz.tv_servidores.set(tupla[0], 'MAX', str(maximo_ping(tupla[0])) + "ms")
    raiz.tv_servidores.set(tupla[0], 'MIN', str(minimo_ping(tupla[0])) + "ms")
    raiz.tv_servidores.set(tupla[0], 'LOST', str(perdida_ping(tupla[0])) + "%")
    if pin == None:
        padre = buscar_padre(tupla[3])
        if padre:
            if not pineador(padre) == None:
                if primera_desconexion(tupla[0]):
                    print("No conectado: "+str(tupla[1]))
                guardar_primera_desconexion(tupla[0], False)
    else:
        guardar_primera_desconexion(tupla[0], True)
    final = time()
    espera = final - inicio
    return espera, pin
def sondeo(raiz):
    hp = cargar_hijos_que_no_son_padre()
    while True:
        for elem in hp:
            espera, pin = pineador(elem)
            if pin:
                espera = 4 - ((pin/1000)+(espera))
            else:
                espera = 4
            if espera > 0:
                sleep(espera)

hilo = threading.Thread(name="comprobacion", target=lambda: sondeo(raiz), daemon=True)
hilo.start()



raiz.update()
raiz.geometry("+" + str(round(raiz.winfo_screenwidth() / 2 - raiz.winfo_reqwidth() / 2)) + "+" + str(
    round(raiz.winfo_screenheight() / 2 - raiz.winfo_reqheight() / 2)))
raiz.update()

raiz.mainloop()
