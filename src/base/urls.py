from django.urls import path

from . import views

app_name = 'base'

urlpatterns = [
    path('',views.inbox_view,name='inbox'),
    path('<int:pk>/',views.messages_view,name='messages'),
]