from rest_framework import viewsets

from .models import FeedbackComment, Work
from .serializers import FeedbackCommentSerializer, WorkSerializer


class WorkViewSet(viewsets.ModelViewSet):
    serializer_class = WorkSerializer

    def get_queryset(self):
        queryset = Work.objects.select_related("creator").prefetch_related("assets")
        creator_id = self.request.query_params.get("creator_id")
        exclude_creator_id = self.request.query_params.get("exclude_creator_id")
        media_type = self.request.query_params.get("media_type")
        status_value = self.request.query_params.get("status")
        visibility = self.request.query_params.get("visibility")
        if creator_id:
            queryset = queryset.filter(creator_id=creator_id)
        if exclude_creator_id:
            queryset = queryset.exclude(creator_id=exclude_creator_id)
        if media_type:
            queryset = queryset.filter(media_type=media_type)
        if status_value:
            queryset = queryset.filter(status=status_value)
        if visibility:
            queryset = queryset.filter(visibility=visibility)
        return queryset


class FeedbackCommentViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackCommentSerializer

    def get_queryset(self):
        queryset = FeedbackComment.objects.select_related("author", "work", "parent")
        work_id = self.request.query_params.get("work_id")
        author_id = self.request.query_params.get("author_id")
        status_value = self.request.query_params.get("status")
        if work_id:
            queryset = queryset.filter(work_id=work_id)
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        if status_value:
            queryset = queryset.filter(status=status_value)
        return queryset
