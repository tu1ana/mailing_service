from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig


class MailoutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailout'

    # def ready(self):
    #     scheduler = BackgroundScheduler()
    #     from . import services
    #     services.launch_scheduler(scheduler)
