import sqlite3
import psycopg2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware #me permite habilitar origenes que hagan consultas al backened
from pydantic import BaseModel
#dpg-d0vp1cggjchc73a0mqkg-a hostname
#host 127.0.0.1
#ya me conecte a la bd queme dio render(visualizar en pgAdmin 4)
#Ahora tengo que hacer un crud aca para manejarla

#conexion local
"""conexion = psycopg2.connect(user='postgres',
                            password='18521945',
                            host='127.0.0.1',
                            port='5432',
                            dbname='productos'
)"""


#conexion en render(bd)

dsn = "postgresql://sosa:1bqN1W7bwlxQxnJmpFTAMXXqHFBBSlGR@dpg-d0vpfnvdiees73f3ngt0-a.oregon-postgres.render.com:5432/productospractica"
conexion = psycopg2.connect(dsn)

cursor = conexion.cursor()



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






"""cursor.execute("CREATE TABLE IF NOT EXISTS productos (id_producto INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, nombre TEXT, precio INTEGER, stock INTEGER)")

cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES(%s,%s,%s)", ("Tostadora", 35000, 100))
cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES(%s,%s,%s)", ("Estufa", 5000, 100))
cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES(%s,%s,%s)", ("Lampara", 7000, 100))
cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES(%s,%s,%s)", ("Cremona", 1000000, 100))"""

def insertarProductos(nombre,precio,stock):
    cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES(%s,%s,%s)", (nombre,precio,stock))
    conexion.commit()





def productos():
    cursor.execute("SELECT * FROM PRODUCTOS ")
    respuesta = cursor.fetchall()

    return transDic(respuesta)

#funcion para transformar las consultas a la bd en diccionarios 
def transDic(respuesta):
    dicProductos = []
    for i in respuesta:
        dicProductos.append({"nombre": i[1], "precio": i[2],  "stock": i[3]})#lo convierto en diccionario con claves-valor como si fuera un json


    return dicProductos


def verProductoId(id):
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id,))
    if (respuesta != []):
        return transDic(respuesta)
    else:
        return {"mensaje" : "no se han encontrado productos"}

def verProductosNombre(nombre):
    cursor.execute("SELECT * FROM productos WHERE nombre = %s", (nombre,))
    respuesta = cursor.fetchall()
    if (respuesta != []):
        return transDic(respuesta)
    else:
        return {"mensaje" : "no se han encontrado productos"}

def eliminarProducto(id):
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,))
    print("Eliminado exitosamente")
    conexion.commit()

def stock(id):
    cursor.execute("SELECT stock FROM productos WHERE id_producto = %s", (id,))
    respuesta = cursor.fetchall()

    st = respuesta[0][0]
    return st



def IncrementarStock(idProducto, restockeo):    
    cursor.execute("UPDATE productos SET stock = stock + %s WHERE id_producto = %s",(restockeo,idProducto) )
    print("el stock se ha actualizado(aumento)")

def restarStock(idProducto, restockeo):    
    cursor.execute("UPDATE productos SET stock = stock - %s WHERE id_producto = %s",(restockeo,idProducto) )
    print("el stock se ha actualizado(resto)")



#insertarProductos("Taladro", 2888, 1000)


@app.get("/")
async def main():
    answer = productos()
    return answer
    

#Uso pydantic para verificar que lo que recibo es el tipo de varibale que espero
class Producto(BaseModel):
    nombre: str
    precio: int
    stock: int



@app.post("/ingresar")
def recibirProducto(producto: Producto):
    nombre = producto.nombre
    precio = producto.precio
    stock = producto.stock

    insertarProductos(nombre,precio,stock)
    return {"mensaje":"se ha ingresado correctamente"}



#insertarProductos("ojeda", 122222, 12)


#print(productos())
#print(verProductoId(1))
#print(verProductosNombre("Taladro"))
#eliminarProducto(2)
#print(productos())
#IncrementarStock(1, 100)
#print(verProductoId(100))
#print(verProductosNombre("pionono"))
#restarStock(1,100)


