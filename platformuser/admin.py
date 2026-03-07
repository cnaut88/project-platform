from django.contrib import admin
from .models import (User,Project,ProjectTag,ProjectCategory,ProjectComment,Subscription)
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_verified")
    search_fields = ("username", "email")

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "status", "created_a")
    list_filter = ("status",)
    search_fields = ("title",)
    filter_horizontal = ("tags",)

@admin.register(ProjectTag)
class ProjectTagAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(ProjectComment)
class ProjectCommentAdmin(admin.ModelAdmin):
    list_display = ("project", "author", "type", "created_at")
    list_filter = ("type",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("subscriber", "author")
