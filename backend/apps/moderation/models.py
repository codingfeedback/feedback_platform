from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.works.models import FeedbackComment, Work


class ContentReport(models.Model):
    class Reason(models.TextChoices):
        ABUSE = "abuse", "Abuse"
        SPAM = "spam", "Spam"
        HATE = "hate", "Hate"
        COPYRIGHT = "copyright", "Copyright"
        ADULT = "adult", "Adult"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        REVIEWING = "reviewing", "Reviewing"
        RESOLVED = "resolved", "Resolved"
        REJECTED = "rejected", "Rejected"

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="submitted_reports", on_delete=models.CASCADE)
    work = models.ForeignKey(Work, related_name="reports", on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(FeedbackComment, related_name="reports", on_delete=models.CASCADE, blank=True, null=True)
    reported_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_reports",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    reason = models.CharField(max_length=16, choices=Reason.choices)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def clean(self):
        targets = [self.work_id, self.comment_id, self.reported_user_id]
        if sum(target is not None for target in targets) != 1:
            raise ValidationError("Exactly one report target must be selected.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.reason}:{self.id}"


class ModerationAction(models.Model):
    class ActionType(models.TextChoices):
        WARN = "warn", "Warn"
        HIDE = "hide", "Hide"
        DELETE = "delete", "Delete"
        SUSPEND = "suspend", "Suspend"
        RESTORE = "restore", "Restore"

    report = models.ForeignKey(ContentReport, related_name="actions", on_delete=models.CASCADE, blank=True, null=True)
    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="moderation_actions", on_delete=models.CASCADE)
    action_type = models.CharField(max_length=16, choices=ActionType.choices)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.action_type}:{self.id}"
