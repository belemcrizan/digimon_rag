import streamlit as st
import os
import json
from PIL import Image
from dotenv import load_dotenv
from rag_engine import get_rag_chain
from graph_engine import plot_digimon_graph

# Carrega variáveis do .env, incluindo OPENAI_API_KEY
load_dotenv()

def extrair_nome_digimon(user_input):
    with open("data/digimons.json", "r", encoding="utf-8") as f:
        digimons = json.load(f)
    nomes = [d["nome"].lower() for d in digimons]
    for word in user_input.lower().split():
        if word.lower() in nomes:
            return word.capitalize()
    return None

def main():
    st.set_page_config(page_title="Digimon RAG", layout="centered")
    st.title("🤖 Digimon RAG")
    st.markdown("Pergunte sobre qualquer **Digimon** e descubra seus pontos fortes, fracos e muito mais com **LangChain + Grafo!**")

    user_question = st.text_input("Digite sua pergunta:")

    if user_question:
        with st.spinner("🔍 Buscando resposta com LangChain..."):
            try:
                chain = get_rag_chain()
                result = chain.run(user_question)
                st.success(result)
            except Exception as e:
                st.error(f"Erro ao consultar o RAG: {str(e)}")
                return

        nome_digimon = extrair_nome_digimon(user_question)
        if nome_digimon:
            plot_digimon_graph(nome_digimon)
            if os.path.exists("graph.png"):
                st.image(Image.open("graph.png"), caption=f"Relações do {nome_digimon}")
        else:
            st.warning("🤔 Não consegui identificar o nome do Digimon na pergunta.")

if __name__ == "__main__":
    main()
