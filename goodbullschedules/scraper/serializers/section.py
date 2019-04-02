from rest_framework import serializers
from scraper import models


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Meeting
        fields = ("location", "meeting_days", "start_time", "end_time", "meeting_type")


class AggregateGradeField(serializers.DictField):
    child = serializers.FloatField()

    class Meta:
        validators = [lambda x: x in "ABCDFISUQX"]


class SectionSerializer(serializers.ModelSerializer):
    meetings = MeetingSerializer(many=True, read_only=True)
    historical_performance = AggregateGradeField(read_only=True, required=False)

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
            "historical_performance",
        )
