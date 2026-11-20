CREATE TABLE IF NOT EXISTS alumnos (
    no_control VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    carrera VARCHAR(120) NOT NULL
);

INSERT INTO alumnos (no_control, nombre, carrera) VALUES
('211130219', 'Carlos Gabriel González Rivas', 'Ing. en TIC'),
('211130220', 'Ana Sofía Martínez López', 'Ing. en TIC'),
('211130221', 'Luis Fernando Hernández Ruiz', 'Ing. en Sistemas Computacionales')
ON CONFLICT (no_control) DO NOTHING;