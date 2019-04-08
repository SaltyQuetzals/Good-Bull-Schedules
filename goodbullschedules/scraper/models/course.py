from django.db import models


class Course(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    dept = models.CharField(max_length=4, db_index=True)
    course_num = models.CharField(max_length=5, db_index=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    prerequisites = models.TextField(null=True, blank=True)
    corequisites = models.TextField(null=True, blank=True)
    min_credits = models.FloatField(null=True)
    max_credits = models.FloatField(null=True)
    distribution_of_hours = models.CharField(max_length=100)

    @property
    def full_name(self) -> str:
        return self.id + " " + self.name

    class Meta:
        db_table = "course"
        ordering = ("dept", "course_num")
