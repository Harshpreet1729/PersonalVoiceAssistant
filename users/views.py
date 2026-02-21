from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm, LoginForm


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    next_url = request.GET.get("next") or request.POST.get("next") or "chat"

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if not form.cleaned_data.get("remember_me"):
                request.session.set_expiry(0)
            else:
                # Keep session across browser restarts when "Remember me" is checked.
                request.session.set_expiry(60 * 60 * 24 * 30)
            return redirect(next_url)
    else:
        form = LoginForm(request)

    return render(request, "registration/login.html", {"form": form, "next": next_url})
