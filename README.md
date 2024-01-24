# Mfa_login_panel

Este es un fichero de login , que implatan un MFA
Se puede configurar con  "google autentificato"

# Instalas el requesmetn.txt

# Hay que generera la siguinte estrutura de base de datos: 

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    codigo_mfa TEXT NULL,
    code_qr BOOLEAN DEFAULT FALSE
);

# Trigger:

DELIMITER //
CREATE TRIGGER actualizar_code_qr
BEFORE INSERT ON usuarios
FOR EACH ROW
BEGIN
    IF NEW.codigo_mfa IS NOT NULL THEN
        SET NEW.code_qr = TRUE;
    END IF;
END;
//
DELIMITER ;


#Ejemplo:

INSERT INTO usuarios (id, username, password, codigo_mfa, code_qr) VALUES (0 ,'usuario0', 'contraseña0', NULL, FALSE);



# Ejecutas el fichero mfa_login_master 















