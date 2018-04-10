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
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from _project import views as tmt_views

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    path(r'favicon.ico',RedirectView.as_view(url=r'static/img/favicon.ico')),
    path(r'api/login', tmt_views.login),
    path(r'api/register', tmt_views.register),
    path(r'api/logout', tmt_views.logout),
    path(r'api/user/confirmpass', tmt_views.confirmPass),
    path(r'api/user/changepass', tmt_views.updatePass),
    path(r'api/addconfig', tmt_views.addConfig),
    path(r'api/config', tmt_views.config),
    path(r'api/list', tmt_views.getList),
    path(r'api/label', tmt_views.getLabel),
    path(r'api/list/add', tmt_views.addList),
    path(r'api/list/del', tmt_views.delList),
    path(r'api/list/complete', tmt_views.doneList),
    path(r'api/list/search_date', tmt_views.listSearchDate),
    path(r'api/promo/add', tmt_views.addPromo),
    path(r'api/time/count', tmt_views.getCountMins),
    path(r'api/time/addcount', tmt_views.addCountMins),
    path(r'api/promo', tmt_views.getPromo),
    path(r'api/promo/del', tmt_views.delPromo),
    path(r'api/list/completelist', tmt_views.getCompleteList),
    path(r'api/list/changecompletelist', tmt_views.updateCompleteList),
    path(r'api/list/delcompleteist', tmt_views.delCompleteList),
    path(r'api/count/linechart', tmt_views.getLineChart),
    path(r'api/count/piechart', tmt_views.getPieChart),
    path(r'api/count/barchart', tmt_views.getBarChart),
    path(r'api/count/data', tmt_views.getCountData),
    path('admin/', admin.site.urls),
]

