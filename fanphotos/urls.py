"""fanphotos URL Configuration

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
from django.urls import path
from back import views
from django.views.static import serve
from django.conf import settings
from django.conf.urls import url
import os
from back.mystatic import serve as myserve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    # media相关的路由配置
    url(r'^photo/(?P<path>.*)$', serve, {"document_root": settings.PHOTO_ROOT}),
    path('photo_preview/<str:album>/<str:path>', myserve,
         {"document_root": os.path.join(settings.PHOTO_ROOT, settings.CACHE_FILE_NAME)}),
    path('album/<album_name>/', views.album, ),
    path('album/<album_name>/<page>/', views.album, ),
    path('flash_cache/', views.flash_cache, ),
    path('create_album/', views.CreatePhotoAlbum, ),
]
