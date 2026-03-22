from django.contrib import admin

from .models import ContentReport, ModerationAction


@admin.register(ContentReport)
class ContentReportAdmin(admin.ModelAdmin):
    list_display = ("id", "reporter", "reason", "status", "created_at")
    list_filter = ("reason", "status")
    search_fields = ("description", "reporter__public_handle")


@admin.register(ModerationAction)
class ModerationActionAdmin(admin.ModelAdmin):
    list_display = ("id", "report", "action_type", "moderator", "created_at")
    list_filter = ("action_type",)
    search_fields = ("note",)
