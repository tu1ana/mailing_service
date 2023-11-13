from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django_apscheduler.jobstores import DjangoJobStore

from blog.models import Blog
from mailout.forms import MailoutForm, MessageForm, ClientForm
from mailout.models import Mailout, Log, Client, Message
from mailout.services import launch_scheduler

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')


class IndexView(TemplateView):
    """Количество рассылок, количество активных рассылок, количество уникальных клиентов для рассылок,
    3 случайные статьи из блога. Кеширование"""
    template_name = 'mailout/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # random_pk = choice(Blog.objects.values_list('pk', flat=True))
        context_data = {
            'mailout_count': Mailout.objects.count(),
            'mailout_active_count': Mailout.objects.filter(is_active=True).count(),
            'client_count': Client.objects.count(),
            # 'random_obj': Blog.objects.get(pk=random_pk)
            'random_blog_list': Blog.objects.order_by('?')[:3],
            'title': 'Сервис рассылок - Главная'
        }
        # pks = Blog.objects.values_list('pk', flat=True)
        # random_pk = choice(pks)
        # random_obj = Blog.objects.get(pk=random_pk)
        return context_data


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'Новой сообщение от {name} ({email}): {message}')

    context = {
        'title': 'Контакты'
    }
    return render(request, 'mailout/contact.html', context)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Клиенты'
        context_data['object_list'] = Client.objects.filter(auth_user=self.request.user)

        return context_data


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailout:client_list')
    extra_context = {'title': 'Создание клиента'}

    def form_valid(self, form):
        self.object = form.save()
        self.object.auth_user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    # success_url = reverse_lazy('main:client_update')
    extra_context = {'title': 'Редактирование клиента'}


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailout:client_list')
    extra_context = {'title': 'Удаление клиента'}


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    extra_context = {'title': 'Редактирование клиента'}


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Рассылки'
        if self.request.user.has_perm('mailout.view_all_messages'):
            context_data['object_list'] = Message.objects.all()
        else:
            context_data['object_list'] = Message.objects.filter(auth_user=self.request.user)
        return context_data


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailout:message_list')
    extra_context = {'title': 'Создать новое сообщение'}

    def form_valid(self, form):
        self.object = form.save()
        self.object.auth_user = self.request.user
        self.object.save()

        log = Log.objects.create(last_attempt=datetime.now(), status='создана', server_response='-', message=self.object)
        log.save()

        launch_scheduler(scheduler)

        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    extra_context = {'title': 'Просмотр рассылки'}


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailout:message_list')
    extra_context = {'title': 'Редактирование рассылки'}


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailout:message_list')
    extra_context = {'title': 'Удаление рассылки'}


class MailoutListView(LoginRequiredMixin, ListView):
    model = Mailout

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.user.has_perm('mailout.view_all'):
            context_data['object_list'] = Mailout.objects.all()
        else:
            context_data['object_list'] = Mailout.objects.filter(auth_user=self.request.user)
        return context_data


class MailoutCreateView(LoginRequiredMixin, CreateView):
    model = Mailout
    form_class = MailoutForm
    success_url = reverse_lazy('mailout:list')
    extra_context = {'title': 'Создание рассылки'}

    def form_valid(self, form):
        self.object = form.save()
        self.object.auth_user = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailoutDetailView(LoginRequiredMixin, DetailView):
    model = Mailout


class MailoutUpdateView(UpdateView):
    model = Mailout
    form_class = MailoutForm
    success_url = reverse_lazy('mailout:list')


class MailoutDeleteView(DeleteView):
    model = Mailout
    success_url = reverse_lazy('mailout:list')


class LogListView(LoginRequiredMixin, ListView):
    model = Log
    extra_context = {'title': 'Логи рассылки'}

    def get_queryset(self):
        queryset = super().get_queryset().filter(auth_user=self.request.user).filter(mailout_id=self.kwargs.get('pk'))
        queryset = queryset.order_by('-pk')

        return queryset


def toggle_activity_mailout(request, pk):
    item = get_object_or_404(Mailout, pk=pk)
    if item.is_active:
        item.is_active = False
    else:
        item.is_active = True

    item.save()
    return redirect(reverse('mailout:list'))
