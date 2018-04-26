from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import include
from .views import KeywordView, TrendView

app_name = 'extract'
urlpatterns = [
    path('', views.index, name='detail'),
    path('abstract_view', views.abstract, name='abstract'),
    path('vote/', KeywordView.as_view()),
    path('trend/', TrendView.as_view()),
    path('abstract/', AbstractView.as_view()),
]
