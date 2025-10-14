# app/services/message_filter.py
from pydantic import BaseModel, Field
from typing import Literal
from langchain_groq import ChatGroq
from app.core.config import Settings

# Define your output schema
class MessageCategory(BaseModel):
    """Classify incoming messages into a structured category."""
    
    category: Literal["general", "inquiry", "payment", "status", "order", "complaint", "other"] = Field(
        description="Category of the message"
    )
    confidence: float = Field(description="Confidence score between 0 and 1")


# Initialize LLM with structured output
def get_message_classifier():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=Settings.GROQ_API_KEY,
        temperature=0,
    )
    return llm.with_structured_output(MessageCategory)

# Run classification
def classify_message(source: str, text: str) -> MessageCategory:
    """
    source: where the message came from (email, whatsapp, api)
    text: message content
    """
    llm = get_message_classifier()

    prompt = f"""
    You are an AI CRM message classifier.
    The message came from: {source}.
    Categorize it as one of:
    [general, inquiry, payment, status, order, complaint, other].

    Follow the schema carefully.

    Available message categories:
    - general_question: general queries not tied to transactions.
    - inquiry: product/service-related inquiries or information requests.
    - payment: anything related to payment, billing, invoice, refund, or receipts.
    - order: order placement, confirmation, cancellation, tracking.
    - status: requests or updates about ongoing processes, delivery, or account.
    - complaint: issues, dissatisfaction, or negative feedback.
    - other: if it doe not fit above categories.
    
    Respond in JSON format following the schema.
    Message: "{text}"
    """

    result = llm.invoke(prompt)
    return result
