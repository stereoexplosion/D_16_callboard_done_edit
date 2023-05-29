from django import forms

from .models import Announcement, Response


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['category_choice', 'a_header', 'a_body']


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['r_text']


class AnnouncementResponseForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['a_header']


class ResponseUpdateForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['accept_decline']
