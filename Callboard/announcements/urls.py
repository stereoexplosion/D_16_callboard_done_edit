from django.urls import path
from .views import *

urlpatterns = [
    path('', AnnouncementsList.as_view(), name='announcements_list'),
    path('create/', AddAnnouncement.as_view(), name='add_announcement'),
    path('<int:pk>/', AnnouncementsDetail.as_view(), name='announcement_detail'),
    path('<int:pk>/response_update/', accept_decline, name='response_update'),
    path('<int:pk>/edit/', AnnouncementUpdate.as_view(), name='announcement_edit'),
    path('<int:pk>/delete/', AnnouncementDelete.as_view(), name='announcement_delete'),
    path('personal/', AnnouncementPersonal.as_view(), name='announcement_personal'),
    path('subscribe/', subscribe, name='announcement_personal'),
]
