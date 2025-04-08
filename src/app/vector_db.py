from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
from .config import (
    EMBEDDING_MODEL,
    OPENAI_API_BASE,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    VECTOR_DB_PATH,
)

embedding = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    openai_api_base=OPENAI_API_BASE,
)


def build_vector_db(doc_path: str):
    loader = TextLoader(doc_path, encoding="utf-8")
    documents = loader.load()

    text = documents[0].page_content
    split_docs = text.split("【")
    docs = []
    for doc in split_docs:
        if doc.strip():
            title, content = doc.split("】", 1)
            docs.append(f"【{title.strip()}】{content.strip()}")

    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    # )
    # docs = text_splitter.split_documents(documents)

    vector_db = FAISS.from_texts(docs, embedding)
    vector_db.save_local(VECTOR_DB_PATH)
    return vector_db


def load_vector_db():
    if not os.path.exists(VECTOR_DB_PATH):
        vector_db = build_vector_db()
    else:
        vector_db = FAISS.load_local(
            VECTOR_DB_PATH, embedding, allow_dangerous_deserialization=True
        )
    return vector_db
