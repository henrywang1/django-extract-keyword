from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()
from django.contrib.auth import views as auth_views
# import hello.views
# from extract.views import custom_login 

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    path('', include('extract.urls')),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
 
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/login/', custom_login, name='login'),
    #path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    # url(r'^$', hello.views.index, name='index'),
    # url(r'^db', hello.views.db, name='db'),
    # path('admin/', admin.site.urls),
    # path('extract/', include('polls.urls')),

]

#Add Django site authentication urls (for login, logout, password management)


