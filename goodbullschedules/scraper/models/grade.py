from django.db import models

# from scraper.models import Section


class GradeManager(models.Manager):
    def instructor_performance(self, dept: str, course_num: str, instructor: str):
        return (
            self.prefetch_related("section")
            .filter(
                section__dept=dept,
                section__course_num=course_num,
                section__instructor=instructor,
            )
            .aggregate(
                A=models.Avg("A"),
                B=models.Avg("B"),
                C=models.Avg("C"),
                D=models.Avg("D"),
                F=models.Avg("F"),
                I=models.Avg("I"),
                S=models.Avg("S"),
                U=models.Avg("U"),
                Q=models.Avg("Q"),
                X=models.Avg("X"),
            )
        )


class Grades(models.Model):
    A = models.IntegerField(db_index=True)
    B = models.IntegerField(db_index=True)
    C = models.IntegerField(db_index=True)
    D = models.IntegerField(db_index=True)
    F = models.IntegerField(db_index=True)
    I = models.IntegerField(db_index=True)
    S = models.IntegerField(db_index=True)
    U = models.IntegerField(db_index=True)
    Q = models.IntegerField(db_index=True)
    X = models.IntegerField(db_index=True)
    objects = GradeManager()

    gpa = models.FloatField()
    section = models.OneToOneField(
        "Section", on_delete=models.CASCADE, related_name="grades", db_index=True
    )

    class Meta:
        db_table = "grades"
