from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile


def profile(request, pk):
    """
    View function to display the user's profile.
    """
    profile = Profile.objects.get(pk=pk)
    context = {
        'profile': profile
    }
    return render(request, 'users/profile.html', context)

@login_required
def profile_update(request):
    """
    View function to update the user's profile.
    """
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/profile_update.html', context)

@login_required
def user(request):
    """
    View function to display the user's information.
    """
    return render(request, 'users/user.html')

@login_required
def user_update(request):
    """
    View function to update the user's information.
    """
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
    
    context = {
        'user_form': user_form
    }
    return render(request, 'users/user_update.html', context)

