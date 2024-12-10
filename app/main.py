# main.py
from fastapi import FastAPI
from app.interfaces.api.routes import generation, verification, parse
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Create a rotating file handler
file_handler = RotatingFileHandler('app.log', maxBytes=1024*1024*5, backupCount=5)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Add the file handler to the root logger
logging.getLogger('').addHandler(file_handler)

app = FastAPI(
    title="AutoAumento API",
    description="API for text generation, parsing and verification using LLMs and custom rules.",
    version="1.0.0"
)

app.include_router(generation.router, prefix="/generation", tags=["Generation"])
app.include_router(parse.router, prefix="/parse", tags=["Parsing"])
app.include_router(verification.router, prefix="/verification", tags=["Verification"])