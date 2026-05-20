from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# Load and split
docs = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100).split_documents(
    PyPDFLoader("test.pdf").load()
)

# Upload to Pinecone
PineconeVectorStore.from_documents(docs, OpenAIEmbeddings(), index_name="idx")
