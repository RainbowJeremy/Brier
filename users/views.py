from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm, UserUpdateForm
from .models import Profile
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView


# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}')
            return redirect('pages:home')
    else:
        form = UserCreationForm()
    context = {'form':form}
    return render(request, 'register.html', context)



@login_required
def edit_profile(request):
    form = ProfileForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('users:profile')
    else:
        form = ProfileForm()
    context = {'bioform': form, 'edit_done': 'Done'}
    return render(request, 'profile.html', context)

@login_required
def profile(request):
    if request == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(f'Your Account has been Updated!')
            redirect('profile')#???
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)

    context = {'u_form':u_form, 'p_form':p_form}
    return render(request, 'profile.html', context)

def score_explained(request):
    return render(request, 'scoreexplained.html', {})
