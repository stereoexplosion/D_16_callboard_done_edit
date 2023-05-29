from datetime import datetime, timedelta
from celery import shared_task

from .models import *


@shared_task
def delete_o_t_code():
    OneTimeCode.objects.all().filter(code_create_time__gte=datetime.now() - timedelta(minutes=5)).delete()
