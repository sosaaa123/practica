import sqlite3
from fastapi import FastAPI

app = FastAPI()

conexion = sqlite3.connect("supermerk2.db")
cursor = conexion.cursor()

cursor.execute("CREATE TABLE IF NOt EXISTS productos (id_producto INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, precio INTEGER, stock INTEGER)")

"""cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES(?,?,?)", ("Tostadora", 35000, 100))
cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES(?,?,?)", ("Estufa", 5000, 100))
cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES(?,?,?)", ("Lampara", 7000, 100))
cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES(?,?,?)", ("Cremona", 1000000, 100))"""

conexion.commit()