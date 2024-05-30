CREATE TABLE liquidacion (
ID_Liquidacion INT PRIMARY KEY,
Indemnizacion DECIMAL(10,2) NOT NULL,
Vacaciones DECIMAL(10,2) NOT NULL,
Cesantias DECIMAL(10,2) NOT NULL,
Intereses_Sobre_Cesantias DECIMAL(10,2) NOT NULL,
Prima_Servicios DECIMAL(10,2) NOT NULL,
Retencion_Fuente DECIMAL(10,2) NOT NULL,
Total_A_Pagar DECIMAL(10,2) NOT NULL,
ID_Usuario INT NOT NULL,
FOREIGN KEY (ID_Usuario) REFERENCES usuarios(ID_Usuario)
);
