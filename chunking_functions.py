from langchain.text_splitter import RecursiveCharacterTextSplitter

def limpiar(cadena: str) -> str:

    return cadena.strip().lower()

def chunkeo(texto: str, chunk_size: int = 600, chunk_overlap: int = 150) -> list:

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    texto = limpiar(texto)

    return text_splitter.split_text(texto)
