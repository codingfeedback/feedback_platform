from rest_framework.routers import DefaultRouter

from apps.accounts.views import UserViewSet
from apps.moderation.views import ContentReportViewSet, ModerationActionViewSet
from apps.works.views import FeedbackCommentViewSet, WorkViewSet


router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("works", WorkViewSet, basename="work")
router.register("comments", FeedbackCommentViewSet, basename="comment")
router.register("reports", ContentReportViewSet, basename="report")
router.register("moderation-actions", ModerationActionViewSet, basename="moderation-action")
