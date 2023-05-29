from django.forms import DateTimeInput

from django_filters import FilterSet, DateTimeFilter, CharFilter, ModelChoiceFilter

from .models import *


class AnnouncementResponseFilter(FilterSet):
    ann = CharFilter(field_name='a_header')
    added_after = DateTimeFilter(
        field_name='a_create_time',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        class Meta:
            model = Announcement
            fields = {
                'name': ['icontains'],
            }
