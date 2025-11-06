CREATE DATABASE IF NOT EXISTS citas_medicas;
USE citas_medicas;

DROP TABLE IF EXISTS citas;
DROP TABLE IF EXISTS pacientes;
DROP TABLE IF EXISTS medicos;

CREATE TABLE pacientes (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(255) NOT NULL,
    telefono VARCHAR(20) DEFAULT NULL,
    email VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre_completo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE medicos (
    id_medico INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(255) NOT NULL,
    especialidad VARCHAR(100) DEFAULT NULL,
    telefono VARCHAR(20) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre_completo),
    INDEX idx_especialidad (especialidad)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE citas (
    id_cita INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_medico INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado VARCHAR(50) NOT NULL DEFAULT 'Programada',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_medico) REFERENCES medicos(id_medico) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_fecha_hora_medico (fecha, hora, id_medico),
    INDEX idx_fecha_hora_paciente (fecha, hora, id_paciente),
    INDEX idx_estado (estado),
    INDEX idx_fecha (fecha)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO pacientes (nombre_completo, telefono, email) VALUES
('María López García', '555-1234', 'maria.lopez@email.com'),
('Juan Pérez Martínez', '555-5678', 'juan.perez@email.com'),
('Ana Rodríguez Sánchez', '555-9012', 'ana.rodriguez@email.com'),
('Carlos González Torres', '555-3456', 'carlos.gonzalez@email.com'),
('Laura Fernández Díaz', '555-7890', 'laura.fernandez@email.com');

INSERT INTO medicos (nombre_completo, especialidad, telefono) VALUES
('Dr. Roberto Martínez', 'Cardiología', '555-1001'),
('Dra. Carmen Sánchez', 'Pediatría', '555-1002'),
('Dr. Luis Fernández', 'Medicina General', '555-1003'),
('Dra. Patricia Gómez', 'Ginecología', '555-1004'),
('Dr. Miguel Torres', 'Dermatología', '555-1005');

INSERT INTO citas (id_paciente, id_medico, fecha, hora, estado) VALUES
(1, 1, '2024-12-20', '10:00', 'Programada'),
(2, 2, '2024-12-20', '11:00', 'Programada'),
(3, 3, '2024-12-21', '09:00', 'Programada'),
(1, 4, '2024-12-22', '14:00', 'Programada'),
(4, 5, '2024-12-20', '15:00', 'Completada');

SELECT 'Base de datos creada exitosamente!' AS mensaje;
SELECT COUNT(*) AS total_pacientes FROM pacientes;
SELECT COUNT(*) AS total_medicos FROM medicos;
SELECT COUNT(*) AS total_citas FROM citas;
