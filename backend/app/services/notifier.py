import logging
from twilio.rest import Client
from app.config.settings import settings

logger = logging.getLogger(__name__)

def send_whatsapp_message(body: str, to_number: str = None):
    """
    Sends a WhatsApp message using Twilio.
    If no to_number is provided, defaults to the user_whatsapp_number in settings.
    """
    if not settings.twilio_account_sid or not settings.twilio_auth_token:
        logger.warning("Twilio credentials not configured. Skipping WhatsApp notification.")
        return False
        
    if not settings.twilio_whatsapp_number:
        logger.warning("Twilio WhatsApp from-number not configured.")
        return False
        
    target_number = to_number or settings.user_whatsapp_number
    if not target_number:
        logger.warning("No target WhatsApp number configured.")
        return False

    try:
        client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
        
        message = client.messages.create(
            from_=settings.twilio_whatsapp_number,
            body=body,
            to=target_number
        )
        
        logger.info(f"WhatsApp message sent successfully: {message.sid}")
        return True
    except Exception as e:
        logger.error(f"Failed to send WhatsApp message: {str(e)}")
        return False
