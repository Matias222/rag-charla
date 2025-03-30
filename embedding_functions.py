from openai import OpenAI
from dotenv import load_dotenv
import db_queries
import json

load_dotenv()

client = OpenAI()

def generar_vector(text:str) -> list[int]: 

    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )

    return response.data[0].embedding

def recuperar_vector(text:str) -> str:

    vector_busqueda = generar_vector(text)

    respuesta = db_queries.knn(vector_busqueda,3)

    print("TOP RESPUESTA")
    
    print("ID Documento",respuesta[0][0])
    print("ID Pagina",respuesta[0][1])
    print("ID contenido",respuesta[0][2])

recuperar_vector("Whats the number of layers of the Encoder")