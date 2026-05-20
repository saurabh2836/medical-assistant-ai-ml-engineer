import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain

load_dotenv()

# LangChain automatically looks for GROQ_API_KEY in your environment variables,
# but it's totally fine to grab it explicitly like this.
GROQ_API_KEY = os.getenv("GROQ_API_KEY")



def get_llm_chain(retriever):
    # 1. Initialize the modern Groq LLM
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,      # Note: lowercase 'groq_api_key' is preferred in newer versions
        model='llama-3.3-70b-versatile',         # Fixed the typo in the model name ('9=8192' -> '8192')
        temperature=0.2,                 # Added the missing comma here
        max_tokens=None,
        timeout=None,
        max_retries=2
    )

    # 2. Define a structured chat prompt
    # Cleaned up the formatting so it passes into the tuple correctly as a single string
    system_prompt = (
        "You are **MediBot**, an AI-powered assistant trained to help users understand "
        "medical documents and health-related questions. Your job is to provide a clear, "
        "accurate, and helpful response based **only on the provided context**.\n\n"
        "**Context:**\n{context}\n\n"
        "**Instructions:**\n"
        "- Respond in a calm, factual, and respectful tone.\n"
        "- Use simple language. If the context does not contain the answer, say exactly: "
        "\"I'm sorry, but I couldn't find relevant information in the provided documents.\"\n"
        "- Do not make up facts.\n"
        "- Do not give medical advice or diagnoses."
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "**User Question:** {input}")  # Modern chains look for {input} by default
    ])

    # 3. Create the modern document chain (replaces the old 'stuff' chain_type)
    question_answer_chain = create_stuff_documents_chain(llm, prompt)

    # 4. Create the final retrieval chain
    # This combines your retriever with the LLM/prompt chain seamlessly
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    return rag_chain