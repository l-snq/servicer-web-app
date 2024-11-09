import datetime

from django.utils import timezone
from django.db import models

# Create your models here.


class Jobs(models.Model):
    job1 = models.CharField(max_length=200)
    job2 = models.CharField(max_length=200)
    job3 = models.CharField(max_length=200)
    job4 = models.CharField(max_length=200)

    def __str__(self):
        return self.job1


class User(models.Model):
    name = models.CharField(max_length=200)
    time_submitted = models.DateTimeField("date submitted")
    jobs_offered = models.ManyToManyField('Jobs')
    #models.ForeignKey(Jobs, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    def was_published_recently(self):
        return self.time_submitted >= timezone.now() - datetime.timedelta(days=1)
