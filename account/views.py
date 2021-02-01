from django.db import IntegrityError
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.models import User
import re
from django.contrib.auth.decorators import login_required
from library.models import Book


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        remember = request.POST.get('remember', False)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                if not remember:
                    request.session.set_expiry(0)
                auth_login(request, user)
                if request.GET.get('next') is not None:
                    return redirect(request.GET.get('next'))
                else:
                    return HttpResponseRedirect('/')
            else:
                messages.error(request, 'Requested user is disabled')
                return HttpResponseRedirect('/account/login/')
        else:
            messages.error(request, 'Invalid credentials. Try again.')
            return HttpResponseRedirect('/account/login/')

    return render(request, 'account/login.html')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']
        if password == password2:
            if len(password2) <= 7:
                messages.error(request, 'Password minimum 8 characters long')
            elif re.search('[A-Z]', password) is None:
                messages.error(request, "Make sure your password has a capital letter in it")
            elif re.search('[a-z]', password) is None:
                messages.error(request, "Make sure your password has a small letter in it")
            elif re.search('[0-9]', password) is None:
                messages.error(request, "Make sure your password has a number in it")
            elif re.search("['!','@','#','$','%','^','&','*','(',')']", password) is None:
                messages.error(request, "Make sure your password has a symbol in it")
            else:
                try:
                    new_user = User.objects.create_user(username=username, email=email, first_name=first_name,
                                                        last_name=last_name, password=password)
                    new_user.save()
                    messages.success(request, 'registration Successful. Login now.')
                except IntegrityError:
                    messages.warning(request, 'Username or email already in database.')
                finally:
                    return redirect('account:login')

        else:
            messages.error(request, 'Passwords not matched')
    return render(request, 'account/registration.html')


def logout_request(request):
    logout(request)
    return redirect('books:book_list')

#
# @login_required
# def account(request):
#     post_objects = Post.objects.filter(author=request.user)
#     book_objects = Book.objects.filter(user=request.user)
#     movie_objects = Movie.objects.filter(author=request.user)
#     return render(request, 'account/dashboard.html',
#                   {'posts': post_objects,
#                    'books': book_objects,
#                    'movies': movie_objects,
#                    })
