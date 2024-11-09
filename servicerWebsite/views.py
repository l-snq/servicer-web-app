from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm

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
    

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username, email, password)
            user.save()
            ######################### mail system #################################### 
            htmly = get_template('user/Email.html')
            d = { 'username': username }
            subject, from_email, to = 'welcome', 'your_email@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            ################################################################## 
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')

    form = UserRegisterForm()
    return render(request, 'servicerWebsite/register.html', {'form': form, 'title':'Register for Servicer'})
  

################ login forms################################################### 
def login(request):
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__
  
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('index')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'servicerWebsite/login.html', {'form':form, 'title':'log in'})

################ About Page ################################################### 
def about(request):
    return render(request, "servicerWebsite/about.html")


################ Terms of Service Page ################################################### 
def tos(request):
    return render(request, "servicerWebsite/tos.html")

################ Contact Page ################################################### 
def contact(request):
    return render(request, "servicerWebsite/contact.html")
    

def test(request):
    return render(request, "servicerWebsite/test.html", {})

def offered_jobs(request):

    """
    I'm thinking that the context (the returned dictionary) contains an dict of jobs, where the content is of the form:
    {
        Job1: [Everyone who has offered to complete Job1],
        Job2: [Everyone who has offered to complete Job2],
        ...
    }

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
    return render(request, "servicerWebsite/your-offered-jobs.html", context)

def jobs_for_user_x(request):

    """
    Context in this case is an array of jobs for a specified user with user id 'x'
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
    context = {
        "job_offered": "Test Job",
        "user_job": "Test User",
        "requested_job": "Test Request",
    }
    return render(request, "servicerWebsite/offer-processed.html", context)
