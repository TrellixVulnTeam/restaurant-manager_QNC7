from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistraterFrom, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.decorators import login_required

def register_view(request):
	if request.method == 'POST':
		form = UserRegistraterFrom(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created! You are not able to log in')
			return redirect('users-login')
	else:
		form = UserRegistraterFrom()
	return render(request, 'users/register.html', {'form': form})

@login_required
def profile_view(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account details have been updated!')
			return redirect('users-profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'u_form': u_form,
		'p_form': p_form
	}
	return render(request, 'users/profile.html', context)