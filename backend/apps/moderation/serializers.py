from rest_framework import serializers

from apps.accounts.models import User
from apps.works.models import FeedbackComment, Work

from .models import ContentReport, ModerationAction


class ContentReportSerializer(serializers.ModelSerializer):
    reporter_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source="reporter")
    work_id = serializers.PrimaryKeyRelatedField(
        queryset=Work.objects.all(),
        source="work",
        required=False,
        allow_null=True,
    )
    comment_id = serializers.PrimaryKeyRelatedField(
        queryset=FeedbackComment.objects.all(),
        source="comment",
        required=False,
        allow_null=True,
    )
    reported_user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="reported_user",
        required=False,
        allow_null=True,
    )

    class Meta:
        model = ContentReport
        fields = (
            "id",
            "reporter_id",
            "work_id",
            "comment_id",
            "reported_user_id",
            "reason",
            "description",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    def validate(self, attrs):
        targets = [attrs.get("work"), attrs.get("comment"), attrs.get("reported_user")]
        if sum(target is not None for target in targets) != 1:
            raise serializers.ValidationError("Exactly one report target must be selected.")
        return attrs


class ModerationActionSerializer(serializers.ModelSerializer):
    moderator_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source="moderator")

    class Meta:
        model = ModerationAction
        fields = ("id", "report", "moderator_id", "action_type", "note", "created_at")
        read_only_fields = ("created_at",)
