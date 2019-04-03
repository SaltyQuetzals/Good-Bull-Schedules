from scheduler import views
from django.urls import path

urlpatterns = [
    path("", views.CreateScheduleView.as_view()),
    path("<int:pk>", views.RetrieveDestroyScheduleView.as_view()),
    path("<int:pk>/sections", views.AddSectionScheduleView.as_view()),
    path(
        "<int:pk>/sections/<slug:section_id>", views.DeleteSectionScheduleView.as_view()
    ),
    path("<int:pk>/courses", views.AddCourseScheduleView.as_view()),
    path("<int:pk>/courses/<slug:course_id>", views.DeleteCourseScheduleView.as_view()),
]

