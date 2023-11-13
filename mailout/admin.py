from django.contrib import admin

from mailout.models import Client, Message, Mailout, Log


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'email', 'auth_user')
    search_fields = ('first_name', 'last_name', 'email', 'auth_user')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subject', 'body', 'auth_user')
    search_fields = ('subject', 'auth_user')


@admin.register(Mailout)
class MailoutAdmin(admin.ModelAdmin):
    list_display = ('pk', 'start_time', 'finish_time', 'freq', 'status')
    search_fields = ('start_time', 'finish_time', 'status', 'is_active', 'auth_user', 'clients')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'last_attempt', 'status', 'server_response', 'mailout', 'auth_user')
