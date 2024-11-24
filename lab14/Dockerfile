# Usa una imagen base de Python
FROM python:3.10

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requerimientos
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto al contenedor
COPY . .

# Exponer el puerto 8000
EXPOSE 8000

# Comando para ejecutar el servidor usando Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "lab14.wsgi:application"]