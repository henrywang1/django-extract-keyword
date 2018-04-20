from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
admin.autodiscover()
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('extract.urls')),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('admin/', admin.site.urls),
]