from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import re
import os


# --- Load .txt documents from directory ---
def load_documents_from_directory(directory_path: str):
    loader = DirectoryLoader(
        path=directory_path,
        glob="**/*.txt",
        loader_cls=lambda p: TextLoader(p, encoding="utf-8"),  # ✅ force UTF-8
        show_progress=True
    )
    return loader.load()


# --- Split text into product-level documents ---
def split_document_by_products(text: str):
    product_pattern = r'###\*\*Product Name\*\*###'
    products = re.split(f'(?={product_pattern})', text)

    split_docs = []

    for product in products:
        product = product.strip()
        if not product:
            continue

        name_match = re.search(r'###\*\*Product Name\*\*###:?\s*\n\s*(.+)', product)
        product_name = name_match.group(1).strip() if name_match else "Unknown Product"

        split_docs.append(
            Document(
                page_content=product,
                metadata={"product_name": product_name}
            )
        )

    return split_docs


# --- Main Pipeline ---
def main():
    # Step 1: Load documents
    directory_path = os.path.join(
        os.environ["USERPROFILE"], "Desktop", "rdl_data", "knowledge_base"
    )
    documents = load_documents_from_directory(directory_path)

    # Step 2: Preprocess and chunk
    all_chunks = []
    for doc in documents:
        chunks = split_document_by_products(doc.page_content)
        all_chunks.extend(chunks)

    # 🔹 Debugging: show file names
    print(f"\n✅ Total documents loaded: {len(documents)}")
    for i, doc in enumerate(documents, 1):
        print(f"Doc {i}: {doc.metadata['source']}")

    # 🔹 Show only first 50 chunks (if available)
    print(f"\n✅ Total chunks loaded: {len(all_chunks)}")

    for i, doc in enumerate(all_chunks, 1):
       print(f"Chunk {i}")
       print("Content:", doc.page_content[:400], "...")  # show first 400 chars
       print("Metadata:", doc.metadata)
       print("=" * 50)

    print(f"\n✅ Displayed all {len(all_chunks)} chunks")


if __name__ == "__main__":
    main()
