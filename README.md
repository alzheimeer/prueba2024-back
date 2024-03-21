# Prueba2024

# Instalar en windows mysql 
- Bajarlo de https://dev.mysql.com/downloads/installer/

# INSTALL
- python -m venv env
- source env/bin/activate
- Alternativa:   env\Scripts\activate
- pip install flask
- pip install mysql-connector-python
- pip install pymongo
- pip install flask-cors

# RUN
- flask run


# Ejecutar queries Mysql - Comprobacion de existencia y insertar data inicial

- mysql -u prueba2024 -p
- USE prueba2024;
- SOURCE ruta/a/init_db.sql;

# Prueba2024 
El proyecto utiliza MySQL para almacenar los tipos de productos y MongoDB para gestionar el inventario, ofreciendo una API REST para las operaciones CRUD.

# Estructura del Proyecto
- app.py: Archivo principal que inicia la aplicación Flask. Define y registra los Blueprints y configura la aplicación con las variables globales definidas en config.py. Incluye la lógica de inicialización de la base de datos y el manejo global de errores.

- config.py: Contiene las configuraciones de la aplicación, incluidas las cadenas de conexión para MySQL y MongoDB. Facilita la gestión de la configuración en un lugar centralizado, mejorando la seguridad y la mantenibilidad.

- models.py: Define los modelos Producto e Inventario, así como las operaciones CRUD para interactuar con las bases de datos MySQL y MongoDB, respectivamente. Este archivo encapsula la lógica de acceso a datos, manteniendo el código organizado y promoviendo la reutilización.

- routes.py: Contiene la definición de las rutas/endpoints de la API REST, utilizando el Blueprint de Flask para organizar las rutas relacionadas con la gestión de productos e inventario. Cada función maneja las solicitudes a su respectivo endpoint y comunica con models.py para realizar operaciones de base de datos.

# Descripción de Endpoints
- GET /api/productos: Recupera y devuelve una lista de todos los productos almacenados en MySQL. Utilizado para mostrar los tipos de productos disponibles al usuario en el frontend.

- POST /api/productos: Permite la inserción de un nuevo tipo de producto en MySQL. Acepta datos en formato JSON que representan las propiedades del producto a agregar.

- GET /api/inventario: Recupera y devuelve la lista de todos los productos en el inventario almacenados en MongoDB. Este endpoint es crucial para la visualización del estado actual del inventario.

- POST /api/inventario: Permite agregar un nuevo producto al inventario en MongoDB. Acepta datos en formato JSON que representan el producto y la cantidad a agregar al inventario.

# Manejo de Errores
La aplicación implementa un manejo global de errores para interceptar excepciones comunes y no manejadas, garantizando que la API responda de manera coherente ante errores. Los errores específicos, como 404 (No Encontrado) y 500 (Error Interno del Servidor), se manejan específicamente para proporcionar respuestas claras y útiles.

# Consideraciones Finales
El proyecto ha sido diseñado utilizando prácticas de desarrollo recomendadas como la separación de responsabilidades y la configuración centralizada.


# AUTOR
- Carlos Mauricio Quintero