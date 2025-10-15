from sqlalchemy import select
from app.db.model.document_model import Document
from app.core.config import SessionLocal
from app.services.embedding.embedding_model import get_embedding_model

def retrieve_company_context( query: str, top_k: int = 1):
    db = SessionLocal()
    embedding_model = get_embedding_model()
    query_vector = embedding_model.encode([query])[0].tolist()

    results = db.scalars(
        select(Document)
        .order_by(Document.embedding.cosine_distance(query_vector))
        .limit(top_k)
    ).all()

    db.close()
    return "\n".join([doc.content for doc in results])
