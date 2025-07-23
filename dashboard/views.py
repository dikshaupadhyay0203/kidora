from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
# Create your views he
from .AI_agent.ai_main import main_generate
from django.conf import settings
import os



@login_required
def dashboard(request):
    return render(request,"dashboard/dashboard.html",{'first_name': request.user.first_name })

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
          user.first_name = request.POST.get('first_name')
          user.last_name = request.POST.get('last_name')
          user.username = request.POST.get('username')
          user.email = request.POST.get('email')
          user.save()
          messages.success(request, f"User profile updated successfully")
          return redirect('dashboard')
    context = {'user': user}
    return render(request, 'dashboard/edit_profile.html', context)


@login_required
def change_password(request):
     user = request.user
     if request.method == "POST":   
          new_password = request.POST.get('password')
          user.set_password(new_password)
          user.save()
          messages.success(request, f"Password changed successfully")
          return redirect('dashboard')
     return render(request, 'dashboard/dashboard.html')



