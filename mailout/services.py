from datetime import datetime
from smtplib import SMTPException

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.utils.timezone import now

from django.conf import settings

from mailout.models import Message, Client, Mailout, Log


def send_message():
    message = Message

    for client in Client.objects.all():
        try:
            send_mail(
                subject=message.subject,
                message=message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email],
                fail_silently=False
            )
            log = Log.objects.create(last_attempt=datetime.now(),
                                     server_response='Сообщение успешно отправлено',
                                     status='Success',
                                     message=message)
            log.save()
        except SMTPException as e:
            log = Log.objects.create(last_attempt=datetime.now(),
                                     server_response=e.args,
                                     status='Error',
                                     message=message)
            log.save()


def create_task(scheduler, mailout: Mailout):
    mailout.message.job_id = f'Задача {mailout.message.pk}'
    mailout.save()

    start_time = mailout.start_time
    finish_time = mailout.finish_time

    if mailout.freq == 'DY':
        trigger = CronTrigger(second=start_time.second,
                              minute=start_time.minute,
                              hour=start_time.hour,
                              start_date=start_time,
                              end_date=finish_time
                              )
    elif mailout.freq == 'WK':
        trigger = CronTrigger(second=start_time.second,
                              minute=start_time.minute,
                              hour=start_time.hour,
                              day_of_week=start_time.weekday(),
                              start_date=start_time,
                              end_date=finish_time
                              )
    else:
        trigger = CronTrigger(second=start_time.second,
                              minute=start_time.minute,
                              hour=start_time.hour,
                              day_of_week=start_time.weekday(),
                              start_date=start_time,
                              end_date=finish_time
                              )
    scheduler.add_job(
        send_message,
        args=(mailout.message,),
        trigger=trigger,
        id=mailout.message.job_id,
        max_instances=1,
        replace_existing=True
    )


def check_time(mailout: Mailout):
    if now() < mailout.finish_time:
        if now() >= mailout.start_time:
            mailout.status = 'STARTED'
            mailout.save()

            log = Log.objects.create(server_response='-', status='Запущена', mailout=mailout)
            log.save()
            return True
        else:
            return False
    else:
        mailout.status = 'COMPLETE'
        mailout.save()

        log = Log.objects.create(server_response='-', status='Завершена', mailout=mailout)
        log.save()
        return False


def launch_scheduler(scheduler):
    scheduler = BackgroundScheduler()
    mailouts = Mailout.objects.filter(is_active=True)

    if mailouts:
        for mailout in mailouts:
            if mailout.status != 'COMPLETE':
                job_id = f'{mailout.pk}'
                if check_time(mailout):
                    if not scheduler.get_job(job_id):
                        create_task(scheduler, mailout)
                else:
                    if scheduler.get_job(job_id):
                        scheduler.pause_job(job_id)

        if scheduler.state == 0:
            scheduler.start()


# def send_message():
#     send_mail(
#         subject='Hey Dipper!',
#         message='Got message',
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=['nomoremaybe@yandex.ru'],
#         fail_silently=False
#     )
