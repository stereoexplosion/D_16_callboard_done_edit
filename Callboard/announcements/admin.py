from django import forms
from django.contrib import admin
from .models import *
from ckeditor.widgets import CKEditorWidget


admin.site.register(Announcement)
admin.site.register(Response)
admin.site.register(Subscribe)
