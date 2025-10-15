import imaplib
import smtplib
from email.message import EmailMessage
from email import message_from_bytes
from app.services.ai.rag_service import run_rag_query
from app.core.config import Settings
from app.services.filter.filter_service import classify_message

def extract_email_body(msg):
    """Safely extract plain-text email body from multipart or single-part messages."""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition", ""))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    return part.get_payload(decode=True).decode(errors="ignore")
                except Exception:
                    pass
    else:
        try:
            return msg.get_payload(decode=True).decode(errors="ignore")
        except Exception:
            pass
    return "(No readable text found)"


def auto_reply_agent():
    # Connect to Gmail IMAP
    mail = imaplib.IMAP4_SSL(Settings.EMAIL_HOST)
    mail.login(Settings.EMAIL_ADDRESS, Settings.EMAIL_PASSWORD)
    mail.select("inbox")

    # Search unread emails
    status, data = mail.search(None, '(UNSEEN)')
    mail_ids = data[0].split()

    if not mail_ids:
        print("No new emails.")
        mail.logout()
        return

    for num in mail_ids:
        status, data = mail.fetch(num, "(RFC822)")
        raw_email = data[0][1]
        msg = message_from_bytes(raw_email)

        sender = msg["From"]
        receiver = msg["To"]
        subject = msg["Subject"]
        body = extract_email_body(msg)

        print(f"📩 New email from {sender}: {subject}")
        print(f"🧠 Extracted body:\n{body}")

        system_prompt = """
                You are an AI email assistant for given company.
                Use the given context to write a professional, concise email reply.
                Do not use markdown. Keep it short and clear.

                Your job is to generate only the final email reply body — nothing else.
                ❌ Do NOT include phrases like:
                - "Here’s a sample email"
                - "Email body:"
                - "Subject:"
                ✅ Only return the final, ready-to-send email message.

                Format:
                Dear [Name if known],

                [Professional and polite response text.]

                Best regards,
                [if know company name add here] Ai Support
                """

        
        # Classify email content
        filter = classify_message("email", body)
        print(f"Classified message category: {filter.category}")
        if filter.category in ["inquiry", "payment", "status", "order", "complaint"]:
            system_prompt += " to answer the question. If you don't know the answer, just say that you don't know, don't try to make up an answer. and say Company agent will contact you soon."
        else:
            system_prompt += ". If you don't know the answer, just say that you don't know, give answer from the context."

        
        # Generate AI reply
        ai_reply = run_rag_query( user_prompt=body, history=[], system_prompt =system_prompt)
        print(f"🤖 AI Reply:\n{ai_reply}")

        # Compose the reply
        reply = EmailMessage()
        reply["Subject"] = f"Re: {subject}"
        reply["From"] = receiver
        reply["To"] = sender
        email = "{ai_reply}\n\nThis is an automated response. Please do not reply to this email." \
        "" \
        "n\nBest regards,\nYour AI Assistant"
        reply.set_content(ai_reply)

        # Send reply
        with smtplib.SMTP_SSL(Settings.EMAIL_HOST, 465) as smtp:
            smtp.login(Settings.EMAIL_ADDRESS, Settings.EMAIL_PASSWORD)
            smtp.send_message(reply)

        print(f"✅ Replied to: {sender}")

    mail.logout()
