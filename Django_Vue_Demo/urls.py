"""Django_Vue_Demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url, include
from django.views.generic import TemplateView
from myapp.views import SearchSuggest, IndexView,SearchView,SearchFromDBView

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^api/', include(myapp.urls)),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^test/$', IndexView.as_view(), name="test"),
    url(r'^suggest$', SearchSuggest.as_view(), name="suggest"),

    url(r'^search$', SearchView.as_view(), name="search"),
    url(r'^searchTop$', SearchFromDBView.as_view(), name="searchTop")
]
