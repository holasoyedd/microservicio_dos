from django.contrib import admin
from django.urls import path, re_path
from microserviciodos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^users/$', views.users),
    re_path(r'^users/(?P<username>.*)/(?P<password>.*)/$', views.users),
]
