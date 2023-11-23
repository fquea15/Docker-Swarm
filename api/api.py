from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import redis
import json
import os  # Importa el módulo os para acceder a variables de entorno

app = Flask(__name__)
CORS(app)

# Usa las variables de entorno para obtener la configuración
redis_host = os.environ.get('REDIS_HOST', 'redis')  # Si no se proporciona, usa 'redis' por defecto
redis_port = int(os.environ.get('REDIS_PORT', 6379))
redis_db = int(os.environ.get('REDIS_DB', 0))

r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)

# Cargar datos desde el archivo CSV y almacenarlos en Redis si no están en caché
if not r.exists("total_records"):
    df = pd.read_csv("movie_data.csv")
    df['Rating'] = df['Rating'].astype(float)
    total_records = len(df)
    records_per_page = 20
    r.set("total_records", total_records)
    r.set("records_per_page", records_per_page)

# Obtener el número total de registros y registros por página
total_records = int(r.get("total_records"))
records_per_page = int(r.get("records_per_page"))

# Ruta para obtener películas paginadas
@app.route('/movies', methods=['GET'])
def get_movies():
    try:
        # Obtener el número de página y calcular el rango de registros
        page = int(request.args.get('page', 1))
        start_index = (page - 1) * records_per_page
        end_index = start_index + records_per_page

        # Obtener datos desde Redis
        movie_data_key = f"movie_data_page_{page}"
        paginated_data = r.get(movie_data_key)

        if not paginated_data:
            df = pd.read_csv("movie_data.csv")
            df['Rating'] = df['Rating'].astype(float)
            paginated_data = df.iloc[start_index:end_index].to_dict(orient='records')
            r.set(movie_data_key, json.dumps(paginated_data))

        # Si ya está en formato de cadena JSON, no necesitas cargarlo nuevamente
        if isinstance(paginated_data, str):
            paginated_data = json.loads(paginated_data)

        # Crear un diccionario de respuesta
        response = {
            'data': paginated_data,
            'total_records': total_records,
            'page': page,
            'records_per_page': records_per_page
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
