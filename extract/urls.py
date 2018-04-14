from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import include

app_name = 'extract'
urlpatterns = [
    #path('example/', views.example, name='example'),
    #path('', views.IndexView.as_view(), name='index'),
    #path('change-password/', auth_views.PasswordChangeView.as_view()),
    
    #path('accounts/', include('django.contrib.auth.urls')),
    #path('accounts/login/', auth_views.LoginView.as_view()),
    #path('accounts/login/', auth_views.LoginView.as_view()),

    #path('login/', auth_views.LoginView.as_view()),
    # url(r'^login/',
    #     auth_views.LoginView.as_view(redirect_authenticated_user=False),
    #     name='login'),
    path('', views.index, name='detail'),

    # accounts/login/ [name='login']
    # accounts/logout/ [name='logout']

    #path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    #path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    #path('<int:question_id>/vote/', views.vote, name='vote'),
    path('vote/', views.vote, name='vote'),
]

# urlpatterns += [
#     path('accounts/', include('django.contrib.auth.urls')),
# ]