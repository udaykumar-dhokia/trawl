from fastapi import FastAPI
from .db.database import engine
from .models import Base
from .models.response import Response
from .models.documents import Document, DocumentChunk
from .models.chat import Chat

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Hello World"}