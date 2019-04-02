from django.db import models
from scraper import models as scraper_models


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
    term_code = models.IntegerField(db_index=True)
    crn = models.IntegerField()
    dept = models.CharField(max_length=5, db_index=True)
    course_num = models.CharField(max_length=6, db_index=True)
    section_num = models.CharField(max_length=6, db_index=True)
    min_credits = models.FloatField(null=True)
    max_credits = models.FloatField(null=True)

    instructor = models.CharField(max_length=150, null=True, blank=True)
    meetings = models.ManyToManyField(Meeting)

    class Meta:
        db_table = "section"
        unique_together = ("term_code", "crn")
