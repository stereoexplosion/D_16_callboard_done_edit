from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Announcement, Response, User
from .tasks import new_response, new_response_accept


@receiver(post_save, sender=Response)
def response_created(sender, instance, **kwargs):
    announcement_id = instance.r_announcement_id
    ann_author = Announcement.objects.filter(id=announcement_id).values_list('a_author_id', flat=True)
    for _id in ann_author:
        ann_author_email = list(User.objects.filter(id=_id).values_list('email', flat=True))
    announcement_header = list(Announcement.objects.filter(id=announcement_id).
                               values_list('a_header', flat=True))
    new_response.delay(announcement_id, instance.preview(), announcement_header, ann_author_email)


@receiver(post_save, sender=Response)
def response_accept(sender, instance,  **kwargs):
    if instance.accept_decline is True:
        announcement_header = list(Announcement.objects.filter(id=instance.r_announcement_id).
                                   values_list('a_header', flat=True))
        announcement_id = instance.r_announcement_id
        res_author_email = list(User.objects.filter(id=instance.r_author_id).values_list('email', flat=True))
        new_response_accept.delay(announcement_id, announcement_header, res_author_email)
