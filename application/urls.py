"""application URL Configuration

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
from django.urls import path
from django.conf.urls import url, include
from Politricks import views
from Politricks.views import UserEdit, UserList


def trigger_error(request):
    division_by_zero = 1 / 0


handler404 = 'Politricks.views.my_custom_page_not_found_view'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>/post/', views.postdetail, name='post-detail'),
    path(r'post/edit/<int:post_id>/', views.postedit, {}, 'post_edit'),
    path('add/post/', views.postupdate, name='post-update'),
    path('users/', UserList.as_view(), name='user-list'),
    path('profile/edit/', UserEdit.as_view(), name='user_edit'),
    path('<int:user_id>/user/', views.userprofile, name='user-profile'),
    path('<int:party_id>/party/', views.partydetail, name='party-detail'),
    path('admin/', admin.site.urls),
    path(r'login/', views.user_login, name='user_login'),
    path("register/", views.register, name="register"),
    path('accounts/', include('django.contrib.auth.urls')),
    path(r'change-password/', views.change_password, name='change_password'),
    path('sentry-debug/', trigger_error),
    path('s3direct/', include('s3direct.urls')),
]
