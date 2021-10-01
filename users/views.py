from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')
        else:
            messages.error(request, "Please Fill Data Properly.")
    else:
        form = UserRegisterForm()
    return render(request,'register.html',{'form':form})


@login_required
def profile(request):
    if request.method == 'POST' :
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES ,instance=request.user.profile)
        if p_form.is_valid() and u_form.is_valid() :
            p_form.save()
            u_form.save()
            return redirect('profile')
        else:
            messages.error(request, "Please Fill Data Properly.")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form' : u_form,
        'p_form' : p_form,
        'tab': 'profile'
    }
    return render(request,'profile.html',context)


