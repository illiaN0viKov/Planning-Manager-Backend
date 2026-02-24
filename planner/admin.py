from django.contrib import admin
from .models import Project, Place


class PlaceInline(admin.TabularInline):
    model = Place
    extra = 0
    fields = ("id", "title", "is_visited")
    readonly_fields = ("id", "title")
    show_change_link = True


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_completed", "start_date", "created_at")
    list_filter = ("is_completed",)
    search_fields = ("name",)
    inlines = [PlaceInline]


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "external_id",
        "project",
        "is_visited",
    )
    list_filter = ("is_visited", "project")
    search_fields = ("title", "external_id")