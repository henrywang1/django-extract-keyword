from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import include
from .views import KeywordView

app_name = 'extract'
urlpatterns = [
    path('', views.index, name='detail'),
    path('vote/', KeywordView.as_view()),
]