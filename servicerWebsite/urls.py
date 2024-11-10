"""
URL configuration for servicerWebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth
from . import views

app_name = "servicer"


urlpatterns = [
    path("", views.index, name="index"),
    path("index/", views.index, name="index"),
    path('login/', views.login, name ='login'),
    path('logout/', views.logout, name ='logout'),
    path('register/', views.register, name ='register'),
    path("about/", views.about, name = 'about'),
    path("tos/", views.tos, name = "tos"),
    path("contact/", views.contact, name="contact"),
    path("test/", views.test, name="test"),
    path("requests/", views.requested_jobs, name="requests"),
    path("create-job/", views.create_job, name="create_job"),
    path("offer-processed/", views.offer_processed, name="process-offer"),
    path("complete-feedback/", views.complete_feedback, name="complete-feedback"),
    path("agreed/", views.agreed_jobs, name="agreed"),
    path("feedback-submitted/", views.feedback_submitted, name="completed"),
    path("others-requested/", views.others_requested_jobs, name="others-requested"),
    path("mutual/", views.mutual_agreement, name="mutual agreement"),
    path('admin/', admin.site.urls),
    path("documentation/" , views.documentation, name="documentation"),
    path("report_issue/", views.report_issue, name="report_issue"),
    path("express_interest/<int:pk>", views.express_interest, name="express_interest"),
    path("delete-request/<int:pk>", views.delete_request, name='delete_request'),
    path("mark-complete/<int:pk>", views.mark_complete, name='mark_complete')
]
