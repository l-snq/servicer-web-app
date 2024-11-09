from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
 
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_no = forms.CharField(max_length = 20)
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'password1', 'password2']


class UserFeedbackForm(forms.Form):
    _YN_CHOICES = [
        ('1', 'Yes'),
        ('2', 'No'),
    ]
    job_is_completed = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=_YN_CHOICES, 
        label="Was the job completed?"
    )

    completion_is_satisfactory = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=_YN_CHOICES, 
        label="Was the job completed satisfactorily?"

    )

    would_you_use_this_person_again = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=_YN_CHOICES, 
        label="Would you use this person again?"
    )

    would_you_recommend_this_person = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=_YN_CHOICES, 
        label="Would you recommend this person to someone else?"
    )

    # https://pypi.org/project/django-ratings/
    # ratings = RatingField(range=5) # 5 possible rating values, 1-5

