from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, BookForm
from .models import Book, Message, Purchase
from django.contrib.auth.models import User


def home(request):
    books = Book.objects.filter(available=True).order_by('-posted_at')
    department = request.GET.get('department')
    semester = request.GET.get('semester')
    query = request.GET.get('q')
    campus = request.GET.get('campus')

    if department:
        books = books.filter(department__icontains=department)
    if semester:
        books = books.filter(semester=semester)
    if query:
        books = books.filter(title__icontains=query)
    if campus:
        books = books.filter(campus__icontains=campus)

    return render(request, 'books/home.html', {'books': books})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'books/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'books/login.html', {'form': form})


@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})


@login_required
def dashboard(request):
    uploaded_books = Book.objects.filter(user=request.user)
    received_messages = Message.objects.filter(receiver=request.user)
    sent_messages = Message.objects.filter(sender=request.user)
    purchases = Purchase.objects.filter(user=request.user)

    return render(request, 'books/dashboard.html', {
        'uploaded_books': uploaded_books,
        'received_messages': received_messages,
        'sent_messages': sent_messages,
        'purchases': purchases,
    })


@login_required
def send_message(request):
    prefill_id = request.GET.get('user')
    users = User.objects.exclude(id=request.user.id)

    try:
        prefill_id = int(prefill_id)
    except (TypeError, ValueError):
        prefill_id = None

    if request.method == 'POST':
        receiver_id = request.POST['receiver_id']
        content = request.POST['content']
        Message.objects.create(
            sender=request.user,
            receiver_id=receiver_id,
            content=content
        )
        return redirect('dashboard')

    return render(request, 'books/send_message.html', {
        'users': users,
        'prefill_id': prefill_id
    })


@login_required
def user_search(request):
    query = request.GET.get('term', '')
    users = User.objects.filter(username__icontains=query).exclude(id=request.user.id)[:10]
    results = [{"id": user.id, "label": user.username} for user in users]
    return JsonResponse(results, safe=False)


@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    if request.method == "POST":
        book.delete()
        messages.success(request, "Book deleted successfully!")
    return redirect('dashboard')
