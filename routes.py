from flask import Blueprint, request, jsonify, Response
from models import Producto, Inventario
from bson import json_util

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/productos', methods=['GET', 'POST'])
def gestionar_productos():
    if request.method == 'GET':
        productos = Producto.obtener_productos()
        return jsonify(productos)
    elif request.method == 'POST':
        data = request.json
        resultado = Producto.agregar_producto(data)
        return jsonify(resultado), 201

@api_blueprint.route('/inventario', methods=['GET', 'POST', 'PUT'])
def gestionar_inventario():
    try:
        if request.method == 'GET':
            inventario = Inventario().obtener_inventario()
            return Response(json_util.dumps(inventario), mimetype='application/json')
        elif request.method == 'POST':
            data = request.json
            resultado = Inventario().agregar_a_inventario(data)
            return jsonify(resultado), 201
        elif request.method == 'PUT':
            data = request.json
            id_inventario = data.get('id_inventario')
            if not id_inventario:
                return jsonify({'error': 'Falta el id_inventario en la solicitud'}), 400
            # Actualizar solo el campo "entregado"
            entregado = data.get('entregado')
            if entregado is None:
                return jsonify({'error': 'Falta el campo entregado en la solicitud'}), 400
            resultado = Inventario().actualizar_inventario(id_inventario, {'entregado': entregado})
            if resultado:
                return jsonify({'mensaje': 'Inventario actualizado exitosamente'}), 200
            else:
                return jsonify({'error': 'No se pudo actualizar el inventario'}), 404
    except Exception as e:
        print(f"Error en gestionar_inventario: {e}")
        raise
