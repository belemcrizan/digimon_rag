from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import JSONLoader
from langchain.chat_models import ChatOpenAI
import os

def load_vectorstore():
    loader = JSONLoader(file_path="data/digimons.json", jq_schema=".[]", text_content=False)
    docs = loader.load()
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(docs, embeddings)

def get_rag_chain():
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_type="similarity", k=3)
    llm = ChatOpenAI(temperature=0.3)
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
