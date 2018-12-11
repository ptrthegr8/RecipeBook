"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path
from mysite.views import *
from mysite.models import Author, Recipe
from django.contrib.auth.views import LogoutView
from mysite.settings import LOGOUT_REDIRECT_URL

admin.site.register(Author)
admin.site.register(Recipe)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', recipe_views, name='homepage'),
    path('authors/<int:id>/', author_views),
    path('recipes/<int:id>/', individual_views),
    # path('add_author/', get_author),
    path('add_recipe/', get_recipe),
    path('signup/', signup_view),
    path('login/', login_view),
    path('logout/', logout_view, name='logout')
]
