from django.conf import settings
from django.core.mail import send_mail

def send_verification_mail(email_subject,message,to_email):
	return send_mail(
	    email_subject, 
	    message , 
	    settings.DEFAULT_FROM_EMAIL,
	    [to_email,]
	)