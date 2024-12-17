from django.urls import path

from . import views

# app_name = 'core'

urlpatterns = [
    path('',views.home_page,name='home'),
    path('save/<slug:slug>/',views.save_post_view,name='save'),
    path('likes/<slug:slug>/',views.likes_view,name='like'),
    path('comment/<slug:slug>/',views.comments_view,name='comment'),
    path('follow/<int:pk>/',views.follow_view,name='follow'),
    path('unfollow/<int:pk>/',views.unfollow_view,name='unfollow'),
    path('register/',views.register_view,name='signup'),
    path('logout/',views.logout_view,name='logout'),
    path('login/',views.login_view,name='login'),
    path('forgot-password/',views.forgot_password_view,name='forgot-password'),
    path('profile/',views.profile_view,name='profile'),
    path('create/',views.create_view,name='create'),
    path('search/',views.search_view,name='search'),
    path('reset-password/<str:reset_id>/',views.reset_password_view,name="reset-password"),
]