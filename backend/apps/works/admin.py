from django.contrib import admin

from .models import FeedbackComment, Work, WorkAsset


class WorkAssetInline(admin.TabularInline):
    model = WorkAsset
    extra = 0


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "creator", "media_type", "status", "visibility", "created_at")
    list_filter = ("media_type", "status", "visibility")
    search_fields = ("title", "creator__public_handle", "creator__username")
    inlines = [WorkAssetInline]


@admin.register(FeedbackComment)
class FeedbackCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "work", "author", "focus_area", "status", "created_at")
    list_filter = ("focus_area", "status")
    search_fields = ("body", "author__public_handle", "work__title")
