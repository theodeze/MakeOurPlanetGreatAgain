"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from apps.venture.views import home, create_venture, show_venture, show_ventures, pledge
from apps.venture.feeds import RssVenturesFeed
from apps.authentication.views import signup, profile

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('ventures/create', create_venture),
    path('ventures', show_ventures),
    path('ventures/rss/', RssVenturesFeed()),
    path('ventures/<int:id>', show_venture),
    path('ventures/<int:id>/pledge', pledge),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', signup),
    path('accounts/profile/', profile)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
