from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, UserFeedbackForm
from django.contrib import messages

# Create your views here.
def index(request):
    # return HttpResponse("Hi!!! You are at the polls view index.")
    if request.user.is_authenticated:

        cat = "Category"
        loc = "Location"
        est = "Est. Completion Time (hrs)"

        cols = [cat, loc, est, ""]  # Last element is to provide space for the button
        jobs = [
            {cat: "Vacuuming", loc: "Lister", est: 3},
            {cat: "Dishes", loc: "Lister", est: 0.5},
            {cat: "Walking the dog", loc: "Hub", est: 1},
            {cat: "Dusting", loc: "Lister", est: 1},
        ]

        context = {"jobs": jobs, "cols": cols, "user_id": 23423}
        return render(
            request,
            "servicerWebsite/auth_index.html",
            context
        )
    else:
        return render(
            request,
            "servicerWebsite/non_auth_index.html",
            {}
        )
    

def register(request):
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            auth_login(request, user)
            return HttpResponseRedirect('/index/')
            

    return render(request, 'servicerWebsite/register.html', {'form': form, 'title':'Register for Servicer'})
  

################ login forms################################################### 
def login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        # AuthenticationForm_can_also_be_used__
  
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = auth_login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('index')
        else:
            messages.info(request, f'account done not exit plz sign in')

    return render(request, 'servicerWebsite/login.html', {'form':form, 'title':'log in'})

def logout(request):
    auth_logout(request)
    return redirect('/')

################ About Page ################################################### 
def about(request):
    return render(request, "servicerWebsite/about.html")

################ Issues Page ################################################### 
def report_issue(request):
    return render(request, "servicerWebsite/report_issue.html")

################ Terms of Service Page ################################################### 
def tos(request):
    return render(request, "servicerWebsite/tos.html")

################ Contact Page ################################################### 
def contact(request):
    return render(request, "servicerWebsite/contact.html")

################ Documentation Page ################################################### 
def documentation(request):
    return render(request, "servicerWebsite/documentation.html")    

def test(request):
    return render(request, "servicerWebsite/test.html", {})

def requested_jobs(request):
    """
    Containsd all jobs requested by the currently logged-in user, and offers made on those jobs by other users.

    The context (the returned dictionary) contains an dict of jobs, where the content is of the form:
    {
        Job1: [Everyone who has offered to complete Job1],
        Job2: [Everyone who has offered to complete Job2],
        ...
    }

    where 'Job1', 'Job2', ... are requested by the currently logged in user.

    The queries will be something like `jobs = 'get from Jobs where user == signed-in user'`
    then `get from Offers where Offers.job IN jobs`

    I'll create a temporary table below
    """

    jobs = {
        "Job1": [
            {"Rating": 3, "Location": "Lister", "Jobs/Week": 2.1},
        ],
        "Job2": [
            {"Rating": 5, "Location": "Antarctica", "Jobs/Week": 1.1},
        ],
    }

    cols = ["Rating", "Location", "Jobs/Week", ""]  # Last element is to provide space for the button
    context = {"jobs": jobs, "cols": cols}
    return render(request, "servicerWebsite/your-requested-jobs.html", context)

def jobs_for_user_x(request):
    """
    Returns an array of jobs for a specified username 'X'

    Query will be something like `get from Jobs where user.username == 'X'`
    """
    cat = "Category"
    loc = "Location"
    est = "Est. Completion Time (hrs)"

    cols = [cat, loc, est, ""]  # Last element is to provide space for the button
    jobs = [
        {cat: "Vacuuming", loc: "Lister", est: 3},
        {cat: "Dishes", loc: "Lister", est: 0.5},
        {cat: "Walking the dog", loc: "Hub", est: 1},
        {cat: "Dusting", loc: "Lister", est: 1},
    ]

    context = {"cols": cols, "jobs": jobs, "user_id": 34569438756}
    return render(request, "servicerWebsite/jobs-for-user-x.html", context)


def offer_processed(request):
    """
    A confirmation screen TODO
    """
    context = {
        "job_offered": "Test Job",
        "user_job": "Test User",
        "requested_job": "Test Request",
    }
    return render(request, "servicerWebsite/offer-processed.html", context)


def agreed_jobs(request):
    """Gets & renders the page for listing all jobs for which mutual agreement has occurred

    Query is of the form `get from Agreement where offer1.user == signed-in user OR offer2.user == signed-in user`
    """

    user_id = "User ID"
    cat = "Category"
    loc = "Location"
    est = "Est. Completion Time (hrs)"

    cols = [user_id, cat, loc, est, "", ""]  # Last element is to provide space for the two buttons
    jobs = [
        {user_id: 234242, cat: "Vacuuming", loc: "Lister", est: 3},
        {user_id: 534242, cat: "Dishes", loc: "Lister", est: 0.5},
        {user_id: 134242, cat: "Walking the dog", loc: "Hub", est: 1},
        {user_id: 4534242, cat: "Dusting", loc: "Lister", est: 1},
    ]

    context = {"cols": cols, "jobs": jobs}
    return render(request, "servicerWebsite/agreed-jobs.html", context)

def marked_complete(request):
    """Marks a specific job as completed, prompts the user to review said job & user

    'request' will (though doesn't yet) contain an ID into the Job table. Update the 'complete' parameter to True

    Args:
        request (_type_): _description_
    """



    """
    Below is taken from https://docs.djangoproject.com/en/5.1/topics/forms/
    """

    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = UserFeedbackForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/feedback-recorded/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserFeedbackForm()
    context = {"form": form, "category": "Vacuuming", "user_id": 23745}
    return render(request, "servicerWebsite/marked-complete.html", context)

def feedback_submitted(request):
    """Generates the landing page for confirming a job's feedback has been submitted.
    No database interaction as we don't have a feedback table lol

    Returns:
        _type_: _description_
    """

    context = {"job_id": 34324}
    return render(request, "servicerWebsite/feedback-submitted.html", context)


def others_requested_jobs(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """

    cat = "Category"
    loc = "Location"
    est = "Est. Completion Time (hrs)"

    cols = [cat, loc, est, ""]  # Last element is to provide space for the button
    jobs = [
        {cat: "Vacuuming", loc: "Lister", est: 3},
        {cat: "Dishes", loc: "Lister", est: 0.5},
        {cat: "Walking the dog", loc: "Hub", est: 1},
        {cat: "Dusting", loc: "Lister", est: 1},
    ]

    context = {"jobs": jobs, "cols": cols, "user_id": 23423}
    return render(request, "servicerWebsite/others-requested-jobs.html", context)
 
def mutual_agreement(request):
    """This request returns a webpage notifying a user that mutual consent to perform tasks has occurred
    between them and someone else, and prompts them to visit `agreed/` and send contact information

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """

    context = {"other_user_id": 3498756}
    return render(request, "servicerWebsite/mutual-agreement.html", context)