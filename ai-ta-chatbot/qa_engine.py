from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import os
from config import openai_api_key

os.environ["OPENAI_API_KEY"] = openai_api_key

def load_and_index_documents():
    docs = []
    for filename in os.listdir("./data"):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(f"./data/{filename}")
            pages = loader.load()
            docs.extend(pages)

    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local("embeddings")
    return vector_store

def get_answer_from_query(query):
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.load_local("embeddings", embeddings)
    retriever_docs = vector_store.similarity_search(query)
    llm = OpenAI(temperature=0.5)
    chain = load_qa_chain(llm, chain_type="stuff")
    result = chain.run(input_documents=retriever_docs, question=query)
    return result
