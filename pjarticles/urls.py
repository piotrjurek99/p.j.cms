from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'pjarticles'

urlpatterns = [
    path('main/', views.main_view),
    path('login/', views.login),
    path('logout/', views.logout_view),
    path('article/<int:a_id>/', views.article_view),
    path('article_edit/<int:a_id>/', views.article_edit),
    path('article_del/<int:a_id>/', views.article_del, name='article_del'),
    path('article_pub/<int:article_id>/', views.article_pub, name='article_pub'),
    path('article_accept/', views.article_acc),
    path('add_article/', views.add_article),
    path('add_comment/<int:article_id>/', views.add_comment),
    path('contact/', views.contact),
]
