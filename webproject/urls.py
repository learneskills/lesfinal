"""webproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from myproject.views import CategoryListView
from webproject import settings


urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^search/', include('haystack.urls'), name='search'),
    url(r'^course/', include('myproject.urls_categories')),
    url(r'^books/', include('books.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^accounts/', include('registration.urls')),
    url(r'^newsletter/', include('newsletter.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^djrichtextfield/', include('djrichtextfield.urls')),
    url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
    url(r'^$', CategoryListView.as_view(), name='index'),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
