from django import shortcuts
from rest_framework import renderers
from rest_framework import request as rf_request
from rest_framework import response, views, generics

from scraper import models, serializers


# Create your views here.
class CourseRetrieveView(views.APIView):
    """
    View to retrieve a specific course and its sections, given a department, course number, and term code.
    """

    renderer_classes = [renderers.JSONRenderer]

    def get(self, request, *args, **kwargs):
        """
        Return the course and its associated sections.
        """
        dept, course_num, term_code = (
            kwargs["dept"],
            kwargs["course_num"],
            kwargs["term_code"],
        )
        course_obj = shortcuts.get_object_or_404(
            models.Course, dept=dept, course_num=course_num
        )
        course_data = serializers.CourseSerializer(course_obj).data

        sections_obj = models.Section.objects.filter(
            dept=dept, course_num=course_num, term_code=term_code
        ).all()

        instructors = {}
        for section in sections_obj:
            if not section.instructor in instructors:
                historical_performance = models.Grades.objects.instructor_performance(
                    dept, course_num, section.instructor
                )
                instructors[section.instructor] = historical_performance
            section.historical_performance = instructors[section.instructor]

        serialized_sections = serializers.SectionSerializer(
            sections_obj, many=True
        ).data
        course_data["sections"] = serialized_sections
        return response.Response(course_data)


class SectionRetrieveView(generics.RetrieveAPIView):
    queryset = models.Section.objects.all()
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = serializers.SectionSerializer

    def get_object(self):
        return self.get_queryset().get(**self.kwargs)
