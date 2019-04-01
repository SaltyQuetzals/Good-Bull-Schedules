from django.db import models
from scraper import models as scraper_models
from django.contrib.auth import models as auth_models

# Create your models here.
class Schedule(models.Model):
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    sections = models.ManyToManyField(
        scraper_models.Section, help="The sections that this user has selected."
    )
    name = models.CharField(max_length=64, help="The name of the schedule")
    term_code = models.IntegerField()

    class Meta:
        unique_together = ("user", "name")
        ordering = ("-term_code",)

