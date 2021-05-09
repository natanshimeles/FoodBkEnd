"""foodDeliverBkEnd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.generic.base import TemplateView
from .router import router


BASE_URL = 'api/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(BASE_URL, include('UserManagement.urls')),
    path(BASE_URL, include('Order.urls')),   
    path(BASE_URL, include(router.urls)),
]



urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns.append(url(r'^celavieadmin/.*', TemplateView.as_view(template_name="admin.html"), name="admin_site"))
urlpatterns.append(url(r'^.*', TemplateView.as_view(template_name="index.html"), name="home"))
