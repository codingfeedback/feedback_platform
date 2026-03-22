from rest_framework import viewsets

from .models import FeedbackComment, Work
from .serializers import FeedbackCommentSerializer, WorkSerializer


class WorkViewSet(viewsets.ModelViewSet):
    serializer_class = WorkSerializer

    def get_queryset(self):
        queryset = Work.objects.select_related("creator").prefetch_related("assets")
        creator_id = self.request.query_params.get("creator_id")
        status_value = self.request.query_params.get("status")
        if creator_id:
            queryset = queryset.filter(creator_id=creator_id)
        if status_value:
            queryset = queryset.filter(status=status_value)
        return queryset


class FeedbackCommentViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackCommentSerializer

    def get_queryset(self):
        queryset = FeedbackComment.objects.select_related("author", "work", "parent")
        work_id = self.request.query_params.get("work_id")
        if work_id:
            queryset = queryset.filter(work_id=work_id)
        return queryset
