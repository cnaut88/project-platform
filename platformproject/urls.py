"""
URL configuration for platformproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from platformuser import views
from django.conf import settings
from django.conf.urls.static import static
from platformuser.views import auth_view, logout_view

urlpatterns = [
    path("", views.project_list, name="show_projects"),
    path("project/<int:project_id>/", views.project_details, name="project_details"),
    path("create/", views.create_project, name="create_project"),
    path("edit/<int:project_id>/", views.edit_project, name="edit_project"),
    path("delete/<int:project_id>/", views.delete_project, name="delete_project"),
    path("my/", views.my_projects, name="my_projects"),

    path("comment/<int:project_id>/", views.add_comment, name="add_comment"),
    path("like/<int:project_id>/", views.like_project, name="like_project"),
    path("user/<int:user_id>/", views.user_profile, name="user_profile"),
    path("subscribe_user/<int:user_id>/", views.subscribe_user, name="subscribe_user"),
    path("unsubscribe/<int:project_id>/", views.unsubscribe_project, name="unsubscribe_project"),
    path("login/", auth_view, name="login"),
    path("auth/", auth_view, name="auth"),
    path("logout/", logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

