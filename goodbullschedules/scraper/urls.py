from django.urls import path
from scraper import views

urlpatterns = [
    path(
        "<str:dept>/<str:course_num>/<int:term_code>/<str:section_num>",
        views.SectionRetrieveView.as_view(),
        name="section-retrieve",
    ),
    path(
        "<str:dept>/<str:course_num>/<int:term_code>",
        views.CourseRetrieveView.as_view(),
        name="course-retrieve",
    ),
]
