from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserFeedbackForm
from django.contrib import messages
from .models import JobType, Job, Offer, User, Agreement
from django.db.models import Q

# Create your views here.
def index(request):
    # return HttpResponse("Hi!!! You are at the polls view index.")
    if request.user.is_authenticated:
        jobs = []
        cat = "Category"
        est = "Est. Completion Time"
        cols = [cat, est, ""]  # Last element is to provide space for the button
        
        # All jobs not for currently-logged in user
        non_user_jobs = Job.objects.filter(~Q(user=request.user))

        for job in non_user_jobs:
            jobs.append({cat: job.category, est: job.est_complete_time, "job_id": job.id})

        context = {"jobs": jobs, "cols": cols}
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


def express_interest(request):
    """
    i want to grab the job in the current row, and then check current users offers. 
    Get the first offer from current user, and then redirect to offer processed.html
    """

    if request.method != 'POST':
        return redirect('index')

    job_id = request.POST.get("job_id")
    if not job_id:
        messages.error(request, "Job is not specified")
        return redirect('index')

    # get job id or return 404.
    job = get_object_or_404(Job, id=job_id)

    existing_offer = Offer.objects.first()
    if existing_offer:
        messages.info(request, "you have expressed interest in this job")
        return redirect('index')

    offer = Offer.objects.create(user=request.user, job=job)

    return render(request, "servicerWebsite/offer_processed.html")


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

@login_required(login_url="/login/")
def requested_jobs(request):
    """
    Containsd all jobs requested by the currently logged-in user, with the option to delete some. 
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
    
    jobs = []
    cat = "Category"
    est = "Est. Completion Time"
    cols = [cat, est, ""]  # Last element is to provide space for the button

    for job in Job.objects.filter(user=request.user):
        jobs.append({cat: job.category, est: job.est_complete_time, "job_id": job.id})

    context = {"jobs": jobs, "cols": cols}
    return render(request, "servicerWebsite/your-requested-jobs.html", context)


@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
def agreed_jobs(request):
    """Gets & renders the page for listing all jobs for which mutual agreement has occurred

    Query is of the form `get from Agreement where offer1.user == signed-in user OR offer2.user == signed-in user`
    """

    user_id = "User ID"
    cat = "Category"
    est = "Est. Completion Time (hrs)"

    agreements = (
        Agreement.objects.filter(offer1__user=request.user)
        | Agreement.objects.filter(offer2__user=request.user)
    )

    jobs = []
    cols = [user_id, cat, est, "", ""]  # Last element is to provide space for the two buttons
    for agreement in agreements:
        # Figure out which job we agreed to do
        if agreement.offer1.user == request.user:
            job = agreement.offer1.job
            job_user = agreement.offer1.job.user
        else:
            job = agreement.offer2.job
            job_user = agreement.offer2.job.user
        jobs.append({user_id: job_user.username, cat: job.category, est: job.est_complete_time, "job_id": job.id})

    context = {"cols": cols, "jobs": jobs}
    return render(request, "servicerWebsite/agreed-jobs.html", context)

@login_required(login_url="/login/")
def mark_complete(request, pk=None):
    """Marks a specific job as completed, prompts the user to review said job & user

    'request' will (though doesn't yet) contain an ID into the Job table. Update the 'complete' parameter to True

    Args:
        request (_type_): _description_
    """
    job = get_object_or_404(Job, pk=pk)  # Get your current cat

    if request.method == 'POST':         # If method is POST,
        # job.complete = True
        # job.save()                       # delete the cat.
        pass

    return HttpResponseRedirect("/complete-feedback/")

@login_required(login_url="/login/")
def complete_feedback(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = UserFeedbackForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/feedback-submitted/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserFeedbackForm()
    return render(request, "servicerWebsite/marked-complete.html", {"form": form})

@login_required(login_url="/login/")
def feedback_submitted(request):
    """Generates the landing page for confirming a job's feedback has been submitted.
    No database interaction as we don't have a feedback table lol

    Returns:
        _type_: _description_
    """

    context = {}
    return render(request, "servicerWebsite/feedback-submitted.html", context)

@login_required(login_url="/login/")
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
 
@login_required(login_url="/login/")
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



### Non-view deletions
@login_required(login_url="/login/")
def delete_request(request, pk):
    job = get_object_or_404(Job, pk=pk)  # Get your current cat

    if request.method == 'POST':         # If method is POST,
        job.delete()                     # delete the cat.

    return redirect('/requests/')             # Finally, redirect to the homepage.
    # If method is not POST, render the default template.
    # *Note*: Replace 'template_name.html' with your corresponding template name.
