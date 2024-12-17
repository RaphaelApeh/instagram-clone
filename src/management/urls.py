from django.urls import path

from . import views

app_name = 'management'

urlpatterns = [
    path('<username>/',views.users_profile_view,name="profiles")
]