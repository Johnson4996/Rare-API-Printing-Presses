"""rare URL Configuration

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

from rareapi.views.deactivate import deactivate
from rareapi.views.makeadmin import MakeAdmin
from rareapi.views.profiles import Profile
from django.conf.urls import include
from django.urls import path
from rareapi.views import register_user, login_user, Tags
from rest_framework import routers
from rareapi.views import Categories, Post, PostTags, Comments, Subs

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', Categories, 'category')
router.register(r'posts', Post, 'posts')
router.register(r'posttags', PostTags, 'postTags')
router.register(r'tags', Tags, 'tag')
router.register(r'comments', Comments, 'comments')
router.register(r'profile', Profile, 'profile')
router.register(r'subscriptions', Subs, 'subscription')
router.register(r'deactivate', deactivate, 'activatedProfile')
router.register(r'makeadmin', MakeAdmin, 'activatedProfile')


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
