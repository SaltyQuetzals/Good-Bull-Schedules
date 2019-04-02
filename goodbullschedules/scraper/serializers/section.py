from rest_framework import serializers
from scraper import models


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Meeting
        fields = ("location", "meeting_days", "start_time", "end_time", "meeting_type")


class SectionSerializer(serializers.ModelSerializer):
    meetings = MeetingSerializer(many=True, read_only=True)

    class Meta:
        model = models.Section
        fields = (
            "name",
            "term_code",
            "crn",
            "dept",
            "course_num",
            "section_num",
            "min_credits",
            "max_credits",
            "instructor",
            "meetings",
        )
