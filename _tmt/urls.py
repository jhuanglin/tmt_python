"""_tmt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.views.generic import TemplateView
from _project import views as tmt_views

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    path(r'api/login', tmt_views.login),
    path(r'api/register', tmt_views.register),
    path(r'api/logout', tmt_views.logout),
    path(r'api/addconfig', tmt_views.addConfig),
    path(r'api/config', tmt_views.config),
    path(r'api/list', tmt_views.getList),
    path(r'api/label', tmt_views.getLabel),
    path(r'api/list/add', tmt_views.addList),
    path(r'api/list/del', tmt_views.delList),
    path(r'api/list/complete', tmt_views.doneList),
    path(r'api/list/search_date', tmt_views.listSearchDate),
    path('admin/', admin.site.urls),
]
