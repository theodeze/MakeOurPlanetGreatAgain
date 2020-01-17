from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from apps.authentication.form import SignUpForm
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'registration/profile.html')