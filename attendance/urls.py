from django.conf.urls import url,include
from django.contrib import admin
import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^ajax/',views.ajax),
    url(r'^$',views.attendanceHome),
]
