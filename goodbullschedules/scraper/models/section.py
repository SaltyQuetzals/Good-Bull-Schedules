from django.db import models


class Meeting(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    meeting_days = models.CharField(max_length=7)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    meeting_type = models.CharField(max_length=50)

    class Meta:
        db_table = "meeting"


class Section(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=75)
    term_code = models.IntegerField()
    crn = models.IntegerField()
    dept = models.CharField(max_length=5)
    course_num = models.CharField(max_length=6)
    section_num = models.CharField(max_length=6)
    min_credits = models.FloatField(null=True)
    max_credits = models.FloatField(null=True)

    instructor = models.CharField(max_length=150, null=True, blank=True)
    meetings = models.ManyToManyField(Meeting)

    class Meta:
        db_table = "section"
