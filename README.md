# Proyecto: Aplicación de Alquiler de Portátiles con Flask

## Descripción

Esta aplicación web en Flask permite a los usuarios registrarse, iniciar sesión y gestionar el alquiler de portátiles. Utiliza MySQL como base de datos y werkzeug.security para el manejo seguro de contraseñas.

## Tecnologías

- Python (Flask)
- MySQL (PyMySQL)
- HTML y Bootstrap para la interfaz

## Instalación

### Requisitos previos

- Python 3.x
- MySQL Server
- Entorno virtual de Python (opcional pero recomendado)

### Pasos de instalación

1. Clonar el repositorio:
   ```sh
   git clone https://github.com/jcalderonvelo/prestamoPortatiles.git
   cd prestamoPortatiles
   ```
2. Crear y activar un entorno virtual (opcional):
   - En Linux/macOS:
     ```sh
     python3 -m venv venv
     source venv/bin/activate
     ```
   - En Windows:
     ```sh
     python -m venv venv
     venv\Scripts\activate
     ```
3. Instalar dependencias:
   ```sh
   pip install -r requirements.txt
   ```
4. Configurar la base de datos:
   - Crear la base de datos `gr2_db` en MySQL.
   - Configurar el usuario y permisos.
   - Ejecutar las migraciones necesarias.
5. Ejecutar la aplicación:
   ```sh
   python app.py
   ```
6. Acceder a la aplicación en el navegador:
   ```
   http://127.0.0.1:5000
   ```

## Uso

- Registro de nuevos usuarios.
- Inicio de sesión con validación de credenciales.
- Acceso al dashboard para visualizar los portátiles disponibles.

## Seguridad

- Contraseñas encriptadas con `werkzeug.security`.
- Uso de sesiones para autenticación de usuarios.

## Mejoras futuras

- Implementar roles de usuario.
- Agregar funcionalidad de alquiler de portátiles.
- Implementar Docker para despliegue más fácil, utilizando un Dockerfile para definir la imagen de la aplicación y docker-compose para gestionar los servicios, como la base de datos y el backend.

## Licencia

Este proyecto está bajo la licencia MIT. Puedes ver el archivo `LICENSE` para más detalles.

---

*Proyecto desarrollado por el Grupo 2.*

