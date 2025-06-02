import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware #me permite habilitar origenes que hagan consultas al backened

#tengo que crear una cadena de origenes permitidos

app = FastAPI()


origenes = ["http://127.0.0.1:5500",
            "https://pagina-practica.vercel.app"
] 

#el origen de la pagina que va a realizar la consulta

app.add_middleware(
    CORSMiddleware,
    allow_origins = origenes, #los origenes que tengo permitidos en la lista
    allow_methods = ["*"], # permito consultar por todos los metodos (get, post, put, delete)
    allow_credentials = False, #no necesito credenciales, lo pongo para no olvidarme
    allow_headers = ["*"], #permite todos los headers ¿que es un header?
)




conexion = sqlite3.connect("supermerk2.db")
cursor = conexion.cursor()

cursor.execute("CREATE TABLE IF NOt EXISTS productos (id_producto INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, precio INTEGER, stock INTEGER)")

"""cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES(?,?,?)", ("Tostadora", 35000, 100))
cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES(?,?,?)", ("Estufa", 5000, 100))
cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES(?,?,?)", ("Lampara", 7000, 100))
cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES(?,?,?)", ("Cremona", 1000000, 100))"""

res = cursor.execute("SELECT * FROM PRODUCTOS ")
respuesta = res.fetchall()
conexion.commit()


def productos():
    res = cursor.execute("SELECT nombre, precio FROM productos")
    respuesta = res.fetchall()

    dicProductos = []
    for i in respuesta:
        dicProductos.append({"nombre": i[0], "precio": i[1]})#lo convierto en diccionario con claves-valor como si fuera un json


    return dicProductos





@app.get("/")
async def main():
    answer = productos()
    return answer

print(productos())