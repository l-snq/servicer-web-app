from django.contrib import admin
from .models import Job, JobType, Offer, Agreement

# Register your models here.

admin.site.register(Job)
admin.site.register(JobType)
admin.site.register(Offer)
admin.site.register(Agreement)
