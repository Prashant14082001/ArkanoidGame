# from celery import shared_task

# @shared_task
# def sum_numbers(a, b):
#     result = a + b
#     print(f'The sum of {a} and {b} is {result}')
#     return result



from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import time


@shared_task
def send_periodic_email():
    subject = 'Testing my code'
    message = 'This is a test email sent via Celery Beat.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['anna@yopmail.com']
    
    send_mail(subject, message, email_from, recipient_list)
    return 'Email sent successfully at {}'.format(time.ctime())


# celery -A WeatherProject worker --loglevel=info

# celery -A WeatherProject beat --loglevel=info