# rag-demo
Demostración de RAG (Retrieval-Augmented Generation) realizada en Python, cuenta con una base de datos vectorial ChromaDB 
y compatibilidad con la API de Gemini (AI Studio).

## ¿En que consiste la demo?
Simplemente en **demostrar las capacidades de un RAG** a la hora de rápidamente obtener información relacionada al input del usuario. La base de datos está *cargada con una serie de citas de filósofos reconocidos*, cuando un usuario envía una frase, el sistema **obtiene las frases más similares y en base al contexto alimenta al LLM** (Por defecto: Gemini Flash 2.5).

## Estructura general del sistema
1.	Carga de citas filosóficas en ChromaDB.
2.	Input del usuario.
3.	Recuperación de frases más similares vía búsqueda semántica.
4.	Generación de respuesta filosófica basada en el contexto encontrado.
5.	Salida en formato estructurado: reflexión + cita original.

## Dependencias
- chromadb: para la base de datos vectorial.
- google-genai: para la interacción con Gemini.
- dotenv: para el manejo de claves API en variables de entorno.

## ¿Cómo instalar?
1. Instalar dependencias:
```bash
pip install chromadb python-dotenv google-genai
```

2.	Configurar tu API Key:
Crear un archivo .env en el mismo directorio que el script y agregar:

```GEMINI_API_KEY=tu_clave_api_de_gemini```

## ¿Cómo ejecutar?
Simplemente correr el archivo Python. El sistema cargará la base vectorial (si no existe), solicitará una frase al usuario y devolverá una respuesta generada por el LLM, inspirada en las citas más cercanas contextualmente.

```bash
python main.py
```

## Notas adicionales
- La demo **no** busca crear código mantenible a lo largo del tiempo; fue desarrollada en un breve periodo de tiempo, por lo que puede no seguir las prácticas más recomendadas a nivel de codigo
- Las citas están embebidas en el script para facilitar la demo, pero se recomienda cargarlas desde un archivo externo para mejor mantenimiento.
- La base vectorial se almacena localmente en ./chroma_db, si querés reiniciar la carga, borrá esa carpeta manualmente.
- El sistema permite filtrar resultados por era (ej: “Antigua Grecia”, “Siglo XX”) modificando el parámetro where en la función query() de ChromaDB.
- El modelo por defecto es Gemini Flash 2.5, pero podés cambiarlo fácilmente desde el llamado a generate_content().