#!/bin/bash

echo "Iniciando actualización del sistema..."
sudo apt update
sudo apt upgrade -y
echo "Sistema actualizado."

echo "Instalando Node.js..."
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
echo "Versión de Node instalada:"
sudo node -v
echo "Versión de NPM instalada:"
sudo npm -v
du 
echo "Instalando MySQL..."
sudo apt-cache search mysql-server
sudo apt install -y mysql-server
echo "MySQL instalado. Estado del servicio MySQL:"
sudo systemctl status mysql.service
sudo systemctl start mysql.service
echo "Servicio MySQL iniciado."
sudo systemctl enable mysql.service
echo "Servicio MySQL habilitado."

echo "Configurando usuario root de MySQL..."
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'admin';"
echo "Usuario root configurado."

echo "Creando base de datos y tabla..."
sudo mysql -u root -padmin <<EOF
CREATE DATABASE epolaris;
USE epolaris;
CREATE TABLE users (
  email VARCHAR(255) NOT NULL,
  name VARCHAR(50) NOT NULL,
  password VARCHAR(255) NOT NULL,
  is_default_password TINYINT(1) NOT NULL DEFAULT 1,
  privilege VARCHAR(20) NOT NULL DEFAULT 'user',
  username VARCHAR(255),
  PRIMARY KEY (email),
  UNIQUE (username)
);
INSERT INTO users (email, name, password, privilege, is_default_password, username)
VALUES ('admin@example.com', 'Admin User', '$2b$10$dA.jNSzAuUD74oC.4aGIeuPfQUZbBxCp7Ksmx/kAXjC3XDkZTdQrC', 'admin', TRUE, 'admin');
EOF
echo "Base de datos y tabla creadas."

echo "Instalando y configurando PM2..."
npm install pm2@latest -g
cd Prototipo_App2024/app_2024/src
pm2 start app.js
pm2 startup
pm2 save
echo "PM2 configurado y aplicación iniciada."

echo "Script completado."
