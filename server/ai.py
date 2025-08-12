'''This module utilises LLM and Langchain tools to summarise website content'''

from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline, HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
import torch

MODEL_NAME = "sshleifer/distilbart-cnn-12-6" #lightweight model for my machine, adjust as needed

EMBEDDINGS = None
MODEL = None
LLM = None


def init_llm():
    '''Initialises LLM'''

    global LLM, EMBEDDINGS

    summariser = pipeline("summarization", model=MODEL_NAME)
    LLM = HuggingFacePipeline(pipeline=summariser)
    EMBEDDINGS = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def summarise_text(db, k=4):
    '''Summarises text using a vector database'''

    query = "summarise the following text by finding the key points"
    docs = db.similarity_search(query, k=k)
    docs_page_content = "".join([d.page_content for d in docs])

    prompt_template_for_text = PromptTemplate.from_template(
        "Summarise the following text in maximum 3 short sentences: {text}. Make sure it is suited for someone who may want to use this source in an academic context.")

    chain = prompt_template_for_text | LLM

    response = chain.invoke({'text': docs_page_content})
    return response


def create_vector_db_from_text(site_text) -> FAISS:
    '''Uses similarity search to split site content into smaller chunks'''
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(site_text)
    db = FAISS.from_documents(docs, EMBEDDINGS)
    return db

def summarise_source(site_text: str) -> str:
    '''Takes site text as input and returns a summary'''
    if not site_text:
        raise ValueError("site_text is empty or None")

    docs = [Document(page_content=site_text)]
    db = create_vector_db_from_text(docs)
    summary = summarise_text(db)

    debug_summary = summary.replace("Make sure it is suited for someone who may want to use this source in an academic context", "")
    debug_summary2 = debug_summary.replace("Summarise the following text in maximum 3 short sentences", "")
    return debug_summary2

init_llm()

