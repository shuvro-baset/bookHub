import random

from bookHub_app.models import *
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# ========== Custom printing function for debugging ============
from user_app.models import UserProfile


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
        user = User.objects.create_user(username=email, first_name=f_name, last_name=l_name, email=email,
                                        password=password)
        user.save()
        # setup userProfile object
        user_profile = UserProfile(user_id=user.id, occupation='occupation', bio='bio', address='address')
        user_profile.save()
        messages.success(request, "Registered Successfully!")

        recepient = f_name + " " + l_name

        html_content = render_to_string('emails/signup_email.html', { 
                "recepient": recepient
            })
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            "Thanks for signing up",
            text_content,
            "BookHub Team",
            [email]
        )

        email.attach_alternative(html_content, "text/html")
        email.send()

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
            
            recepient = email_auth

            html_content = render_to_string('emails/reset_pass_email.html', { 
                    "recepient": recepient,
                    "code": auth_number
                })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                "Password Recovery",
                text_content,
                "BookHub Team",
                [email_auth]
            )

            email.attach_alternative(html_content, "text/html")
            email.send()
            

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
        book_review = BooksReview.objects.filter(user=request.user)
        books = Books.objects.filter(uploader=request.user)
        book_categories = BookCategories.objects.all()

        global user_profile_ins
        user_profile_ins = UserProfile.objects.filter(user_id=request.user.id).first()
        if request.method == "POST":
            if 'personal_info' in request.POST:
                println('Personal Info form')
                f_name = request.POST.get('f_name')
                l_name = request.POST.get('l_name')
                user_ins = User.objects.get(id=request.user.id)
                if (f_name == ""):
                    user_ins.first_name = user_ins.first_name
                else:
                    user_ins.first_name = f_name
                if (l_name == ""):
                    user_ins.last_name = user_ins.last_name
                else:
                    user_ins.last_name = l_name
                # updating user info
                user_ins.save()
                messages.success(request, "Changes applied!")

                # getting userProfile info
                address = request.POST.get('address')
                occupation = request.POST.get('occupation')
                bio = request.POST.get('bio')
                if (address == ""):
                    user_profile_ins.address = user_profile_ins.address
                else:
                    user_profile_ins.address = address
                if (occupation == ""):
                    user_profile_ins.occupation = user_profile_ins.occupation
                else:
                    user_profile_ins.occupation = occupation
                if (bio == ""):
                    user_profile_ins.bio = user_profile_ins.bio
                else:
                    user_profile_ins.bio = bio
                if 'image' in request.FILES:
                    user_profile_ins.profile_pic = request.FILES['image']
                else:
                    user_profile_ins.profile_pic = user_profile_ins.profile_pic
                user_profile_ins.save()
                messages.success(request, "Chenges applied!")

            if 'book_upload' in request.POST:
                book_name = request.POST.get('book_name')
                author_name = request.POST.get('author_name')
                language = request.POST.get('language')
                book_description = request.POST.get('book_description')
                category_value = request.POST.get('category_value')
                book_pdf = request.POST.get('book_pdf')
                book_pdf = request.FILES['book_pdf']
                book_thumbnail = request.FILES['book_thumb']

                println(type(book_pdf))
                println(type(book_thumbnail))

                books_ins = Books(
                    uploader=request.user,
                    book=book_pdf,
                    book_thumbnail=book_thumbnail,
                    book_name=book_name,
                    author_name=author_name,
                    description=book_description,
                    book_category=category_value,
                    language=language,
                )

                books_ins.save()
                messages.success(request, "Book uploaded successfully!")

                println("Data saved")

        context = {
            'user_profile_ins': user_profile_ins,
            'book_reviews': book_review,
            'books': books,
            'categories': book_categories
        }

        return render(request, 'dashboard.html', context=context)
    else:
        messages.warning(request, "You Must Be Logged In")
        return redirect('/login')
