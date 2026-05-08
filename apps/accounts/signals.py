from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .tasks import send_message

@receiver(post_save, sender=get_user_model())
def send_welcome_email(sender, instance, created, **kwargs):
    if created:

        from config.settings import EMAIL_HOST_USER
        subject, from_email, to = ('Welcome to TraceElements! You have taken your first step towards health management.🍃',
                                   EMAIL_HOST_USER, instance.email)
        text_content = '<br>Good afternoon!' + instance.first_name + ' ' + instance.patronymic + '</br>'
        html_content = '<p>On behalf of the entire TraceElements team, we welcome you!</p> '
        html_content += 'We are glad that you chose our micronutrient indicator tracking app. . \
                        Now all your results will be under control, and their dynamics will be understandable and transparent..</p> '
        html_content += '<br>What to do next?</br>'
        html_content += '<p>1.  Add your details. It will only take a couple of minutes. \
                                Look at the screen and just fill in the boxes. </p> '
        html_content += '<p>2. Watch the trends. After adding the information, the calculation process is activated., \
                            and you will be able to view the charts for each indicator on the "Home" tab and in the  \
                            "Dynamics". This will help you see the full picture..</p> '
        html_content += '<p>3. Create profiles for your loved ones. Keep track of the health of the whole family in one app.</p> '
        html_content += '<br>We are always in touch:</br>'
        html_content += '<p> If you have any questions or suggestions on how to make the app better., \
                        just write to us in response to this letter or by email <a href="support@traceelements.app">[support@traceelements.app].</a></p>'
        html_content += '<p> Remember that our app is just a convenient digital assistant. Interpretation \
                        The results are for reference purposes only and do not replace consultation with a doctor..</p>'
        html_content += '<p>Thank you again for being with us. We wish you good health.!</p> '

        send_message.enqueue(subject, from_email, to, html_content, text_content)