from django.test import TestCase

from apps.accounts.models import User

from .models import FeedbackComment, Work


class FeedbackCommentTests(TestCase):
    def test_comment_can_be_created(self):
        creator = User.objects.create_user(username="creator", password="testpass1234")
        reviewer = User.objects.create_user(username="reviewer", password="testpass1234")
        work = Work.objects.create(
            creator=creator,
            title="Short Film",
            summary="A quiet scene",
            creator_intent="I want the scene to feel tense.",
            media_type=Work.MediaType.VIDEO,
            status=Work.Status.PUBLISHED,
        )

        comment = FeedbackComment.objects.create(
            work=work,
            author=reviewer,
            body="The tension builds well, but the ending feels abrupt.",
        )

        self.assertEqual(comment.work, work)
