import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_PARAMS = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": 5432
}


def knn(vector:list,k:int):

    busqueda=f"""SELECT id, pagina_id, texto, embedding <=> ARRAY{vector}::vector AS similarity
    FROM fragmentos
    ORDER BY similarity
    LIMIT {k};"""

    return ejecutar_query(busqueda)

def crear_documento(titulo: str):
    query = f"""INSERT INTO documentos (titulo) 
    VALUES ('{titulo}') 
    RETURNING id;"""
    
    return ejecutar_query(query)

def crear_pagina(documento_id: int, numero: int, contenido: str):
    query = f"""INSERT INTO paginas (documento_id, numero, contenido) 
    VALUES ({documento_id}, {numero}, '{contenido}') 
    RETURNING id;"""
    
    return ejecutar_query(query)

def crear_fragmento(pagina_id: int, texto: str, embedding: list):
    query = f"""INSERT INTO fragmentos (pagina_id, texto, embedding) 
    VALUES ({pagina_id}, '{texto}', ARRAY{embedding}::vector) 
    RETURNING id;"""
    
    return ejecutar_query(query)


def ejecutar_query(query: str):

    try:

        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute(query)

        # Fetch results if it's a SELECT query
        if query.strip().upper().startswith("SELECT"):
            result = cur.fetchall()
        elif "RETURNING id" in query:  # If query returns an ID, fetch it
            result = cur.fetchone()[0]  # Get the inserted ID
            conn.commit()
        else:
            result = None
            conn.commit()  # Commit changes for INSERT, UPDATE, DELETE

        cur.close()
        conn.close()
        return result
    
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    