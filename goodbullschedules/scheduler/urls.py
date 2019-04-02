from scheduler import views
from django.urls import path

urlpatterns = [path("", views.CreateScheduleView.as_view())]

