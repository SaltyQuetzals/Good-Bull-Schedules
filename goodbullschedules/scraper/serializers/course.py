from rest_framework import serializers
from scraper import models as scraper_models


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = scraper_models.Course
        fields = (
            "dept",
            "course_num",
            "name",
            "description",
            "prerequisites",
            "corequisites",
            "min_credits",
            "max_credits",
            "distribution_of_hours",
        )


class CourseSearchSerializer(serializers.Serializer):
    name = serializers.CharField()
    dept = serializers.CharField()
    course_num = serializers.CharField()
    description = serializers.CharField()
    search = serializers.CharField(required=False)
