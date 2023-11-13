from django.urls import path
from django.views.decorators.cache import cache_page

from mailout.apps import MailoutConfig
from mailout.views import IndexView, contact, ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    ClientDetailView, MessageListView, MessageCreateView, MessageDetailView, MessageUpdateView, MessageDeleteView, \
    MailoutListView, MailoutCreateView, MailoutDetailView, MailoutUpdateView, MailoutDeleteView, LogListView, \
    toggle_activity_mailout

app_name = MailoutConfig.name

urlpatterns = [
    path('', cache_page(60)(IndexView.as_view()), name='index'),
    path('contact/', contact, name='contact'),

    path('clients/', ClientListView.as_view(), name='client_list'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('client/view/<int:pk>', ClientDetailView.as_view(), name='client_view'),

    path('message/list/', MessageListView.as_view(), name='message_list'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/view/<int:pk>', MessageDetailView.as_view(), name='message_view'),
    path('message/update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),

    path('list/', MailoutListView.as_view(), name='list'),
    path('create/', MailoutCreateView.as_view(), name='create'),
    path('view/<int:pk>/', MailoutDetailView.as_view(), name='view'),
    path('update/<int:pk>/', MailoutUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', MailoutDeleteView.as_view(), name='delete'),

    path('logs/<int:pk>', LogListView.as_view(), name='log_list'),
    path('activity/<int:pk>', toggle_activity_mailout, name='toggle_activity_mailout'),

]

# urlpatterns = [
#     path('', cache_page(60)(IndexView.as_view()), name='index'),
# ]
