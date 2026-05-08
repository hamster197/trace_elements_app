from django.tasks import task
from django.core.mail import EmailMultiAlternatives


@task()
def send_message(subject, from_email, to, html_content, text_content):
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()