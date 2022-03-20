from django.conf.urls import url
from .import views

urlpatterns = [

    url(r'^$', views.home, name='home'),                        ## Front Home Page
    url(r'^login/$', views.login, name='login'),            ## Front Login Page
    url(r'^register/$', views.register, name='register'),    ## Front Register Page
]   