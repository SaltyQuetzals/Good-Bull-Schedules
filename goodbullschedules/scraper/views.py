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

        sections_data = serializers.SectionSerializer(sections_obj, many=True).data

        instructors = {}
        for section in sections_data:
            instructor = section["instructor"]
            if instructor not in instructors:
                instructors[instructor] = models.Grades.objects.professor_performance(
                    section["dept"], section["course_num"], instructor
                )
            section["instructor_performance"] = instructors[instructor]

        course_data["sections"] = sections_data

        return response.Response(course_data)


class SectionRetrieveView(generics.RetrieveAPIView):
    queryset = models.Section.objects.all()
    serializer_class = serializers.SectionSerializer
    renderer_classes = [renderers.JSONRenderer]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        lookup = {
            "dept": self.kwargs["dept"],
            "course_num": self.kwargs["course_num"],
            "section_num": self.kwargs["section_num"],
            "term_code": self.kwargs["term_code"],
        }
        obj = shortcuts.get_object_or_404(queryset, **lookup)
        serialized_obj = serializers.SectionSerializer(obj).data
        serialized_obj[
            "instructor_performance"
        ] = models.Grades.objects.professor_performance(
            obj.dept, obj.course_num, obj.instructor
        )
        return response.Response(serialized_obj)

    def get_object(self):
        queryset = self.get_queryset()
        lookup = {
            "dept": self.kwargs["dept"],
            "course_num": self.kwargs["course_num"],
            "section_num": self.kwargs["section_num"],
            "term_code": self.kwargs["term_code"],
        }
        obj = shortcuts.get_object_or_404(queryset, **lookup)
        obj.instructor_performance = models.Grades.objects.professor_performance(
            obj.dept, obj.course_num, obj.instructor
        )
        return obj

