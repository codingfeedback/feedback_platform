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

    def test_public_feed_filters_multiple_user_works(self):
        creator = User.objects.create_user(username="creator", password="testpass1234")
        reviewer = User.objects.create_user(username="reviewer", password="testpass1234")
        Work.objects.create(
            creator=creator,
            title="Published Film",
            creator_intent="Check if the story lands.",
            media_type=Work.MediaType.VIDEO,
            visibility=Work.Visibility.PUBLIC,
            status=Work.Status.PUBLISHED,
        )
        Work.objects.create(
            creator=reviewer,
            title="Draft Poster",
            creator_intent="Check readability.",
            media_type=Work.MediaType.IMAGE,
            visibility=Work.Visibility.PUBLIC,
            status=Work.Status.DRAFT,
        )

        response = self.client.get("/api/works/?visibility=public&status=published&exclude_creator_id=%s" % reviewer.id)

        self.assertEqual(response.status_code, 200)
        titles = [item["title"] for item in response.json()["results"]]
        self.assertEqual(titles, ["Published Film"])

    def test_comments_can_be_filtered_by_author(self):
        creator = User.objects.create_user(username="creator-2", password="testpass1234")
        reviewer = User.objects.create_user(username="reviewer-2", password="testpass1234")
        other = User.objects.create_user(username="other", password="testpass1234")
        work = Work.objects.create(
            creator=creator,
            title="Poster",
            creator_intent="Check hierarchy.",
            media_type=Work.MediaType.IMAGE,
            status=Work.Status.PUBLISHED,
        )
        FeedbackComment.objects.create(work=work, author=reviewer, body="Clear hierarchy.")
        FeedbackComment.objects.create(work=work, author=other, body="Needs more contrast.")

        response = self.client.get("/api/comments/?author_id=%s&status=active" % reviewer.id)

        self.assertEqual(response.status_code, 200)
        comments = response.json()["results"]
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0]["author"]["id"], reviewer.id)
