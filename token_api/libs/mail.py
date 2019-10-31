# python imports
import logging
import datetime

# django level imports
from django.core.mail import EmailMessage,send_mail

# project imports
from token_api.settings import EMAIL_HOST_USER

#Third party imports
from celery import shared_task


logger = logging.getLogger(__name__)

@shared_task
def sendmail(message,subject,tolist):
	try:
		# msg = EmailMessage(subject, message, EMAIL_HOST_USER, tolist) 
		# msg.send(fail_silently=True)
		print(message,subject,tolist)
		send_mail(subject, message, EMAIL_HOST_USER, tolist)
		logger.info("Mail Sent ")
		return 1
	except:
		logger.error("Sending mail is failed", exc_info=True)
		return 0




