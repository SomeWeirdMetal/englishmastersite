"""DjangoProject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
     path('admin/', admin.site.urls),
     path('', views.index, name='index'),
     path('feedback/', views.feedback, name='feedback'),
     path('grammar/', views.grammar, name='grammar'),
     path('vocabulary/', views.wordlist, name='vocabulary'),
     path('add-word/', views.add_word, name='add_word'),
     path('send-word/', views.send_word, name='send_word'),
     path('show-stats/', views.show_stats, name='show_stats'),
]
