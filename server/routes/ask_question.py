import os
from fastapi import APIRouter,Form
from fastapi.responses import JSONResponse
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, pinecone
from pydantic import Field
from typing import List, Optional
from logger import logger
from dotenv import load_dotenv


router = APIRouter()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME=os.getenv("PINECONE_INDEX_NAME")
@router.post("/ask")
async def ask_question(question:str=Form(...)):
    try:
        logger.info(f"User query:{question}")
    #embed model + pinecone setup
        print(PINECONE_INDEX_NAME);
        print(PINECONE_API_KEY);
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index=pc.Index(PINECONE_INDEX_NAME)
        embed_model =  OpenAIEmbeddings( model="text-embedding-3-large",dimensions=1024)
        embedded_query = embed_model.embed_query(question)
        res=index.query(vector=embedded_query,top_k=3,include_metadata=True)
        docs =[
            Document(
                page_content=match["metadata"].get("text",""),\
                metadata=match["metadata"]
            ) for match in res["matches"]
        ]

        class SimpleRetriever(BaseRetriever):
            documents: List[Document] = Field(..., description="...")
            k: int = 5

            def _get_relevant_documents(self, query: str) -> List[Document]:
                # Simple keyword filter (optional improvement)
                query_lower = query.lower()
                scored = [
                    (doc, sum(1 for word in query_lower.split() if word in doc.page_content.lower()))
                    for doc in self.documents
                ]
                scored.sort(key=lambda x: x[1], reverse=True)
                return [doc for doc, _ in scored[:self.k]]

            
        retriever = SimpleRetriever(
            documents=docs,   # ← Must be keyword argument
            k=10
        )
        chain = get_llm_chain(retriever)
        result=query_chain(chain,question)
        logger.info("Query is successfull")

        return result            

    except Exception as e :
        logger.exception("Error processing question")
        return JSONResponse(status_code=500,content={"error":str(e)})


