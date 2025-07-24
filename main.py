import chromadb
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

try: 
    client_gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
except Exception as e:
    print('Error configurando LLM: '+e)
    exit()

# Estas citas vendrian idealmente de un archivo
citas = [
    # Socráticos y Platón
    {"quote": "Solo sé que no sé nada.", "author": "Sócrates", "era": "Antigua Grecia"},
    {"quote": "La vida no examinada no merece ser vivida.", "author": "Sócrates", "era": "Antigua Grecia"},
    {"quote": "El conocimiento empieza en el asombro.", "author": "Sócrates", "era": "Antigua Grecia"},
    {"quote": "La música es para el alma lo que la gimnasia para el cuerpo.", "author": "Platón", "era": "Antigua Grecia"},
    {"quote": "Buscando el bien de nuestros semejantes, encontramos el nuestro.", "author": "Platón", "era": "Antigua Grecia"},
    {"quote": "La mayor declaración de amor es la que no se hace; el hombre que siente mucho, habla poco.", "author": "Platón", "era": "Antigua Grecia"},
    
    # Aristóteles
    {"quote": "La duda es el principio de la sabiduría.", "author": "Aristóteles", "era": "Antigua Grecia"},
    {"quote": "La felicidad depende de nosotros mismos.", "author": "Aristóteles", "era": "Antigua Grecia"},
    {"quote": "La belleza del alma resplandece cuando una persona soporta una desgracia tras otra con resignación.", "author": "Aristóteles", "era": "Antigua Grecia"},
    {"quote": "La inteligencia consiste no solo en el conocimiento, sino también en la destreza de aplicar los conocimientos en la práctica.", "author": "Aristóteles", "era": "Antigua Grecia"},
    {"quote": "El amigo de todo el mundo no es un amigo.", "author": "Aristóteles", "era": "Antigua Grecia"},
    
    # Modernos y Racionalistas
    {"quote": "Pienso, luego existo.", "author": "René Descartes", "era": "Modernidad"},
    {"quote": "Donde no hay ley, no hay libertad.", "author": "John Locke", "era": "Modernidad"},
    {"quote": "Atreverse a saber. ¡Ten el valor de servirte de tu propia razón!", "author": "Immanuel Kant", "era": "Ilustración"},
    {"quote": "El sabio puede cambiar de opinión. El necio, nunca.", "author": "Immanuel Kant", "era": "Ilustración"},
    {"quote": "Vivir sin filosofar es, propiamente, tener los ojos cerrados, sin tratar de abrirlos jamás.", "author": "René Descartes", "era": "Modernidad"},

    # Existencialistas y Críticos
    {"quote": "El hombre está condenado a ser libre.", "author": "Jean-Paul Sartre", "era": "Siglo XX"},
    {"quote": "La existencia precede a la esencia.", "author": "Jean-Paul Sartre", "era": "Siglo XX"},
    {"quote": "Dios ha muerto.", "author": "Friedrich Nietzsche", "era": "Siglo XIX"},
    {"quote": "Lo que no me mata, me hace más fuerte.", "author": "Friedrich Nietzsche", "era": "Siglo XIX"},
    {"quote": "La esperanza es el peor de los males, pues prolonga el tormento del hombre.", "author": "Friedrich Nietzsche", "era": "Siglo XIX"},
    {"quote": "Aquel que tiene un porqué para vivir se puede enfrentar a todos los 'cómos'.", "author": "Friedrich Nietzsche", "era": "Siglo XIX"},
    {"quote": "No soy un hombre, soy dinamita.", "author": "Friedrich Nietzsche", "era": "Siglo XIX"},

    # Otros
    {"quote": "La paciencia es amarga, pero sus frutos son dulces.", "author": "Jean-Jacques Rousseau", "era": "Ilustración"},
    {"quote": "No se puede pisar dos veces el mismo río.", "author": "Heráclito", "era": "Presocráticos"},
    {"quote": "El hombre es un lobo para el hombre.", "author": "Thomas Hobbes", "era": "Modernidad"},
    {"quote": "La imaginación es más importante que el conocimiento.", "author": "Albert Einstein", "era": "Siglo XX"},
    {"quote": "La única cosa que sé es saber que nada sé; y esto cabalmente me distingue de los demás filósofos, que creen saberlo todo.", "author": "Sócrates", "era": "Antigua Grecia"},
    {"quote": "El corazón tiene razones que la razón no entiende.", "author": "Blaise Pascal", "era": "Modernidad"},
    {"quote": "La libertad significa responsabilidad. Por eso la mayoría de los hombres la temen.", "author": "George Bernard Shaw", "era": "Siglo XX"},
    {"quote": "La religión es el opio de los pueblos.", "author": "Karl Marx", "era": "Siglo XIX"},
]


client_chroma = chromadb.PersistentClient(path="./chroma_db")

collection_name = "citas_filosoficas"
#Creo la coleccion y que sea de tipo coseno para el texto
collection = client_chroma.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"}) 

# Si la coleccion está vacia
if (collection.count() == 0):
    print("Cargando citas en ChromaDB por primera vez...")

    for i, cita in enumerate(citas):
        collection.add(
            documents = [cita["quote"]],
            metadatas=[{"author": cita["author"], "era": cita["era"]}],           
            ids=[f"cita_{i}"]
        )
    
    print(f"Fueron cargadas {collection.count()} citas.")

else:
    print(f"La coleccion {collection_name} ya tiene {collection.count()} citas cargadas.")


#user_input = "Che tipo me parece que no sé nada"
user_input = input("Ingrese una frase: ")

# Manda el user_input y me devuelve las coincidencias más cercanas
results = collection.query(
    query_texts = [user_input],
    n_results= 4,
    # where={"era": "Siglo XX"} # Aca puedo filtrar los de una era especifica
)

citas_encontradas = results['documents'][0]
autores_encontrados = []

for metadata in results['metadatas'][0]:
    autores_encontrados.append(metadata['author'])

#distancia_coincidencia = results['distances'][0]


print("BUSQUEDA VECTORIAL:")
print(f"Frase del usuario: {user_input}")
print(f"Citas más similares encontradas en ChromaDB: {citas_encontradas}")
print(f"Autores: {autores_encontrados}")
#print(f"Distancia de coincidencias: {distancia_coincidencia}")
print("\n\n")

# ------------------- Ahora voy a guardar toda esta info y darsela al LLM

contexto_final = ""
for i in range(len(citas_encontradas)):
    cita = citas_encontradas[i]
    autor = autores_encontrados[i]
    
    texto_formateado = f"- '{cita}' ({autor})\n" # Armo el textito para una cita
    contexto_final += texto_formateado          # Lo voy sumando al texto grande


# Pedirle al LLM que genere el prompt
prompt_genio = f"""
Actuá como un sabio filósofo, elocuente y profundo. Un individuo se te acerca y te plantea su inquietud: "{user_input}"

Debes ofrecerle una respuesta breve pero cargada de significado. Inspírate en la sabiduría de las siguientes citas, pero no las copies. Sintetiza su esencia en una reflexión original. Intenta que el tono de tu respuesta se ajuste al estilo de los filósofos del contexto (ej: si son existencialistas, sé más incisivo; si son griegos, más reflexivo).

**Contexto para tu inspiración:**
{contexto_final}

---
**Formato de tu respuesta:**
Debes responder usando estrictamente este formato, sin añadir nada más:

RESPUESTA:
[Aquí va tu reflexión filosófica]

CITA ORIGINAL:
[Aquí va la nueva cita que has creado, inspirada en tu reflexión]
---

Importante: Asegurate de incluir en tu respuesta los filosofos que te inspiraron
"""

print("Respuesta del genio:")

try:
    respuesta_gemini = client_gemini.models.generate_content(model="gemini-2.5-flash", contents=prompt_genio)
    print(respuesta_gemini.text)
    
except Exception as e:
    print(f"Error al generar la historia con Gemini: {e}")
    exit()