from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Book
from .quote_generator import quotes
import random
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def book_list(request):  # Reading
    quote = random.choice(quotes)
    user = request.user
    books = Book.objects.filter(user=user).exclude(status="Available")
    error = None
    success = None
    if request.method == "POST":
        title = request.POST['title']
        author = request.POST['author']
        rating = request.POST['rating']

        new_book = Book.objects.create(title=title,
                                       author=author,
                                       rating=rating,
                                       )
        new_book.save()
        success = "Successfully added new book. Congratulations!"
    return render(request, 'library/list.html',
                  {'books': books,
                   'error': error,
                   'success': success,
                   'quote': quote,

                   })


@login_required
def library(request):  # Book shelf
    quote = random.choice(quotes)
    books = Book.objects.filter(user=request.user)
    total_count = len(books)
    paginator = Paginator(books, 25)
    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        books = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver last page of results
        books = paginator.page(paginator.num_pages)
    if request.method == "POST":
        title = request.POST['title']
        author = request.POST['author']
        edition = request.POST['edition']
        book_type = request.POST['book_type']
        new_book = Book.objects.create(title=title,
                                       user=request.user,
                                       author=author,
                                       edition=edition,
                                       type=book_type,
                                       status='Available')

        new_book.save()
        messages.success(request, "Successfully added new book.")
        return redirect('books:book_library')
    return render(request, 'library/library.html',
                  {'books': books,
                   'quote': quote,
                   'page': page,
                   'total': total_count,
                   })


@login_required
def delete_book(request, id):
    next_path = request.GET.get('next')
    book_obj = Book.objects.get(pk=id)
    if request.user == book_obj.user:
        book_obj.delete()
        if next_path is not None:
            return redirect(next_path)
        else:
            return redirect("books:book_library")
    else:
        return redirect("books:book_library")


@login_required
def change_status(request, id):
    status = request.POST['status']
    book = Book.objects.get(pk=id)
    book.status = status
    book.save()
    return redirect('books:book_list')


