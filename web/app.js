const express = require('express');
const axios = require('axios');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const port = 3000;

app.set('view engine', 'pug');

app.get('/', async (req, res) => {
  try {
    const apiUrl = process.env.PYTHON_API_URL || 'http://localhost:5000';
    
    // Obtén el número de página de la solicitud
    const page = parseInt(req.query.page) || 1;

    // Realiza la solicitud GET a la API Flask
    const response = await axios.get(`${apiUrl}/movies`, {
      params: { page },
    });

    // Renderiza la vista Pug con los datos de la API
    res.render('movies', {
      movies: response.data.data,
      totalRecords: response.data.total_records,
      currentPage: response.data.page,
      recordsPerPage: response.data.records_per_page,
    });
  } catch (error) {
    console.error('Error al realizar la solicitud:', error.message);
    res.render('error', { errorMessage: 'Error al cargar los datos.' });
  }
});

app.listen(port, () => {
  console.log(`Servidor escuchando en http://localhost:${port}`);
});
