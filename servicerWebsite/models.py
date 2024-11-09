import datetime

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class JobType(models.Model):
    category = models.CharField(max_length=200)

class Job(models.Model):
    category = models.ForeignKey(to=JobType, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    est_complete_time = models.IntegerField()

    def __str__(self):
        return self.job1


class Offer(models.Model):
    job = models.ForeignKey(to=Job, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)


class Agreement(models.Model):
    offer1 = models.ForeignKey(to=Offer, related_name="Offer_1", on_delete=models.CASCADE)
    offer2 = models.ForeignKey(to=Offer, related_name="Offer_2", on_delete=models.CASCADE)
