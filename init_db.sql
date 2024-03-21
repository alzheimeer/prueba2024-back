CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(100) NOT NULL
);

INSERT INTO productos (nombre, descripcion, categoria) VALUES
('Tarjeta credito', 'Descripción de Tarjeta credito', 'Categoría A'),
('Cheque', 'Descripción del Cheque', 'Categoría B'),
('Talonario', 'Descripción del Talonario', 'Categoría A'),

ON DUPLICATE KEY UPDATE nombre=VALUES(nombre), descripcion=VALUES(descripcion), categoria=VALUES(categoria);