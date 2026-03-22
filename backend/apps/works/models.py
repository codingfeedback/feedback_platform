from django.conf import settings
from django.db import models


class Work(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = "image", "Image"
        VIDEO = "video", "Video"
        AUDIO = "audio", "Audio"
        ILLUSTRATION = "illustration", "Illustration"
        OTHER = "other", "Other"

    class Visibility(models.TextChoices):
        PUBLIC = "public", "Public"
        UNLISTED = "unlisted", "Unlisted"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="works", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=280, blank=True)
    creator_intent = models.TextField()
    media_type = models.CharField(max_length=20, choices=MediaType.choices)
    visibility = models.CharField(max_length=16, choices=Visibility.choices, default=Visibility.PUBLIC)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.title


class WorkAsset(models.Model):
    work = models.ForeignKey(Work, related_name="assets", on_delete=models.CASCADE)
    asset_url = models.URLField()
    thumbnail_url = models.URLField(blank=True)
    mime_type = models.CharField(max_length=100, blank=True)
    duration_seconds = models.PositiveIntegerField(blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "id")

    def __str__(self) -> str:
        return f"{self.work_id}:{self.sort_order}"


class FeedbackComment(models.Model):
    class FocusArea(models.TextChoices):
        OVERALL = "overall", "Overall"
        STORY = "story", "Story"
        VISUAL = "visual", "Visual"
        SOUND = "sound", "Sound"
        EDITING = "editing", "Editing"
        EMOTION = "emotion", "Emotion"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        HIDDEN = "hidden", "Hidden"
        DELETED = "deleted", "Deleted"

    work = models.ForeignKey(Work, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="feedback_comments", on_delete=models.CASCADE)
    parent = models.ForeignKey("self", related_name="replies", on_delete=models.CASCADE, blank=True, null=True)
    body = models.TextField()
    focus_area = models.CharField(max_length=16, choices=FocusArea.choices, default=FocusArea.OVERALL)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self) -> str:
        return f"{self.author} -> {self.work}"
