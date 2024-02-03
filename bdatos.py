import sqlite3 as sql

SERVIDOR = "datadb.db"

def cargar_servidores():
    conn = sql.connect("datadb.db")
    cursor = conn.cursor()
    instruccion = f"SELECT id,nombre FROM servidores;"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos


def cargar_hijos_que_no_son_padre():
    conn = sql.connect("datadb.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM servidores WHERE id NOT IN (SELECT padre FROM servidores WHERE padre is not null GROUP BY padre)"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos

def obtener_direccion(nombre_servidor):
    conn = sql.connect("datadb.db")
    cursor = conn.cursor()
    instruccion2 = "SELECT direccion FROM servidores WHERE name =" + str(nombre_servidor) + ";"
    cursor.execute(instruccion2)
    datos2 = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos2

def guardar_pin(pin,servidor):
    conn = sql.connect("datadb.db")
    cursor = conn.cursor()
    if pin:
        instruccion = f"INSERT INTO pings (ping, id_servidor) VALUES ("+str(pin)+", "+str(servidor)+");"
    else:
        instruccion = f"INSERT INTO pings (id_servidor) VALUES (" + str(servidor) + ");"
    instruccion2 = f"SELECT count(*) FROM pings WHERE id_servidor = "+str(servidor)
    cursor.execute(instruccion)
    cursor.execute(instruccion2)
    datos2 = cursor.fetchall()
    if datos2[0][0] > 15:
        instruccion3 = f"SELECT min(id) FROM pings WHERE id_servidor = " + str(servidor)
        cursor.execute(instruccion3)
        datos3 = cursor.fetchall()[0][0]
        instruccion4 = f"DELETE FROM pings WHERE id =" + str(datos3)
        cursor.execute(instruccion4)
    conn.commit()
    conn.close()

def maximo_ping(id):
    conn = sql.connect("datadb.db")
    cursor = conn.cursor()
    instruccion2 = "SELECT max(ping) FROM pings WHERE id_servidor =" + str(id) + ";"
    cursor.execute(instruccion2)
    datos2 = cursor.fetchall()
    conn.commit()
    conn.close()
    if datos2[0][0]:
        return datos2[0][0]
    return "---"

def minimo_ping(id):
    conn = sql.connect("datadb.db")
    cursor = conn.cursor()
    instruccion2 = "SELECT min(ping) FROM pings WHERE id_servidor =" + str(id) + ";"
    cursor.execute(instruccion2)
    datos2 = cursor.fetchall()
    conn.commit()
    conn.close()
    if datos2[0][0]:
        return datos2[0][0]
    return "---"

def promedio_ping(id):
    conn = sql.connect("datadb.db")
    cursor = conn.cursor()
    instruccion = "SELECT ping FROM pings WHERE id_servidor =" + str(id) + " AND ping is not null;"
    instruccion2 = "SELECT count(*) FROM pings WHERE id_servidor =" + str(id) + ";"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    cursor.execute(instruccion2)
    cant = cursor.fetchall()[0][0]
    sum = 0
    for elem in datos:
        sum = sum + elem[0]
    if sum != 0:
        prom = round(sum / cant)
    else:
        prom = "---"
    conn.commit()
    conn.close()
    return prom

def perdida_ping(id):
    conn = sql.connect("datadb.db")
    cursor = conn.cursor()
    instruccion = "SELECT count(*) FROM pings WHERE id_servidor =" + str(id) + " AND ping is null;"
    instruccion2 = "SELECT count(*) FROM pings WHERE id_servidor =" + str(id) + ";"
    cursor.execute(instruccion)
    perdida = cursor.fetchall()[0][0]
    cursor.execute(instruccion2)
    cant = cursor.fetchall()[0][0]
    porcentaje = round(perdida/cant*100)
    conn.commit()
    conn.close()
    return porcentaje

def reiniciar_pines():
    conn = sql.connect("datadb.db")
    cursor = conn.cursor()
    instruccion = "DELETE FROM pings;"
    instruccion2 = "UPDATE servidores SET sonido_conexion_primero = "+str(0)+";"
    cursor.execute(instruccion)
    cursor.execute(instruccion2)
    conn.commit()
    conn.close()

def buscar_padre(id):
    conn = sql.connect("datadb.db")
    cursor = conn.cursor()
    if id:
        instruccion2 = "SELECT * FROM servidores WHERE id =" + str(id) + ";"
        cursor.execute(instruccion2)
        resp = cursor.fetchall()[0]
    else:
        resp = None
    conn.commit()
    conn.close()
    return resp

def primera_desconexion(id):
    conn = sql.connect("datadb.db")
    cursor = conn.cursor()
    instruccion2 = "SELECT sonido_conexion_primero FROM servidores WHERE id =" + str(id) + ";"
    cursor.execute(instruccion2)
    resp = cursor.fetchall()[0][0]
    if resp == 1:
        resp = True
    else:
        resp = False
    conn.commit()
    conn.close()
    return resp

def guardar_primera_desconexion(id,valor):
    conn = sql.connect("datadb.db")
    cursor = conn.cursor()
    if valor:
        valor = 1
    else:
        valor = 0
    instruccion2 = "UPDATE servidores SET sonido_conexion_primero = "+str(valor)+" WHERE id =" + str(id) + ";"
    cursor.execute(instruccion2)
    conn.commit()
    conn.close()