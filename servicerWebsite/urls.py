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

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path('login/', views.login, name ='login'),
    path('logout/', auth.LogoutView.as_view(template_name ='user/index.html'), name ='logout'),
    path('register/', views.register, name ='register'),
    path("about/", views.about, name = 'about'),
    path("tos/", views.tos, name = "tos"),
    path("contact/", views.contact, name="contact"),
    path("test/", views.test, name="test"),
    path("requests/", views.requested_jobs, name="requests"),
    path("requests-x/", views.jobs_for_user_x, name="requests"),
    path("offer-processed/", views.offer_processed, name="process-offer"),
    path("agreed/", views.agreed_jobs, name="agreed"),
    path("completed/", views.marked_complete, name="completed"),
    path("feedback-submitted/", views.feedback_submitted, name="completed"),
    path("others-requested/", views.others_requested_jobs, name="others-requested"),
    path("mutual/", views.mutual_agreement, name="mutual agreement"),
]
