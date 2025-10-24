from dotenv import load_dotenv
import os
import sys
from glob import glob
from tqdm import tqdm
from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import (Element)
from unstructured.chunking.title import chunk_by_title

# Set UTF-8 encoding for Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')


def load_documents(document_path: str) -> list[Element]:    
    # Check if folder exists
    if not os.path.exists(data_folder):
        raise ValueError(f"Folder {document_path} not found!")        
    elements: list[Element] = []
    print(f"📂 Loading documents from: {document_path}")
    for file in tqdm(glob(os.path.join(data_folder, "*.pdf"), recursive=False), desc="Loading files"):
        if os.path.isfile(file):
            print(f" Processing file {file}")
            elements.extend(partition_pdf(  file,            
                                            languages=["eng"],
                                            strategy="hi_res",                                            
                                            infer_table_structure=True,
                                            extract_image_block_types=["Image", "Table"],
                                            extract_image_block_to_payload=True,
                                            ))    
    print(f"✅ {len(elements)} elements extracted")
    return elements; 


def chunk_elements(elements: list[Element]) -> list[Element]:
    print(f"🔨 Chunking elements")
    chunked_elements = chunk_by_title(  elements,
                            max_characters=500,
                            new_after_n_chars=400,
                            combine_text_under_n_chars=100,
                            overlap=100,
                            multipage_sections=True,
                            include_orig_elements=False )
    print(f"✅ {len(elements)} elements after chunk")
    return chunked_elements


if __name__ == "__main__":
    load_dotenv()
    print("✅ Test environment loaded!")
    
    data_folder = "../data"
    try:
        elements = load_documents(data_folder)
        chunked_elements = chunk_elements(elements)

    except Exception as e:
        print(f"❌ Exception occurred: '{e}'")