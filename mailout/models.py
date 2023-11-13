from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='Email')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    auth_user = models.ForeignKey(User, related_name='clients', on_delete=models.SET_NULL, **NULLABLE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    subject = models.CharField(max_length=150, verbose_name='Тема сообщения')
    body = models.TextField(verbose_name='Текст сообщения')

    auth_user = models.ForeignKey(User, related_name='messages', on_delete=models.SET_NULL, **NULLABLE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

        permissions = [
            ('view_all_messages', 'Can see all messages')
        ]


class Mailout(models.Model):

    FREQ_CHOICES = [
        ('DY', 'Раз в день'),
        ('WK', 'Раз в неделю'),
        ('MO', 'Раз в месяц'),
    ]
    STATUS_CHOICES = [
        ('CREATED', 'Создана'),
        ('STARTED', 'Запущена'),
        ('COMPLETE', 'Завершена')
    ]
    start_time = models.DateTimeField(verbose_name='Время рассылки')
    finish_time = models.DateTimeField(verbose_name='Время окончания рассылки')
    freq = models.CharField(max_length=2, choices=FREQ_CHOICES, verbose_name='Периодичность')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='CREATED', verbose_name='Статус рассылки')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    clients = models.ManyToManyField(Client, related_name='mailouts', verbose_name='Клиенты') # default='' or defailt=None
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='mailouts', verbose_name='Сообщение')

    auth_user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='mailouts', **NULLABLE, verbose_name='Пользователь')

    def __str__(self):
        return f'Рассылка {self.pk} {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

        permissions = [
            ('deactivate', 'Can deactivate mailouts'),
            ('view_all', 'Can see all mailouts')
        ]


class Log(models.Model):
    last_attempt = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')
    status = models.CharField(max_length=50, verbose_name='Статус попытки')
    server_response = models.CharField(max_length=250, **NULLABLE, verbose_name='Ответ почтового сервера')

    mailout = models.ForeignKey(Mailout, on_delete=models.CASCADE, related_name='logs', verbose_name='Рассылка')
    auth_user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='logs', **NULLABLE)

    def __str__(self):
        return f'Лог {self.pk} {self.last_attempt} ({self.status})'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
