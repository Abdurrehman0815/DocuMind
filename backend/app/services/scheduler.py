import logging
import json
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.config.database import SessionLocal
from app.models.document import Document
from app.services.notifier import send_whatsapp_message

logger = logging.getLogger(__name__)

def check_upcoming_reminders():
    """
    Background job that runs daily to check for upcoming deadlines.
    Sends a WhatsApp message if a deadline is exactly 3 days away, or today.
    """
    logger.info("Running scheduled check for upcoming reminders...")
    
    db = SessionLocal()
    try:
        docs = db.query(Document).filter(Document.extracted_entities.isnot(None)).all()
        today = datetime.now().date()
        
        for doc in docs:
            entities = doc.extracted_entities
            if isinstance(entities, str):
                try:
                    entities = json.loads(entities)
                except:
                    continue
                    
            if not isinstance(entities, dict):
                continue
                
            due_date_str = entities.get("due_date") or entities.get("expiry_date")
            if not due_date_str:
                continue
                
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            except ValueError:
                continue
                
            days_until = (due_date - today).days
            
            # Send notification if exactly 3 days away or due today (or overdue by 1 day as a final warning)
            if days_until == 3 or days_until == 0 or days_until == -1:
                
                if days_until < 0:
                    priority = "CRITICAL"
                    timeframe = "YESTERDAY"
                elif days_until == 0:
                    priority = "HIGH"
                    timeframe = "TODAY!"
                else:
                    priority = "MEDIUM"
                    timeframe = "in 3 days"
                
                amount = entities.get("payment_amount", "")
                provider = entities.get("provider", doc.filename)
                
                body = f"🤖 *DocuMind - {priority} ALERT*\n\n"
                body += f"🚨 Your {provider} is due {timeframe} ({due_date_str}).\n"
                if amount:
                    body += f"📌 Amount: {amount}\n"
                body += f"\nPlease check your dashboard for more details."
                
                # Send the message
                send_whatsapp_message(body)
                
    except Exception as e:
        logger.error(f"Error in check_upcoming_reminders: {str(e)}")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Run every day at 9:00 AM
    scheduler.add_job(
        check_upcoming_reminders,
        trigger=CronTrigger(hour=9, minute=0),
        id="daily_reminder_job",
        name="Check deadlines and send WhatsApp notifications",
        replace_existing=True
    )
    scheduler.start()
    logger.info("Background scheduler started successfully.")
