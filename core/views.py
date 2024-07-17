from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, UpdateProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from blogapp.models import Blog
from .models import Profile


# Create your views here.
User = get_user_model()


def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect("signin")
        
    context = {"form":form}
    return render(request, "core/signup.html", context)

def signin(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            messages.success(request, "Login successful")
            login(request, user)
            return redirect("index")
        
        else:
            messages.warning(request, "Invalid credentials")
            return redirect("signin")
    context = {}
    return render(request, "core/login.html", context)

def signout(request):
    logout(request)
    return redirect("index")

@login_required(login_url="signin")
def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    blogs = Blog.objects.filter(user=user_profile)
    profile = Profile.objects.get_or_create(user=user_profile)[0]
    is_following = False
    if request.user.is_authenticated:
        is_following = profile.is_following(request.user)
        
    context = {"user_profile": user_profile, "profile":profile, "blogs":blogs, 'is_following': is_following}
    return render(request, "core/profile.html", context)

@login_required(login_url="signin")
def update_profile(request):
    if request.user.is_authenticated:
        user = request.user
        form = UpdateProfileForm(instance=user)
        if request.method == 'POST':
            form = UpdateProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile update successfully")
                return redirect("profile")
            
    context = {"form":form}
    return render(request, "core/update_profile.html", context)


@login_required(login_url="signin")
def user_list(request):
    users = User.objects.exclude(username=request.user.username)
    context = {"users":users}

    return render(request, 'core/user_list.html', context)

@login_required(login_url="signin")
def follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    profile = Profile.objects.get_or_create(user=user_to_follow)[0]
    profile.follow(request.user)
    return redirect('profile', username=username)

@login_required(login_url="signin")
def unfollow(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    profile = Profile.objects.get_or_create(user=user_to_unfollow)[0]
    profile.unfollow(request.user)
    return redirect('profile', username=username)