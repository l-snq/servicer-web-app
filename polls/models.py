from django.db import models

# Create your models here.


class Jobs(models.Model):
    job1 = models.CharField(max_length=200)
    job2 = models.CharField(max_length=200)
    job3 = models.CharField(max_length=200)
    job4 = models.CharField(max_length=200)


class User(models.Model):
    name = models.CharField(max_length=200)
    time_submitted = models.DateTimeField("date submitted")
    jobs_offered = models.ForeignKey(Jobs, on_delete=models.CASCADE)
