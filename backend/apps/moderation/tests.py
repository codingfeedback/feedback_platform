from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.accounts.models import User
from apps.works.models import Work

from .models import ContentReport


class ContentReportTests(TestCase):
    def test_report_requires_one_target(self):
        reporter = User.objects.create_user(username="reporter", password="testpass1234")
        creator = User.objects.create_user(username="creator", password="testpass1234")
        work = Work.objects.create(
            creator=creator,
            title="Poster",
            creator_intent="I want feedback on readability.",
            media_type=Work.MediaType.IMAGE,
        )

        report = ContentReport(reporter=reporter, work=work, reason=ContentReport.Reason.SPAM)
        report.full_clean()

        invalid_report = ContentReport(
            reporter=reporter,
            work=work,
            reported_user=creator,
            reason=ContentReport.Reason.OTHER,
        )

        with self.assertRaises(ValidationError):
            invalid_report.full_clean()
