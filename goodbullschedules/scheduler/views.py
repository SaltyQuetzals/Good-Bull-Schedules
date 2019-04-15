from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, response, views, renderers

from scheduler import models as scheduler_models
from scheduler import serializers as scheduler_serializers
from scraper import models as scraper_models
from scraper import serializers as scraper_serializers

# Create your views here.


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class ListCreateSchedulesView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = scheduler_serializers.ScheduleSerializer
    renderer_classes = [renderers.JSONRenderer]

    def get_queryset(self):
        return scheduler_models.Schedule.objects.filter(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        schedules = {}
        for schedule in self.get_queryset().all():
            course_serializer = scraper_serializers.CourseSerializer(
                schedule.courses.all(), many=True
            )
            course_data = course_serializer.data
            courses = {}
            for course in course_data:
                filter = {
                    "dept": course["dept"],
                    "course_num": course["course_num"],
                    "term_code": schedule.term_code,
                }
                sections_obj = scraper_models.Section.objects.filter(**filter).all()
                instructors = {}
                for section in sections_obj:
                    if not section.instructor in instructors:
                        performance = section.historical_instructor_performance()
                        instructors[section.instructor] = performance
                    section.historical_performance = instructors[section.instructor]
                serialized_sections = scraper_serializers.SectionSerializer(
                    sections_obj, many=True
                ).data
                course["sections"] = serialized_sections
                courses[course["dept"] + "-" + course["course_num"]] = dict(**course)
            schedule_json = {
                "term_code": schedule.term_code,
                "courses": courses,
                "sections": schedule.sections.values_list("pk", flat=True),
                "id": schedule.id,
            }
            schedules[schedule.name] = schedule_json
        return response.Response(data=schedules)

    def create(self, request, *args, **kwargs):
        data = {
            "name": request.data["name"],
            "term_code": int(request.data["term_code"]),
            "owner": request.user,
        }
        schedule = scheduler_models.Schedule(**data)
        schedule.full_clean()
        schedule.save()

        serializer = self.get_serializer(schedule)
        return response.Response(serializer.data)


class RetrieveDestroyScheduleView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsOwner, permissions.IsAuthenticated)
    queryset = scheduler_models.Schedule.objects.all()
    serializer_class = scheduler_serializers.ScheduleSerializer
    renderer_classes = [renderers.JSONRenderer]

    def retrieve(self, request, *args, **kwargs):
        schedule = self.get_object()
        course_serializer = scraper_serializers.CourseSerializer(
            schedule.courses.all(), many=True
        )
        course_data = course_serializer.data
        courses = {}
        for course in course_data:
            filter = {
                "dept": course["dept"],
                "course_num": course["course_num"],
                "term_code": schedule.term_code,
            }
            sections_obj = scraper_models.Section.objects.filter(**filter).all()
            instructors = {}
            for section in sections_obj:
                if not section.instructor in instructors:
                    performance = section.historical_instructor_performance()
                    instructors[section.instructor] = performance
                section.historical_performance = instructors[section.instructor]
            serialized_sections = scraper_serializers.SectionSerializer(
                sections_obj, many=True
            ).data
            course["sections"] = serialized_sections
            courses[course["dept"] + "-" + course["course_num"]] = dict(**course)
        data = {
            "term_code": schedule.term_code,
            "courses": courses,
            "sections": schedule.sections.values_list("pk", flat=True),
            "id": schedule.id,
        }
        return response.Response(data=data)


class AddSectionScheduleView(generics.UpdateAPIView):
    permission_classes = (IsOwner, permissions.IsAuthenticated)
    queryset = scheduler_models.Schedule.objects.all()
    serializer_class = scheduler_serializers.ScheduleSerializer
    renderer_classes = [renderers.JSONRenderer]

    def partial_update(self, request, *args, **kwargs):
        schedule = self.get_object()

        section = scraper_models.Section.objects.get(pk=request.data["section_id"])
        if section.term_code != schedule.term_code:
            return response.Response(
                data={
                    "msg": "The section must belong to the same term as the schedule."
                },
                status=422,
            )
        course = scraper_models.Course.objects.get(
            dept=section.dept, course_num=section.course_num
        )
        schedule.sections.add(section)
        schedule.courses.add(course)
        return response.Response(status=200)


class DeleteSectionScheduleView(generics.DestroyAPIView):
    permission_classes = (IsOwner, permissions.IsAuthenticated)
    queryset = scheduler_models.Schedule.objects.all()
    serializer_class = scheduler_serializers.ScheduleSerializer
    renderer_classes = [renderers.JSONRenderer]

    def destroy(self, request, *args, **kwargs):
        schedule = self.get_object()
        section = scraper_models.Section.objects.get(pk=kwargs["section_id"])
        schedule.sections.remove(section)
        return response.Response(status=200)


class AddCourseScheduleView(generics.UpdateAPIView):
    permission_classes = (IsOwner, permissions.IsAuthenticated)
    queryset = scheduler_models.Schedule.objects.all()
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = scraper_serializers.CourseSerializer

    def partial_update(self, request, *args, **kwargs):
        schedule = self.get_object()
        course = scraper_models.Course.objects.get(pk=request.data["course_id"])

        sections_obj = scraper_models.Section.objects.filter(
            dept=course.dept, course_num=course.course_num, term_code=schedule.term_code
        ).all()

        if len(sections_obj) == 0:
            return response.Response(status=404)

        schedule.courses.add(course)

        course_data = self.get_serializer(course).data
        instructors = {}
        for section in sections_obj:
            if not section.instructor in instructors:
                historical_performance = scraper_models.Grades.objects.instructor_performance(
                    course.dept, course.course_num, section.instructor
                )
                instructors[section.instructor] = historical_performance
            section.historical_performance = instructors[section.instructor]

        serialized_sections = scraper_serializers.SectionSerializer(
            sections_obj, many=True
        ).data
        course_data["sections"] = serialized_sections
        return response.Response(course_data)


class DeleteCourseScheduleView(generics.DestroyAPIView):
    permission_classes = (IsOwner, permissions.IsAuthenticated)
    queryset = scheduler_models.Schedule.objects.all()
    serializer_class = scheduler_serializers.ScheduleSerializer
    renderer_classes = [renderers.JSONRenderer]

    def destroy(self, request, *args, **kwargs):
        schedule = self.get_object()
        course = scraper_models.Course.objects.get(pk=kwargs["course_id"])
        schedule.courses.remove(course)
        sections_to_remove = schedule.sections.filter(
            dept=course.dept, course_num=course.course_num
        )
        schedule.sections.remove(sections_to_remove)
        return response.Response(200)
