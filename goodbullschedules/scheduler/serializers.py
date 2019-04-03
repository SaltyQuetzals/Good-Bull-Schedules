from scraper import serializers as scraper_serializers
from rest_framework import serializers as rf_serializers
from scheduler import models as scheduler_models
from scraper import models as scraper_models


class ScheduleSerializer(rf_serializers.ModelSerializer):
    courses = scraper_serializers.CourseSerializer(many=True, allow_null=True)
    sections = rf_serializers.PrimaryKeyRelatedField(
        queryset=scraper_models.Section.objects.all(), many=True
    )
    name = rf_serializers.CharField()
    term_code = rf_serializers.IntegerField()

    def create(self, validated_data):
        schedule = scheduler_models.Schedule(**validated_data)
        schedule.courses.set()
        schedule.sections.set()
        return schedule

    class Meta:
        fields = ("courses", "sections", "name", "term_code")
        model = scheduler_models.Schedule
