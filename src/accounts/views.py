from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import UserRegistrationForm, UserLoginForm


def register_page(request):
   form = UserRegistrationForm(request.POST or None)
   if form.is_valid():
      form.save()
      return redirect('home')
   context = {
      "registeration_page": True,
      "form": form,
   }
   return render(request, 'register.html', context)

@login_required
def logout(request):
   """ Log user out """
   auth.logout(request)
   messages.success(request, 'You have successfully logged out')

   return redirect('home')


def login_page(request):
   if request.user.is_authenticated:
      return redirect('home')

   form = UserLoginForm(request.POST or None)
   if form.is_valid():
      user = auth.authenticate(username=request.POST['username'],
                               password=request.POST['password'])
         
      if user:
         auth.login(user=user, request=request)
         messages.success(request, "You have successfully logged in!")
         return redirect('home')
      else:
         form.add_error(None, "Your username or password is incorect")

   return render(request, 'login.html', {"form": form})

