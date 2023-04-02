from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import EmailMessage
from roomsession.models import GmailAccount

def email():
    gmail_accounts = GmailAccount.objects.all()
    for gmail_account in gmail_accounts:
        mail_subject = "Activate your user account."
        message = "heelo"
        email = EmailMessage(mail_subject, message, to=[gmail_account.email])
        if email.send():
            print("ok")
        

def start():
	scheduler = BackgroundScheduler()
	scheduler.add_job(email, 'interval', seconds=10)
	scheduler.start()

start()