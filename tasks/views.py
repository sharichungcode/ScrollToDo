import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import smtplib
import ssl

from .forms import CustomPasswordChangeForm, ItemListForm, ItemForm
from .models import ItemList, Item

def index(request):
    return render(request, 'tasks/index.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def create_default_lists_and_tasks(user):
    if not ItemList.objects.filter(user=user).exists():
        work_list = ItemList.objects.create(name='Work', user=user)
        personal_list = ItemList.objects.create(name='Personal', user=user)
        grocery_list = ItemList.objects.create(
            name='Grocery Shopping', user=user
        )

        items_to_create = [
            {'title': 'Finish project report', 'item_list': work_list},
            {'title': 'Prepare presentation', 'item_list': work_list},
            {'title': 'Call mom', 'item_list': personal_list},
            {'title': 'Buy milk', 'item_list': grocery_list},
            {'title': 'Buy bread', 'item_list': grocery_list},
        ]

        for item in items_to_create:
            Item.objects.create(**item)

@login_required
def dashboard_view(request):
    create_default_lists_and_tasks(request.user)
    items = Item.objects.filter(item_list__user=request.user)
    item_lists_exist = ItemList.objects.filter(user=request.user).exists()
    empty_state = not item_lists_exist
    return render(request, 'tasks/dashboard.html', {'items': items, 'empty_state': empty_state})

@login_required
def account_view(request):
    if request.method == 'POST':
        user = request.user
        new_email = request.POST.get('email')
        if user.email != new_email:
            user.email = new_email
            user.save()
            send_confirmation_email(user)
            messages.success(request, 'Account details updated successfully. A confirmation email has been sent to your new email address. Please check your email.')
        else:
            user.username = request.POST.get('username')
            user.save()
            messages.success(request, 'Account details updated successfully.')
        return redirect('account')
    return render(request, 'tasks/account.html')

def send_confirmation_email(user):
    subject = 'Email Address Change Confirmation'
    message = render_to_string('tasks/email_confirmation.txt', {'user': user})
    from_email = 'scrolltodo.team@gmail.com'
    recipient_list = [user.email]
    
    # Create a secure SSL context
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    # Use Django's built-in send_mail function with custom SSL context
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls(context=context)
        server.login(from_email, 'qdddxqturrjokqmu')
        server.sendmail(from_email, recipient_list, f"Subject: {subject}\n\n{message}")

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('account')
        else:
            messages.error(request, 'Failed to update password. Please try again.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'tasks/change_password.html', {'form': form})

@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('index')

@csrf_exempt
def ajax_auth_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return JsonResponse({'success': True, 'redirect_url': '/dashboard/'})
        else:
            # If user does not exist, create a new user
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username=email, email=email, password=password)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return JsonResponse({'success': True, 'redirect_url': '/dashboard/'})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid email or password'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def create_item_list_view(request):
    if request.method == 'POST':
        item_list_form = ItemListForm(request.POST)
        item_form = ItemForm(request.POST)
        if item_list_form.is_valid() and item_form.is_valid():
            item_list = item_list_form.save(commit=False)
            item_list.user = request.user
            item_list.save()
            item = item_form.save(commit=False)
            item.item_list = item_list
            item.save()
            return redirect('dashboard')
    else:
        item_list_form = ItemListForm()
        item_form = ItemForm()
    return render(request, 'tasks/create_item_list.html', {'item_list_form': item_list_form, 'item_form': item_form})

@login_required
def create_item_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item_list_id = form.cleaned_data['item_list']
            item_list = ItemList.objects.get(id=item_list_id, user=request.user)
            item.item_list = item_list
            item.save()
            messages.success(request, 'Item successfully added.')
            return redirect('dashboard')
    else:
        form = ItemForm()
    return render(request, 'tasks/create_item.html', {'form': form})

def item_classification_view(request):
    # Your view logic here
    return render(request, 'tasks/item_classification.html')

@login_required
def item_list_detail_view(request, list_id):
    item_list = get_object_or_404(ItemList, id=list_id, user=request.user)
    items = item_list.item_set.all()
    completed_items = items.filter(completed=True).count()
    total_items = items.count()
    completion_percentage = (completed_items / total_items) * 100 if total_items > 0 else 0

    if request.method == 'POST':
        if 'edit_list' in request.POST:
            form = ItemListForm(request.POST, instance=item_list)
            if form.is_valid():
                form.save()
                return redirect('item_list_detail', list_id=list_id)
        elif 'delete_list' in request.POST:
            item_list.delete()
            return redirect('dashboard')
    else:
        form = ItemListForm(instance=item_list)

    return render(request, 'tasks/item_list_detail.html', {
        'item_list': item_list,
        'items': items,
        'completion_percentage': completion_percentage,
        'form': form
    })