from celery.decorators import task
from celery.utils.log import get_task_logger
from BlogApp.utils import send_verification_mail

logger = get_task_logger(__name__)

@task(name="send_verification_mail_task")
def send_verification_mail_task(email_subject,message,to_email):
    logger.info("Sent verification email")
    return send_verification_mail(email_subject,message,to_email)