import mysql.connector
import pymongo
from bson import json_util, ObjectId
from flask import current_app as app

class Producto:
    @staticmethod
    def obtener_productos():
        conn = None
        try:
            conn = mysql.connector.connect(**app.config['MYSQL_CONNECTION'])
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()
            return productos
        except mysql.connector.Error as err:
            print(f"Error al obtener productos: {err}")
            return []
        finally:
            if conn.is_connected():
                conn.close()

    @staticmethod
    def agregar_producto(data):
        conn = None
        try:
            conn = mysql.connector.connect(**app.config['MYSQL_CONNECTION'])
            cursor = conn.cursor()
            cursor.execute("INSERT INTO productos (nombre, descripcion, categoria) VALUES (%s, %s, %s)", (data['nombre'], data['descripcion'], data['categoria']))
            conn.commit()
            return {"mensaje": "Producto agregado exitosamente"}
        except mysql.connector.Error as err:
            print(f"Error al agregar producto: {err}")
            return {"mensaje": "Error al agregar el producto"}
        finally:
            if conn.is_connected():
                conn.close()

class Inventario:
    def __init__(self):
        self.client = pymongo.MongoClient(app.config['MONGO_URI'])
        self.db = self.client[app.config['MONGO_DBNAME']]
        self.coleccion = self.db["inventario"]

    def obtener_inventario(self):
        try:
            inventario = list(self.coleccion.find())
            return json_util.loads(json_util.dumps(inventario))
        except pymongo.errors.PyMongoError as err:
            print(f"Error al obtener inventario: {err}")
            raise

    def agregar_a_inventario(self, data):
        try:
            if 'entregado' not in data:
                data['entregado'] = False
            resultado = self.coleccion.insert_one(data)
            return {"mensaje": "Inventario creado exitosamente", "id_inventario": str(resultado.inserted_id)}
        except pymongo.errors.PyMongoError as err:
            print(f"Error al agregar al inventario: {err}")
            raise

    def actualizar_inventario(self, id_inventario, data):
        try:
            # Obtener el documento de inventario por su ID
            inventario = self.coleccion.find_one({"_id": ObjectId(id_inventario)})
            if inventario:
                # Actualizar el campo "entregado" del inventario
                campos_actualizados = {}
                if 'entregado' in data:
                    campos_actualizados['entregado'] = data['entregado']
                resultado = self.coleccion.update_one(
                    {"_id": ObjectId(id_inventario)},
                    {"$set": campos_actualizados}
                )
                return resultado.modified_count > 0
            return False
        except pymongo.errors.PyMongoError as err:
            print(f"Error al actualizar el inventario: {err}")
            raise