from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime, timedelta
from celery import shared_task

from .models import *


def get_unique_subscribed_users() -> list:
    subscribed_users = Subscribe.objects.all().values_list('user_id', flat=True).distinct()
    return subscribed_users


def get_announcements_from_the_last_day() -> list:
    announcements_last_day = Announcement.objects.all().filter(a_create_time__gte=datetime.now() - timedelta(minutes=60 * 24))
    return announcements_last_day


def get_subscribed_user_email(user: int) -> list:
    return User.objects.filter(id=user).values_list('email', flat=True)


@shared_task
def daily_subscribers_email():
    """Newsletter for subscribers with publications published in the last day, used by celery."""
    for user in get_unique_subscribed_users():
        subject = 'За последний день вышли следующие объявления :'
        text_content = ''
        html_content = ''
        for publication in get_announcements_from_the_last_day():
            text_content_que: str = (
                f'Заголовок: {publication.a_header}\n'
                f'Ссылка на объявление: http://127.0.0.1:8000{publication.get_absolute_url()}\n\n'
            )
            text_content += text_content_que
            html_content_que: str = (
                f'Заголовок: {publication.a_header}<br>'
                f'<a href="http://127.0.0.1:8000{publication.get_absolute_url()}">'
                f'Ссылка на объявление</a><br><br>'
            )
            html_content += html_content_que
        for email in get_subscribed_user_email(user):
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
