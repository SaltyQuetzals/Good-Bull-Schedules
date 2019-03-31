from django.db import models

# from scraper.models import Section


class Grades(models.Model):
    A = models.IntegerField()
    B = models.IntegerField()
    C = models.IntegerField()
    D = models.IntegerField()
    F = models.IntegerField()
    I = models.IntegerField()
    S = models.IntegerField()
    U = models.IntegerField()
    Q = models.IntegerField()
    X = models.IntegerField()

    gpa = models.FloatField()
    section = models.OneToOneField(
        "Section", on_delete=models.CASCADE, related_name="grades"
    )

    class Meta:
        db_table = "grades"
