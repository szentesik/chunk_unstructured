from dotenv import load_dotenv
import os
import sys
from glob import glob
from tqdm import tqdm
from unstructured.partition.pdf import (partition_pdf, PartitionStrategy)
from unstructured.documents.elements import (Element)
from unstructured.chunking.title import chunk_by_title
import requests
import tiktoken

# Set UTF-8 encoding for Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')


def load_documents(document_path: str, mode: str = PartitionStrategy.FAST) -> list[Element]:    
    # Check if folder exists
    if not os.path.exists(data_folder):
        raise ValueError(f"Folder {document_path} not found!")        
    elements: list[Element] = []
    print(f"📂 Loading documents from: {document_path}")
    for file in tqdm(glob(os.path.join(data_folder, "*.pdf"), recursive=False), desc="Loading files"):
        if os.path.isfile(file):
            print(f" Processing file {file} ({mode})")
            if mode == PartitionStrategy.FAST:
                elements.extend(partition_pdf(  file,            
                                            languages=["eng"],
                                            strategy="fast"
                                            ))
            else:
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
    print(f"✅ {len(chunked_elements)} elements after chunk")    
    return chunked_elements


def prepare_documents(chunks: list[Element]) -> list:
    print(f"📋 Preparing documents")
    documents = []
    for i, chunk in enumerate(chunks):
        if(len(str(chunk)) == 0):
            continue
        doc = {
            "id": i + 1,
            "filename": chunk.metadata.filename if hasattr(chunk, 'metadata') and hasattr(chunk.metadata, 'filename') else None,            
            "page": chunk.metadata.page_number if hasattr(chunk, 'metadata') and hasattr(chunk.metadata, 'page_number') else 0,
            "text": str(chunk)
        }        
        documents.append(doc)
    print(f"✅ {len(documents)} documents ready")
    return documents


def calculate_num_tokens(documents: list, encoding_name: str = "cl100k_base") -> int:
    """Returns the predicted number of tokens."""
    num_tokens = 0
    for doc in tqdm(documents, desc="Calculating token count"):
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens += len(encoding.encode(doc["text"]))
    return num_tokens


def upload_documents(documents: list, url: str):
    uploaded = 0
    try:
        for doc in tqdm(documents, desc="Uploading documents"):
            res = requests.post(url, json = doc)
            if(res.status_code == 201):
                uploaded += 1
            else:
                print(f"⚠️ Resource not created: {res.status_code}, {res.text}")        
    except Exception as e:
        print(f"❌ Upload failed: '{e}'")
    finally:
        return uploaded


if __name__ == "__main__":
    load_dotenv()
    print("✅ Test environment loaded!")

    api_endpoint=os.getenv("UPLOAD_API_ENDPOINT", "")
    if not api_endpoint:
        print(f"❌ Environment variable UPLOAD_API_ENDPOINT is not defined")
        quit()

    data_folder = "../data"

    print(f"⚠️ This scripts uploads all pdf documents from {data_folder} to embedding database!")
    confirmation = input("❓ Do you want to continue? (y/N): ").strip().lower()
    if confirmation != 'y': quit()
    
    try:
        elements = load_documents(data_folder, mode="fast")
        chunked_elements = chunk_elements(elements)
        documents = prepare_documents(chunked_elements)

        num_tokens = calculate_num_tokens(documents)
        print(f"ℹ️ Estimated number of tokens: {num_tokens}")
        confirmation = input("❓ Do you want to continue? (y/N): ").strip().lower()
        if confirmation == 'y':
            uploaded = upload_documents(documents, url=api_endpoint)

            if uploaded == len(documents):
                print(f"✅ {uploaded} / {len(documents)} documents uploaded")
            elif uploaded > 0:
                print(f"⚠️ {uploaded} / {len(documents)} documents uploaded")
            else:
                print(f"❌ Error occurred while connecting to {api_endpoint}, no document uploaded!")

    except Exception as e:
        print(f"❌ Exception occurred: '{e}'")