from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import *
from .models import *
from .filters import *


class AnnouncementsList(ListView):
    model = Announcement
    ordering = '-id'
    template_name = 'announcement/announcements.html'
    context_object_name = 'announcements'
    paginate_by = 10


class AddAnnouncement(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    raise_exception = True
    permission_required = ('announcements.add_announcement',)
    form_class = AnnouncementForm
    model = Announcement
    template_name = "announcement/add_announcement.html"
    success_url = reverse_lazy('announcements_list')

    def post(self, request, *args, **kwargs):  # Принятие формы с комментарием, определение id поста и автора, редирект
        if self.request.method == 'POST':  # обратно
            announcement_form = AnnouncementForm(data=self.request.POST)
            new_response = announcement_form.save(commit=False)
            new_response.a_author_id = self.request.user.id
            new_response.save()
            return redirect("http://127.0.0.1:8000/announcements")


class AnnouncementsDetail(DetailView):
    model = Announcement
    template_name = 'announcement/announcement.html'
    context_object_name = 'announcement'

    def get_context_data(self, **kwargs):  # Сбор данных для использования в html
        context = super().get_context_data(**kwargs)
        activities = self.get_related_activities(context)
        context['responses'] = activities
        context['page_obj'] = activities
        context['response_form'] = ResponseForm
        return context

    def post(self, request, *args, **kwargs):  # Принятие формы с комментарием, определение id поста и автора, редирект
        if self.request.method == 'POST':  # обратно
            response_form = ResponseForm(data=self.request.POST)
            new_response = response_form.save(commit=False)
            new_response.r_announcement_id = self.get_object().id
            new_response.r_author_id = self.request.user.id
            pk = new_response.r_announcement_id
            new_response.save()
            return redirect("http://127.0.0.1:8000/announcements/" + str(pk))

    def get_related_activities(self, context):  # Реализация пагинации для DetailView вручную
        queryset = Response.objects.filter(r_announcement=context['announcement']).order_by('-r_create_time')
        paginator = Paginator(queryset, 5)  # paginate_by
        page = self.request.GET.get('page')
        activities = paginator.get_page(page)
        return activities


class AnnouncementUpdate(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    raise_exception = True
    permission_required = ('announcements.change_announcement',)
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcement/announcement_edit.html'


class AnnouncementDelete(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    raise_exception = True
    permission_required = ('announcements.delete_announcement',)
    model = Announcement
    template_name = 'announcement/announcement_delete.html'
    success_url = reverse_lazy('announcements_list')


class AnnouncementPersonal(LoginRequiredMixin, ListView):
    model = Announcement
    raise_exception = True
    template_name = 'announcement/personal_page.html'
    context_object_name = 'response_search'
    queryset = Announcement.objects.all().values().order_by('-id')
    paginate_by = 10
    form_class = AnnouncementResponseForm

    def get_queryset(self):
        queryset = Announcement.objects.filter(a_author=self.request.user)
        self.filterset = AnnouncementResponseFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Забираем отфильтрованные объекты
        context['filterset'] = self.filterset
        context['filter'] = AnnouncementResponseFilter(self.request.GET,
                                                       queryset=self.get_queryset())  # вписываем фильтр в контекст
        context['form'] = AnnouncementResponseForm()
        return context


@login_required
@csrf_protect
def accept_decline(request, pk):
    ann = Response.objects.filter(id=pk).values_list('r_announcement_id', flat=True)
    for ann_ in ann:
        ann_author = Announcement.objects.filter(id=ann_).values_list('a_author_id', flat=True)
    for author in ann_author:
        if request.user.id == author:
            if request.method == 'POST':
                action = request.POST.get('action')
                if action == 'accept':
                    Response.objects.filter(id=pk).update(accept_decline=True)
                elif action == 'decline':
                    Response.objects.filter(id=pk).update(accept_decline=False)

                return redirect('/announcements/' + ' '.join(map(str, ann)))
        else:
            return render(
                request,
                'rights_exception.html',
            )

    return render(
        request,
        'response/response_update.html',
    )


@login_required
@csrf_protect
def subscribe(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscribe.objects.create(user=request.user, subscription=True)
        elif action == 'unsubscribe':
            Subscribe.objects.filter(user=request.user).delete()
        return redirect('/announcements/')

    user_subscribed = Subscribe.objects.filter(user=request.user)

    return render(
        request,
        'announcement/subscribe.html',
        {'user_subscribed': user_subscribed},
    )
