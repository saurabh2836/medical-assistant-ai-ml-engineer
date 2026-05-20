from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from middlewares.exception_handlers import catch_exception_middleware
from routes.upload_pdfs import router as upload_router
from routes.ask_question import router as ask_question

app = FastAPI(title =" Medical Assistant API",decription="API For AI Medical Assistant Chatbot")

#CORS Setup

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # This must be a boolean value
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def root():
    return {"saurabh kamble is god1"}



app.middleware("http")(catch_exception_middleware)


#routers
#1. uploading pdfs documents 
app.include_router(upload_router)
#2. asking query
app.include_router(ask_question)


