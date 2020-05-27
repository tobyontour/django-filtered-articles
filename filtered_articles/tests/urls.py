from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('articles/', include('filtered_articles.urls'))
]