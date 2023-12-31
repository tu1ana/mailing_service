# Generated by Django 4.2.7 on 2023-11-10 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('first_name', models.CharField(max_length=100, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('auth_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clients', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=150, verbose_name='Тема сообщения')),
                ('body', models.TextField(verbose_name='Текст сообщения')),
                ('auth_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='Mailout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='Время рассылки')),
                ('finish_time', models.DateTimeField(verbose_name='Время окончания рассылки')),
                ('freq', models.CharField(choices=[('DY', 'Раз в день'), ('WK', 'Раз в неделю'), ('MO', 'Раз в месяц')], max_length=2, verbose_name='Периодичность')),
                ('status', models.CharField(choices=[('CREATED', 'Создана'), ('STARTED', 'Запущена'), ('COMPLETE', 'Завершена')], default='CREATED', max_length=8, verbose_name='Статус рассылки')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активна')),
                ('auth_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mailouts', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('clients', models.ManyToManyField(related_name='mailouts', to='mailout.client', verbose_name='Клиенты')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mailouts', to='mailout.message', verbose_name='Сообщение')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_attempt', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')),
                ('status', models.CharField(max_length=50, verbose_name='Статус попытки')),
                ('server_response', models.CharField(blank=True, max_length=250, null=True, verbose_name='Ответ почтового сервера')),
                ('auth_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='logs', to=settings.AUTH_USER_MODEL)),
                ('mailout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='mailout.mailout', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'Лог',
                'verbose_name_plural': 'Логи',
            },
        ),
    ]
