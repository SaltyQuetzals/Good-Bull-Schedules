from django.db import models
from scraper import models as scraper_models
from django.contrib.auth import models as auth_models

# Create your models here.
class Schedule(models.Model):
    owner = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(scraper_models.Course)
    sections = models.ManyToManyField(scraper_models.Section)
    name = models.CharField(max_length=64)
    term_code = models.IntegerField()

    class Meta:
        unique_together = ("owner", "name")
        ordering = ("-term_code",)

