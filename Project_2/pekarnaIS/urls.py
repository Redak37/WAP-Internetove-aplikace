"""pekarnaIS URL Configuration

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
from django.conf.urls import include
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('pekarnaApp.urls')),
    path('', serve, kwargs={'document_root': 'vueapp/dist/', 'path': 'index.html'}),
    path('favicon.ico', serve, kwargs={'document_root': 'vueapp/dist/', 'path': 'favicon.ico'}),
    path('css/<path:path>', serve, kwargs={'document_root': 'vueapp/dist/css'}),
    path('js/<path:path>', serve, kwargs={'document_root': 'vueapp/dist/js'}),
    path('img/<path:path>', serve, kwargs={'document_root': 'vueapp/dist/img'}),
]