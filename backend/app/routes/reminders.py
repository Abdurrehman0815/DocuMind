from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import json

from app.config.database import get_db
from app.middleware.auth import get_current_user
from app.models.document import Document

router = APIRouter(prefix="/reminders", tags=["Reminders"])

@router.get("")
def get_reminders(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Fetch all documents for this user that have extracted entities
    docs = db.query(Document).filter(
        Document.user_id == current_user.id,
        Document.extracted_entities.isnot(None)
    ).all()

    reminders = []
    
    for doc in docs:
        entities = doc.extracted_entities
        if isinstance(entities, str):
            try:
                entities = json.loads(entities)
            except:
                continue
                
        # Look for due dates or expiry dates
        if not isinstance(entities, dict):
            continue
            
        due_date = entities.get("due_date")
        expiry_date = entities.get("expiry_date")
        amount = entities.get("payment_amount")
        provider = entities.get("provider", doc.filename)
        
        date_str = due_date or expiry_date
        
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                days_diff = (date_obj - datetime.now().date()).days
                
                if days_diff < 0:
                    priority = "CRITICAL"
                elif days_diff <= 7:
                    priority = "HIGH"
                elif days_diff <= 30:
                    priority = "MEDIUM"
                else:
                    priority = "LOW"
            except:
                priority = "MEDIUM"
                
            reminders.append({
                "id": doc.id,
                "document_id": doc.id,
                "filename": doc.filename,
                "category": doc.category,
                "date": date_str,
                "type": "due_date" if due_date else "expiry_date",
                "amount": amount,
                "provider": provider,
                "priority": priority
            })
            
    # Sort by date
    reminders.sort(key=lambda x: x["date"])
    
    return reminders

@router.post("/test-whatsapp")
def test_whatsapp(current_user = Depends(get_current_user)):
    from app.services.notifier import send_whatsapp_message
    
    body = "🤖 *AI Life Admin - Test Notification*\n\nThis is a test message to confirm your WhatsApp integration is working perfectly! When deadlines approach, you will receive alerts like this."
    
    success = send_whatsapp_message(body)
    
    if success:
        return {"message": "Test WhatsApp message sent successfully."}
    else:
        return {"error": "Failed to send WhatsApp message. Please check Twilio configuration."}

@router.post("/trigger")
def trigger_reminders_manually(current_user = Depends(get_current_user)):
    """
    Manually trigger the background job that sends WhatsApp reminders.
    Useful for testing the actual cron job logic immediately.
    """
    try:
        from app.services.scheduler import check_upcoming_reminders
        check_upcoming_reminders()
        return {"message": "Reminders triggered successfully! If any documents are due within 3 days, you will receive a WhatsApp message right now."}
    except Exception as e:
        return {"error": str(e)}
