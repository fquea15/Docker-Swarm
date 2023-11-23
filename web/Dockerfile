# Establece la imagen base con Node.js
FROM node:14

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY package.json /app/
RUN npm install

# Copia el resto de los archivos
COPY . /app/

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 3000

# Comando para iniciar la aplicación al ejecutar el contenedor
CMD ["npm", "start"]
