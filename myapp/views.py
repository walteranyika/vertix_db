

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.shortcuts import render, redirect, get_object_or_404

from myapp.models import Book
from myapp.my_forms import BookForm, RegisterForm


# Create your views here.
@login_required
def show_books(request):
    books = Book.objects.all()  # select * from books
    return render(request, 'show_books.html', {'books': books})

@login_required
@permission_required('myapp.add_book', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Book {request.POST.get('title')} Created')
            return redirect('show_books')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})


# Django models
# Book.objects.create(title='River and the Source',
#                     year=2021,
#                     category='Fiction',
#                     cost=450,
#                     isbn='335678909876',
#                     published=True)
# Book.objects.create(title='Man of the people',
#                     year=1967,
#                     category='Politics',
#                     cost=900,
#                     isbn='335678909877',
#                     published=True)

#     delete-book/34
@login_required
@permission_required('myapp.delete_book', raise_exception=True)
def delete_book(request, id):
    book = Book.objects.get(id=id)  # select * from books where id = 34
    book.delete()  # delete from books where id=34
    messages.error(request, f'{book.title} Deleted Successfully')
    return redirect('show_books')

@login_required
@permission_required('myapp.change_book', raise_exception=True)
def edit_book(request, id):
    book = get_object_or_404(Book, pk=id)
    if request.method == 'POST':
        form = BookForm(request.POST,request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'{book.title} Updated Successfully')
            return redirect('show_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form})

# TODO  flash messages, image, login, register, django admin, permissions
def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('show_books')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
    else:
        form = RegisterForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def signout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')

# python manage.py createsuperuser