from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm


# ======================
# AUTH VIEWS
# ======================

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    print("=== LOGIN VIEW HIT ===")
    print("Method:", request.method)

    if request.method == "POST":
        print("POST RECEIVED")
        form = LoginForm(request.POST)

        if form.is_valid():
            print("FORM VALID")
            user = form.cleaned_data["user"]
            print("User authenticated:", user)

            login(request, user)
            print("LOGIN() CALLED")

            next_url = request.GET.get("next")
            print("NEXT URL:", next_url)

            if next_url:
                print("Redirecting to next")
                return redirect(next_url)

            print("Redirecting to dashboard")
            return redirect("dashboard")

        else:
            print("FORM INVALID")
            print(form.errors)

    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# ======================
# DASHBOARD ROUTER
# ======================

@login_required
def dashboard_view(request):

    if request.user.role in ["admin", "cert", "veteran"]:
        return redirect("operational_dashboard")

    return redirect("reporter_dashboard")


@login_required
def operational_dashboard(request):
    return render(request, "accounts/operational_dashboard.html")


@login_required
def reporter_dashboard(request):
    return render(request, "accounts/reporter_dashboard.html")