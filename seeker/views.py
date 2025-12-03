from django.shortcuts import render, redirect
# signup 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def signup_view(request):

    errors = {}

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")

        # validate email format 
        try:
            validate_email(email)
        except ValidationError:
            errors["email"] = "Please enter a valid email address"

        # email already used 
        if User.objects.filter(email=email).exists():
            errors["email"] = "Email is already in use"

        # username already used
        if User.objects.filter(username=username).exists():
            errors["username"] = "Username is already taken"

        # validate password strength
        password_errors = []

        # length check
        if len(password) < 8:
            password_errors.append("Must be at least 8 characters")

        # uppercase check
        if not any(c.isupper() for c in password):
            password_errors.append("Must include at least one uppercase letter")

        # special char check
        specials = "!@#$%^&*()-_=+[]{};:,.<>?/|"
        if not any(c in specials for c in password):
            password_errors.append("Must include at least one special character")

        # errors["password"]
        if password_errors:
            errors["password"] = password_errors

        # if no errors => create user
        if not errors:
            new_user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            return redirect("seeker:signin")

        # إذا فيه أخطاء يرجع للصفحة
        return render(request, "seeker/signup.html", {"errors": errors})

    # GET request
    return render(request, "seeker/signup.html")

def signin_view(request):
    error = False

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"]
        )

        if user:
            login(request, user)
            return redirect(request.GET.get("next", "/"))
        else:
            error = True  

    return render(request, "seeker/signin.html", {"error": error})


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("/")
