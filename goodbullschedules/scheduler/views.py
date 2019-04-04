from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, response, views

from scheduler import models as scheduler_models
from scheduler import serializers as scheduler_serializers
from scraper import models as scraper_models
from scraper import serializers as scraper_serializers

# Create your views here.


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class CreateScheduleView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = scheduler_models.Schedule.objects.all()
    serializer_class = scheduler_serializers.ScheduleSerializer

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
        }
        return response.Response(data=data)


class AddSectionScheduleView(generics.UpdateAPIView):
    permission_classes = (IsOwner, permissions.IsAuthenticated)
    queryset = scheduler_models.Schedule.objects.all()
    serializer_class = scheduler_serializers.ScheduleSerializer

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

    def destroy(self, request, *args, **kwargs):
        schedule = self.get_object()
        section = scraper_models.Section.objects.get(pk=kwargs["section_id"])
        schedule.sections.remove(section)
        return response.Response(status=200)


class AddCourseScheduleView(generics.UpdateAPIView):
    permission_classes = (IsOwner, permissions.IsAuthenticated)
    queryset = scheduler_models.Schedule.objects.all()

    def partial_update(self, request, *args, **kwargs):
        schedule = self.get_object()
        course = scraper_models.Course.objects.get(pk=request.data["course_id"])
        schedule.courses.add(course)
        return response.Response(status=200)


class DeleteCourseScheduleView(generics.DestroyAPIView):
    permission_classes = (IsOwner, permissions.IsAuthenticated)
    queryset = scheduler_models.Schedule.objects.all()
    serializer_class = scheduler_serializers.ScheduleSerializer

    def destroy(self, request, *args, **kwargs):
        schedule = self.get_object()
        course = scraper_models.Course.objects.get(pk=kwargs["course_id"])
        schedule.courses.remove(course)
        return response.Response(200)
