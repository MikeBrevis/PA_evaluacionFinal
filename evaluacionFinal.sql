CREATE DATABASE EmpresaLogistica;

USE EmpresaLogistica;

CREATE TABLE Envios (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NumeroSeguimiento VARCHAR(50) NOT NULL,
    Origen VARCHAR(100) NOT NULL,
    Destino VARCHAR(100) NOT NULL,
    FechaEntregaPrevista DATE,
    Estado VARCHAR(50) DEFAULT 'En tránsito'
);

INSERT INTO Envios (NumeroSeguimiento, Origen, Destino, FechaEntregaPrevista, Estado) VALUES 
('123456789', 'Ciudad A', 'Ciudad B', '2024-02-10', 'En tránsito'), 
('987654321', 'Ciudad B', 'Ciudad C', '2024-02-12', 'En tránsito'), 
('567890123', 'Ciudad C', 'Ciudad A', '2024-02-15', 'En tránsito');
