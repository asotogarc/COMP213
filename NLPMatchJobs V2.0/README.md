# NLPMatchJobs - Comparador Inteligente de Candidatos y Ofertas de Trabajo

NLPMatchJobs es una aplicación web  desarrollada con Streamlit que utiliza Inteligencia Artificial y Procesamiento de Lenguaje Natural (NLP) avanzado para comparar candidatos con ofertas de trabajo. La aplicación evalúa de manera inteligente si los candidatos se ajustan adecuadamente a la oferta seleccionada, proporcionando un análisis PLN detallado  del texto de la oferta y la candidatura.

## Características Principales

- **Comparación Inteligente**: Utiliza algoritmos de IA y NLP para analizar y comparar el contenido de las ofertas de trabajo con los perfiles de los candidatos.
- **Análisis de Ajuste**: Determina con precisión si un candidato se ajusta bien a una oferta específica.
- **Datos de Contacto**: En caso de que nuestro algoritmo IA determine que el candidato cumple con los requisitos de la oferta, muestra los datos de contacto del candidato para facilitar la comunicación.
- **Análisis Detallado**: Proporciona un análisis completo del procesamiento de lenguaje natural de ambos textos (oferta y candidatura).
- **Visualizaciones Interactivas**: Presenta los resultados mediante gráficos y tablas para una fácil comprensión del análisis PLN.
- **Recomendaciones Personalizadas**: Ofrece sugerencias específicas para mejorar la similitud  entre ambos textos (candidato y oferta).


## Tabla de Contenidos
1. [Estructura del Repositorio](#estructura-del-repositorio)
2. [Instalación](#instalación)
3. [Configuración](#configuración)
4. [Uso](#uso)
5. [Descripción Detallada de los Componentes](#descripción-detallada-de-los-componentes)
6. [Flujo de Trabajo del Programa](#flujo-de-trabajo-del-programa)
7. [Contribución](#contribución)
8. [Licencia](#licencia)

## Estructura del Repositorio

```
.
├── components/
│   ├── candidates.py
│   ├── comparison.py
│   └── job_offers.py
├── streamlit/
│   └── config.toml
├── styles/
│   └── custom.css
├── utils/
│   ├── data_processing.py
│   ├── google_sheets.py
│   └── visualization.py
├── .gitignore
├── config.py
├── Procfile
├── requirements.txt
├── runtime.txt
└── streamlit_app.py
```

## Instalación

1. Clona este repositorio:
   ```
   git clone https://github.com/tu-usuario/NLPMatchJobs.git
   cd NLPMatchJobs
   ```

2. Crea un entorno virtual e instala las dependencias:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Instala las dependencias adicionales:
   ```
   python -m nltk.downloader stopwords
   ```

## Configuración

1. Configura las credenciales de Google Sheets en `config.py`:
   - Asegúrate de tener un proyecto en Google Cloud Platform con la API de Google Sheets habilitada.
   - Crea una cuenta de servicio y descarga el archivo JSON de credenciales.
   - Copia el contenido del JSON en la variable `credentials` en `config.py`.

2. Configura la clave API de OpenAI en `config.py`:
   - Obtén una clave API de OpenAI y asígnala a la variable `API_KEY` en `config.py`.

## Uso

Para ejecutar la aplicación:

```
streamlit run streamlit_app.py
```

Abre tu navegador y ve a `http://localhost:8501` para ver la aplicación en funcionamiento.

## Descripción Detallada de los Componentes

### streamlit_app.py

Este es el archivo principal que ejecuta la aplicación Streamlit. Sus principales funciones son:

- Configurar la página y el tema de Streamlit.
- Cargar los datos de ofertas y candidatos desde Google Sheets.
- Mostrar las ofertas y candidatos utilizando los componentes correspondientes.
- Manejar la lógica de comparación cuando se selecciona una oferta y un candidato.
- Visualizar los resultados de la comparación, incluyendo gráficos y análisis detallados.

Funciones clave:
- `main()`: Función principal que orquesta todo el flujo de la aplicación.

### components/candidates.py

Maneja la visualización de los candidatos en la interfaz de usuario.

Funciones principales:
- `display_candidates(data)`: Crea tarjetas interactivas para cada candidato, permitiendo su selección y mostrando detalles como formación, conocimientos y experiencia.

### components/job_offers.py

Similar a `candidates.py`, pero para las ofertas de trabajo.

Funciones principales:
- `display_job_offers(data)`: Crea tarjetas interactivas para cada oferta de trabajo, permitiendo su selección y mostrando detalles relevantes.

### components/comparison.py

Contiene funciones para interactuar con la API de OpenAI y generar explicaciones personalizadas.

Funciones principales:
- `get_gpt_explanation(prompt)`: Envía un prompt a GPT-4 y recibe una respuesta explicativa, utilizada para generar análisis detallados y recomendaciones.

### utils/data_processing.py

Contiene funciones para procesar y comparar datos de candidatos y ofertas.

Funciones principales:
- `calculate_similarity(offer, candidate)`: Utiliza TF-IDF y similitud del coseno para calcular un porcentaje de similitud entre una oferta y un candidato. También devuelve los términos más relevantes para la comparación.

### utils/google_sheets.py

Maneja la interacción con Google Sheets para leer y escribir datos.

Funciones principales:
- `open_google_sheet(sheet_title, worksheet_title)`: Abre una hoja de cálculo específica de Google Sheets.
- `read_worksheet(worksheet)`: Lee los datos de una hoja de trabajo y los devuelve como un DataFrame de pandas.

### utils/visualization.py

Contiene funciones para crear visualizaciones de los resultados.

Funciones principales:
- `display_bar_chart(offer_scores, candidate_scores, terms)`: Crea un gráfico de barras comparativo utilizando Plotly, mostrando la relevancia de diferentes términos para la oferta y el candidato.

## Flujo de Trabajo del Programa

1. El usuario inicia la aplicación ejecutando `streamlit run streamlit_app.py`.
2. La aplicación carga los datos de ofertas y candidatos desde Google Sheets.
3. Se muestran las tarjetas de ofertas y candidatos en la interfaz.
4. El usuario selecciona una oferta y un candidato.
5. Al hacer clic en "Realizar Comparación":
   - Se calcula la similitud entre la oferta y el candidato.
   - Se genera una recomendación personalizada utilizando GPT-4.
   - Se muestran gráficos comparativos (gráfico de radar y de barras).
   - Se presenta una tabla detallada de comparación de términos.
   - Se generan explicaciones detalladas sobre la similitud y los términos clave.
   - Se proporcionan recomendaciones de áreas de mejora para el candidato.

## Contribución

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/AmazingFeature`).
3. Haz tus cambios y commit (`git commit -m 'Add some AmazingFeature'`).
4. Push a la rama (`git push origin feature/AmazingFeature`).
5. Abre un Pull Request.

## Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.