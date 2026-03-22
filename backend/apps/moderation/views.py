from rest_framework import mixins, viewsets

from .models import ContentReport, ModerationAction
from .serializers import ContentReportSerializer, ModerationActionSerializer


class ContentReportViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = ContentReport.objects.select_related("reporter", "work", "comment", "reported_user")
    serializer_class = ContentReportSerializer


class ModerationActionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = ModerationAction.objects.select_related("report", "moderator")
    serializer_class = ModerationActionSerializer
