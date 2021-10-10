from django.contrib import messages
from django.shortcuts import redirect, render


# Create your views here.
def home(request):
    context = {
        "home": "active"
    }
    return render(request, 'home.html', context)

def books(request):
    context = {
        "books": "active"
    }
    return render(request, 'books.html', context=context)

def blogs(request):
    context = {
        "blogs": "active"
    }
    return render(request, 'all-blogs.html', context)

def my_blog(request):
    if request.user.is_authenticated:
        context = {
            "my_blog": "active"
        }
        return render(request, 'blog.html', context)
    
    else:
        messages.warning(request, "You must be logged in")
        return redirect('/login')

def contact(request):
    context = {
        "contact": "active"
    }
    return render(request, 'contact.html', context)

def about(request):
    context = {
        "about": "active"
    }
    return render(request, 'about-us.html', context)
