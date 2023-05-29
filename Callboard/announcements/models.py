from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField


class Announcement(models.Model):
    tanks = 'TK'
    heals = 'HS'
    dd = 'DD'
    merchants = 'MC'
    guild_masters = 'GM'
    quest_givers = 'QG'
    blacksmiths = 'BS'
    tanners = 'TN'
    potion_makers = 'PM'
    spell_masters = 'SM'
    POSITIONS = [
        (tanks, 'Танки'),
        (heals, 'Хилы'),
        (dd, 'ДД'),
        (merchants, 'Торговцы'),
        (guild_masters, 'Гилдмастеры'),
        (quest_givers, 'Квестгиверы'),
        (blacksmiths, 'Кузнецы'),
        (tanners, 'Кожевники'),
        (potion_makers, 'Зельевары'),
        (spell_masters, 'Мастера заклинаний'),
    ]
    a_author = models.ForeignKey(User, on_delete=models.CASCADE)
    category_choice = models.CharField(max_length=2, choices=POSITIONS, default=tanks)
    a_create_time = models.DateTimeField(auto_now_add=True)
    a_header = models.CharField('Заголовок', max_length=64)
    a_body = RichTextUploadingField()

    def __str__(self):
        return '{}'.format(self.a_header)

    def get_absolute_url(self):
        return reverse('announcement_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class Response(models.Model):
    r_author = models.ForeignKey(User, on_delete=models.CASCADE)
    r_announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    r_create_time = models.DateTimeField(auto_now_add=True)
    r_text = models.TextField('Текст')
    accept_decline = models.BooleanField(null=True)

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'

    def preview(self):
        return self.r_text[0:40] + '...'


class Subscribe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.BooleanField(default=False)
