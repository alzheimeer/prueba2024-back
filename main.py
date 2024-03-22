from flask import Flask, jsonify
from routes import api_blueprint  
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})
    # Carga configuraciones desde config.py
    app.config.from_pyfile('config.py')
    # Registra el Blueprint de la API
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # Manejo de errores comunes
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Recurso no encontrado'}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'error': 'Error interno del servidor'}), 500

    # Manejador para errores de validación o personalizados
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Petición incorrecta'}), 400

    # Manejo de cualquier otro error no capturado específicamente
    @app.errorhandler(Exception)
    def unhandled_exception(error):
        app.logger.error(f'Error no manejado: {error}')
        return jsonify({'error': 'Ocurrió un error inesperado'}), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
