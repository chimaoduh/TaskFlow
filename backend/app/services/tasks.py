import logging
from app.celery_app import celery

logger = logging.getLogger(__name__)


@celery.task(name="taskflow.demo_notification")
def send_demo_notification(task_title: str) -> dict:
    # Demonstration only: replace this with a real email provider integration.
    message = f"Background worker processed task: {task_title}"
    logger.info(message)
    return {"status": "processed", "message": message}
