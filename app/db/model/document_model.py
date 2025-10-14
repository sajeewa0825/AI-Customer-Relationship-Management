from sqlalchemy import Column, Integer, String, Float
from pgvector.sqlalchemy import Vector

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Document(Base):
    __tablename__ = "vector_document"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, index=True)
    content = Column(String, nullable=False)
    document_meta = Column(String, nullable=True)
    embedding = Column(Vector(384)) 