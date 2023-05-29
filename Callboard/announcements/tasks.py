from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime, timedelta
from celery import shared_task

from .models import *


@shared_task
def new_response(pk: int, preview: str, announcement_header: str, ann_author_email: list):
    for pk_ in pk:
        for announcement_header_ in announcement_header:
            subject = f'Новый отклик в вашем объявлении: {announcement_header_}'
            text_content = (
                f'Превью: {preview}\n\n'
                f'Ссылка на объявление: http://127.0.0.1:8000/announcements/{pk_}'
            )
            html_content = (
                f'Превью: {preview} <br><br>'
                f'<a href="http://127.0.0.1:8000/announcements/{pk_}">'
                f'Ссылка на объявление</a>'
            )
            for email in ann_author_email:
                msg = EmailMultiAlternatives(subject, text_content, None, [email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()


@shared_task
def new_response_accept(pk: int, announcement_header: str, res_author_email: list):
    for pk_ in pk:
        for announcement_header_ in announcement_header:
            subject = f'Ваш отклик на объявление {announcement_header_} был принят!'
            text_content = (
                f'Ссылка на объявление: http://127.0.0.1:8000/announcements/{pk_}'
            )
            html_content = (
                f'<a href="http://127.0.0.1:8000/announcements/{pk_}">'
                f'Ссылка на объявление</a>'
            )
            for email in res_author_email:
                msg = EmailMultiAlternatives(subject, text_content, None, [email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()


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
