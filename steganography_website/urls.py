from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name = "home"),
    path('about', views.about, name = "about"),
    path('processcompleted', views.processcompleted, name = "processcompleted"),
    path('secret_text_download', views.secret_text_download, name = "secret_text_download"),
]


urlpatterns += staticfiles_urlpatterns()
