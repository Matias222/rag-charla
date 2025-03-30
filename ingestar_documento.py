import fitz
import os
import chunking_functions
import embedding_functions
import db_queries

def extraer_imagen(page,doc,page_num,output_dir):

    # Extract images from the page
    images = page.get_images(full=True)
    
    if images:
        print(f"Found {len(images)} image(s) on page {page_num}")
        
        # Extract and save each image
        for img_index, img_info in enumerate(images):
            # Get the image reference
            xref = img_info[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image['image']
            
            # Determine file extension
            ext = base_image['ext']
            
            # Create filename
            filename = f'page_{page_num}_image_{img_index+1}.{ext}'
            filepath = os.path.join(output_dir, filename)
            
            # Save the image
            with open(filepath, 'wb') as img_file:
                img_file.write(image_bytes)
            
            print(f"Saved image: {filename}")
    
            #LLM Vision -> Haiku
            #Describa la imagen
            #Vectorizar la descripcion

    else:
        print(f"No images found on page {page_num}")

    

def extract_pdf_images(pdf_path, output_dir='extracted_images'):

    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)
    
    id_documento=db_queries.crear_documento(pdf_path)

    # Iterate through pages
    for page_num, page in enumerate(doc, 1):

        print(f"\n--- Page {page_num} ---")
        
        # Print page text
        pagina_texto=page.get_text()
        
        id_pagina=db_queries.crear_pagina(id_documento,page_num,pagina_texto)

        fragmentos=chunking_functions.chunkeo(pagina_texto)

        for i in fragmentos: 
            
            vector=embedding_functions.generar_vector(i)
        
            id_fragmento=db_queries.crear_fragmento(id_pagina,i,vector)
        
        extraer_imagen(page,doc,page_num,output_dir)

        if(page_num>3): break

    doc.close()


pdf_path = "attention.pdf"
extract_pdf_images(pdf_path)