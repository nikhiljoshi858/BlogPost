from django.shortcuts import render, redirect
from account.forms import *
from django.contrib.auth import logout, login, authenticate
from blog.models import *
# Create your views here.

def registration_view(request):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            account = form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            # account = authenticate(email=email, password=password)
            login(request, account)
            # Check urls.py we have given a name 'home' for the homepage view func
            return redirect('home')
        
        else:
            return render(request, 'account/register.html', context={'registration_form': form})
    
    else:
        form = RegistrationForm()
        return render(request, 'account/register.html', context={'registration_form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('home')
        
    else:
        form = AccountAuthenticationForm()
        return render(request, 'account/login.html', context={'login_form': form})


def account_view(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('login')
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                'email': request.POST['email'],
                'username': request.POST['username'],
            }
            form.save()
            context['success_message'] = 'Changes saved!!!'
    
    else:
        form = AccountUpdateForm(
            initial = {
                'email': request.user.email,
                'username': request.user.username
            }
        )
    context['account_form'] = form
    blog_posts = BlogPost.objects.filter(author=request.user)
    context['blog_posts'] = blog_posts    
    
    return render(request, 'account/account.html', context)


def must_authenticate_view(request):
    return render(request, 'account/must_authenticate.html')