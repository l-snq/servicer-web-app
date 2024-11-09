from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    # return HttpResponse("Hi!!! You are at the polls view index.")
    if request.user.is_authenticated:
        return render(
            request,
            "servicerWebsite/auth_index.html",
            {}
        )
    else:
        return render(
            request,
            "servicerWebsite/non_auth_index.html",
            {}
        )

def login(request):
    # TODO: If already logged in, redirect to auth_index.html
    return render(
        request,
        "servicerWebsite/login.html",
        {},
    )