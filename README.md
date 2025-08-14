# 📊 Movimientos Bancarios API

Una API web desarrollada con **FastAPI** para cargar, clasificar y gestionar movimientos bancarios desde archivos Excel. Incluye autenticación de usuarios, almacenamiento en base de datos MySQL y una interfaz web básica.

---

## 🚀 Características

- ✅ Registro y login de usuarios con autenticación JWT
- 📥 Carga de movimientos bancarios desde archivos Excel
- 🗃️ Almacenamiento en MySQL mediante SQLAlchemy
- 🔐 Seguridad con bcrypt y tokens JWT
- 🌐 Interfaz web básica para subir archivos
- ⚙️ Configuración flexible con variables de entorno

---

## 🧱 Tecnologías utilizadas

- **Python 3.10**
- **FastAPI**
- **SQLAlchemy**
- **MySQL**
- **pandas** y **openpyxl**
- **bcrypt** y **python-jose**
- **HTML + JavaScript**
- **dotenv**

---

## 📁 Estructura del proyecto
movimientos_api/
├── LICENSE                # Licencia del proyecto
├── README.md              # Documentación principal
├── requirements.txt       # Dependencias de Python
├── app/                   # Backend de la aplicación
├── env/                   # Entorno virtual (puede ignorarse en producción)
└── frontend/              # Interfaz de usuario o cliente web

---

## ⚙️ Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/movimientos_api.git
   cd movimientos_api

---

2. Crea un entorno virtual:
    '''bash
    python -m venv venv
    source venv/bin/activate

---

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt

---

4. Configura el archivo .env:
    ```bash
    DATABASE_URL=mysql+pymysql://usuario:contraseña@host:puerto/basedatos
    SECRET_KEY=tu_clave_secreta

---

5. Configura el archivo .env:
    ```bash
    uvicorn app.main:app --reload

---

📌 Endpoints principales
Método	Ruta	Descripción
POST	/registro/	Registro de nuevo usuario
POST	/login/	Login y generación de token JWT
POST	/cargar_movimientos/	Carga de archivo Excel
GET	/	Mensaje de bienvenida

🛡️ Seguridad
- Contraseñas encriptadas con bcrypt
- Autenticación con JWT
- Variables sensibles gestionadas con .env

## 📄 Licencia
Este proyecto está bajo la licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente.

## ✉️ Contacto
Desarrollado por Esteban. ¿Tienes sugerencias o quieres colaborar? ¡Estoy abierto a mejoras!