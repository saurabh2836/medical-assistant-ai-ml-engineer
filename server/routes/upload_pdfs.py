
from fastapi import APIRouter,UploadFile,File, Request
from typing import List
from modules.load_vectorstore import load_vectorstore
from fastapi.responses import JSONResponse
from logger import logger
import time

router= APIRouter()

#middleware expection handlers

@router.post("/upload_pdfs/")

async def upload_pdfs(files:List[UploadFile]=File(...)):
     try:
          logger.info("Received uploaded files")
          load_vectorstore(files)
          logger.info("Document added to vectorstore")
          return {"messages":"Files processed and vectorstore updated"}
     except Exception  as e :
         logger.exception("error during PDF upload")
         return JSONResponse(status_code=500,content={"error":str(e)})
