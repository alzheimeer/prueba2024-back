from flask import Flask, jsonify, request
import mysql.connector
import pymongo

from flask import jsonify
from bson import json_util, ObjectId

app = Flask(__name__)

# Configuración de MySQL
db_mysql = mysql.connector.connect(
    host="localhost",
    user="prueba",
    password="prueba2024",
    database="prueba2024"
)
cursor = db_mysql.cursor()

try:
    # Crear tabla de productos en MySQL
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(255),
        descripcion TEXT,
        categoria VARCHAR(100)
    )
    """)

    # Datos iniciales de prueba para la tabla de productos
    datos_prueba = [
        ('Tarjeta credito', 'Descripción de Tarjeta credito', 'Categoría A'),
        ('Cheque', 'Descripción del Cheque', 'Categoría B'),
        ('Talonario', 'Descripción del Talonario', 'Categoría A')
    ]

    # Insertar datos iniciales en la tabla de productos
    for dato in datos_prueba:
        cursor.execute("INSERT INTO productos (nombre, descripcion, categoria) VALUES (%s, %s, %s)", dato)
    db_mysql.commit()
except mysql.connector.Error as error:
    print(f"Error al crear la tabla o insertar datos: {error}")
finally:
    # Cerrar la conexión a MySQL
    cursor.close()
    db_mysql.close()

# Configuración de MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db_mongo = client["prueba2024"]
coleccion_inventario = db_mongo["inventario"]

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/productos', methods=['GET', 'POST'])
def gestionar_productos():
    try:
        db_mysql = mysql.connector.connect(
            host="localhost",
            user="prueba",
            password="prueba2024",
            database="prueba2024"
        )
        cursor = db_mysql.cursor()

        if request.method == 'GET':
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()
            productos_lista = []
            for producto in productos:
                producto_dict = {
                    "id": producto[0],
                    "nombre": producto[1],
                    "descripcion": producto[2],
                    "categoria": producto[3]
                }
                productos_lista.append(producto_dict)
            return jsonify(productos_lista)
        elif request.method == 'POST':
            data = request.get_json()
            nombre = data['nombre']
            descripcion = data['descripcion']
            categoria = data['categoria']
            cursor.execute("INSERT INTO productos (nombre, descripcion, categoria) VALUES (%s, %s, %s)", (nombre, descripcion, categoria))
            db_mysql.commit()
            return jsonify({"mensaje": "Producto agregado exitosamente"})
    except mysql.connector.Error as error:
        print(f"Error al gestionar productos: {error}")
        return jsonify({"error": "Error al gestionar productos"}), 500
    finally:
        # Cerrar la conexión a MySQL
        cursor.close()
        db_mysql.close()

@app.route('/inventario', methods=['GET', 'POST', 'PUT'])
def gestionar_inventario():
    try:
        if request.method == 'GET':
            inventario = list(coleccion_inventario.find())
            inventario_json = json_util.dumps(inventario)
            return inventario_json
        elif request.method == 'POST':
            datos = request.get_json()
            nuevo_inventario = {
                "nombre_de_usuario": datos["nombre_de_usuario"],
                "producto": datos["producto"],
                "numero_de_serie": datos["numero_de_serie"],
                "fecha_ingreso": datos["fecha_ingreso"],
                "entregado": False
            }
            resultado = coleccion_inventario.insert_one(nuevo_inventario)
            return jsonify({
                "mensaje": "Inventario creado exitosamente",
                "id_inventario": str(resultado.inserted_id)
            })
        elif request.method == 'PUT':
            datos = request.get_json()
            id_inventario = datos["id_inventario"]
            coleccion_inventario.update_one({"_id": ObjectId(id_inventario)}, {"$set": {"entregado": True}})
            return jsonify({"mensaje": "Inventario actualizado exitosamente"})
    except pymongo.errors.PyMongoError as error:
        print(f"Error al gestionar inventario: {error}")
        return jsonify({"error": "Error al gestionar inventario"}), 500

if __name__ == '__main__':
    app.run()