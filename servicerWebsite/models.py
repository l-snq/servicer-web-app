import datetime

from django.utils import timezone
from django.db import models


class Job(models.Model):
    job1 = models.CharField(max_length=200)
    job2 = models.CharField(max_length=200)
    job3 = models.CharField(max_length=200)
    job4 = models.CharField(max_length=200)

    def __str__(self):
        return self.job1
