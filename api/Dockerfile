# Usa la imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY requirements.txt api.py movie_data.csv /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que se ejecuta la aplicación
EXPOSE 5000

# Comando para ejecutar la aplicación al iniciar el contenedor
CMD ["python", "api.py"]
