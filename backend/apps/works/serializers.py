from django.db import transaction
from rest_framework import serializers

from apps.accounts.models import User
from apps.accounts.serializers import PublicUserSerializer

from .models import FeedbackComment, Work, WorkAsset


class WorkAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkAsset
        fields = ("id", "asset_url", "thumbnail_url", "mime_type", "duration_seconds", "sort_order")


class WorkSerializer(serializers.ModelSerializer):
    creator = PublicUserSerializer(read_only=True)
    creator_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source="creator", write_only=True)
    assets = WorkAssetSerializer(many=True)

    class Meta:
        model = Work
        fields = (
            "id",
            "creator",
            "creator_id",
            "title",
            "summary",
            "creator_intent",
            "media_type",
            "visibility",
            "status",
            "published_at",
            "assets",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    @transaction.atomic
    def create(self, validated_data):
        assets_data = validated_data.pop("assets", [])
        work = Work.objects.create(**validated_data)
        for asset_data in assets_data:
            WorkAsset.objects.create(work=work, **asset_data)
        return work

    @transaction.atomic
    def update(self, instance, validated_data):
        assets_data = validated_data.pop("assets", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if assets_data is not None:
            instance.assets.all().delete()
            for asset_data in assets_data:
                WorkAsset.objects.create(work=instance, **asset_data)

        return instance


class FeedbackCommentSerializer(serializers.ModelSerializer):
    author = PublicUserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source="author", write_only=True)
    work_id = serializers.PrimaryKeyRelatedField(queryset=Work.objects.all(), source="work", write_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=FeedbackComment.objects.all(),
        source="parent",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = FeedbackComment
        fields = (
            "id",
            "work",
            "work_id",
            "author",
            "author_id",
            "parent",
            "parent_id",
            "body",
            "focus_area",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("work", "author", "parent", "created_at", "updated_at")

    def validate(self, attrs):
        parent = attrs.get("parent")
        work = attrs.get("work")
        if parent and work and parent.work_id != work.id:
            raise serializers.ValidationError("Replies must belong to the same work.")
        return attrs
