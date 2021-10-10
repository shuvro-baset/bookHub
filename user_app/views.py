import random

from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

# ========== Custom printing function for debugging ============

def println(text):
    print("\n====================\n", text, "\n====================\n")

# ========== Custom printing function for debugging ============


# Create your views here.
def signup(request):
    if request.method == 'POST':
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username=email, first_name=f_name, last_name=l_name, email=email, password=password)
        user.save()
        
        messages.success(request, "Registered Successfully!")

        return redirect('login')
    return render(request, 'signup.html')

def app_login(request):
    println(request.user)
    if request.method == "POST":
        println("1. Initializing Login system")
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            println("2. User is authenticated")
            login(request, user)
            println("3. User logged in")
            
            messages.success(request, "Logged In Successfully!")

            return redirect('/user-dashboard')

        else:
            messages.error(request, "Incorrect login credentials!")

    return render(request, 'login.html')

def app_logout(request):
    logout(request)
    messages.info(request, "Logged Out!")

    return redirect('/')

def forget_password(request):
    if request.method == "POST":
        global email_auth
        email_auth = request.POST.get('email')

        try:
            User.objects.get(username=email_auth)
            request.session['auth_permission'] = True

            return redirect('/code-auth')
        
        except:
            request.session['auth_permission'] = False
            
            messages.warning(request, "Email Address Doesn't Exist!")

    context = {}
    return render(request, 'forget-password.html', context=context)

def code_authentication(request):
    if 'auth_permission' in request.session and request.session['auth_permission']:

        if request.method == "GET":
            global auth_number
            auth_number = random.randint(1000, 9999)
            auth_number = str(auth_number)
            message_body = "Your password recovery code - " + auth_number
            println(message_body)

            send_mail(
                'Password Reset',
                message_body,
                'BookHub Info',
                [email_auth],
                fail_silently=False
            )

        if request.method == "POST":
            verification_code = request.POST.get('code')

            if verification_code == auth_number:
                println("Verification code matched")
                request.session['reset_permission'] = True

                request.session['auth_permission'] = False

                return redirect('/reset-forgetten-password')
            else:
                request.session['reset_permission'] = False
                return HttpResponse("<h1>Verification code is invalid</h1>")

        context = {}
        return render(request, 'code.html', context)
    else:
        messages.warning(request, "You Don't Have Persmission To Proceed!")
        return redirect('/forget-password')

def reset_forget_pass(request):
    if 'reset_permission' in request.session and request.session['reset_permission']:

        if request.method == "POST":
            new_password = request.POST['new_password']
            println(new_password)

            user = User.objects.get(username=email_auth)
            println(user)
            user.set_password(new_password)
            user.save()

            println("Password changed")
            request.session['reset_permission'] = False

            messages.success(request, "Password Reset Successful!")

            return redirect('/login')

        return render(request, 'reset_forget_pass.html')
    
    else:
        messages.warning(request, "You Don't Have Persmission To Proceed!")
        return redirect('/')

def reset_password(request):
    if request.user.is_authenticated:
        println("Reset password system initialized")

        if request.method == "POST":
            new_password = request.POST['new_password']
            println(new_password)

            user = User.objects.get(username=request.user)
            println(user)
            user.set_password(new_password)
            user.save()

            messages.success(request, "Password Reset Successful!")

            return redirect('/login')


        context = {}
        return render(request, 'reset-password.html', context=context)
    
    else:
        messages.warning(request, "You Must Be Logged In")
        return redirect('/login')


def userDashboard(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            first_name = request.user.first_name
            last_name = request.user.last_name
            email = request.user.email

            context = {
                "f_name": first_name,
                "l_name": last_name,
                "email": email,
            }
            
        constext = {}
        return render(request, 'dashboard.html', context=context)
    else:
        messages.warning(request, "You Must Be Logged In")
        return redirect('/login')

