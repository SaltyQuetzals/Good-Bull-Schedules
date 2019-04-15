from django import shortcuts
from django.core.cache import cache
from rest_framework import generics, renderers
from rest_framework import request as rf_request
from rest_framework import response, views
from elasticsearch_dsl import Q

from scraper import models, serializers, documents

# Create your views here.


class CourseSearchView(generics.ListAPIView):
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = serializers.CourseSearchSerializer

    def get_queryset(self, *args, **kwargs):
        q = self.request.query_params.get("q")
        if q is not None:
            return (
                documents.CourseDocument.search().query("match", search=q).to_queryset()
            )

        return models.Course.objects.none()


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
        cached_result = cache.get(f"/{dept}/{course_num}/{term_code}")
        if cached_result:
            return response.Response(cached_result)

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
        cache.set(f"{dept}/{course_num}/{term_code}", course_data)
        return response.Response(course_data)


class SectionRetrieveView(generics.RetrieveAPIView):
    queryset = models.Section.objects.all()
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = serializers.SectionSerializer

    def get_object(self):
        return self.get_queryset().get(**self.kwargs)


class TermListView(views.APIView):
    def get(self, request, *args, **kwargs):
        term_codes = models.Section.objects.values_list(
            "term_code", flat=True
        ).distinct()
        return response.Response(data=term_codes)
