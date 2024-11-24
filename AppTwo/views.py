from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from AppTwo.models import UsersModel
from faker import Faker
from AppTwo.forms import UsersForm, UserProfileInfoForm

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    return render(request, "index.html")

def help(request):
    help_dict = {"help_insert": "HELP PAGE"}
    return render(request, "help.html", context=help_dict)

def add_fake_data(request):
    fake = Faker()
    for _ in range(10):  # Generating 10 fake students
        UsersModel.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email()
        )

def register(request):
    registered = False
    if request.method == "POST":
        user_form = UsersForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user


            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UsersForm()
        profile_form = UserProfileInfoForm()

    return render(request, "registration.html", {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            
            else:
                return HttpResponse("Account not active")
            
        else:
            print("Someone tried to login and failed")
            return HttpResponse("invalid login details")
        
    else:
        return render(request, 'user_login.html', {})
    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


