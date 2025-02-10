import requests
import json
import smtplib
import ssl
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import CustomPasswordChangeForm, ItemListForm, ItemForm
from .models import ItemList, Item, Profile
import logging
from django.core.exceptions import ValidationError
from django.db import IntegrityError  # Correct import for IntegrityError
from django.utils.dateparse import parse_datetime

logger = logging.getLogger(__name__)

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
    try:
        # Check if the 'Work' list already exists
        work_list, created = ItemList.objects.get_or_create(
            name='Work', user=user
        )
        if created:
            # Create default tasks for the 'Work' list if it was newly created
            Item.objects.create(title='Task 1', item_list=work_list, user=user)
            Item.objects.create(title='Task 2', item_list=work_list, user=user)
    except IntegrityError:
        logger.warning(f"Work list for user {user.username} already exists.")


@login_required
def dashboard_view(request):
    create_default_lists_and_tasks(request.user)
    items = Item.objects.filter(item_list__user=request.user)
    item_lists_exist = ItemList.objects.filter(user=request.user).exists()
    empty_state = not item_lists_exist and not items.exists()
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
        try:
            data = json.loads(request.body)
            name = data.get('name')
            deadline = data.get('deadline')
        except json.JSONDecodeError:
            return JsonResponse(
                {'success': False, 'error': 'Invalid JSON data.'}
            )

        if not name:
            return JsonResponse(
                {'success': False, 'error': 'List name is required'}
            )

        if deadline:
            try:
                deadline = parse_datetime(deadline)
                if deadline is None:
                    raise ValidationError("Invalid date format")
            except ValidationError:
                return JsonResponse(
                    {'success': False, 'error': 'Invalid date format'}
                )
        else:
            deadline = None

        item_list = ItemList(name=name, deadline=deadline, user=request.user)
        item_list.save()

        return JsonResponse({'success': True})

    return render(request, 'tasks/create_item_list.html')

@login_required
def create_item_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            title = data.get("title")
            description = data.get("description", "")
            deadline = data.get("deadline")
            item_list_id = data.get("item_list")
            new_list_name = data.get("new_list_name", "").strip()

            # Handle deadline parsing
            if deadline:
                deadline = parse_datetime(deadline)
                if not deadline:
                    return JsonResponse({"success": False, "error": "Invalid date format."})

            # Determine the correct item list
            if new_list_name:
                item_list = ItemList.objects.create(name=new_list_name, user=request.user)
            else:
                item_list = get_object_or_404(ItemList, id=item_list_id, user=request.user)

            # Create the item
            item = Item.objects.create(
                title=title,
                description=description,
                deadline=deadline,
                item_list=item_list,
                user=request.user
            )

            return JsonResponse({
                "success": True,
                "item": {
                    "id": item.id,
                    "title": item.title,
                    "list_name": item_list.name,
                    "deadline": item.deadline
                }
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

@login_required
def create_items_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            titles = data.get('titles')
            item_list_id = data.get('item_list')
            new_list_name = data.get('new_list_name')
            item_list = None

            if new_list_name:
                item_list = ItemList.objects.create(name=new_list_name, user=request.user)
            else:
                item_list = get_object_or_404(ItemList, id=item_list_id, user=request.user)

            items = []
            for title in titles:
                item = Item.objects.create(title=title, item_list=item_list, user=request.user)
                items.append({'id': item.id, 'title': item.title})
            return JsonResponse({'success': True, 'items': items})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

def item_classification_view(request):
    # Your view logic here
    return render(request, 'tasks/item_classification.html')

@csrf_exempt  # Remove this if CSRF middleware is enabled
def create_item_list(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_list_name = data.get("name", "").strip()

            if len(new_list_name) < 3:
                return JsonResponse({"success": False, "error": "List name must be at least 3 characters."}, status=400)

            # Prevent duplicate lists
            existing_list = ItemList.objects.filter(name=new_list_name, user=request.user).first()
            if existing_list:
                return JsonResponse({"success": True, "list_id": existing_list.id}, status=200)

            new_list = ItemList.objects.create(name=new_list_name, user=request.user)

            return JsonResponse({"success": True, "list_id": new_list.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON format."}, status=400)
    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)

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

@login_required
def delete_selected_lists_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_lists = data.get('selected_lists', [])
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data.'})

        if not selected_lists:
            return JsonResponse({'success': False, 'error': 'No lists selected.'})

        for list_id in selected_lists:
            item_list = get_object_or_404(ItemList, id=list_id, user=request.user)
            item_list.delete()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@csrf_exempt
@login_required
def update_priority_view(request, item_id):
    if request.method == 'POST':
        try:
            item = Item.objects.get(id=item_id, user=request.user)
            data = json.loads(request.body)
            item.priority = data.get('priority', item.priority)
            item.save()
            return JsonResponse({'success': True})
        except Item.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    

@login_required
def update_position_view(request, item_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            position_x = data.get('position_x')
            position_y = data.get('position_y')
            priority = data.get('priority')
            order = data.get('order')
            item = Item.objects.get(id=item_id, item_list__user=request.user)
            if position_x is not None:
                item.position_x = position_x
            if position_y is not None:
                item.position_y = position_y
            if priority is not None:
                item.priority = priority
            if order is not None:
                item.order = order
            item.save()
            return JsonResponse({'success': True})
        except Item.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def delete_item_view(request, item_id):
    if request.method == 'DELETE':
        try:
            item = get_object_or_404(Item, id=item_id, user=request.user)
            item.delete()
            return JsonResponse({'success': True, 'message': 'Item deleted successfully.'})
        except Item.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found.'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

@csrf_exempt
@login_required
def delete_items(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_ids = data.get('item_ids', [])
            items = Item.objects.filter(id__in=item_ids, user=request.user)
            items.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

@csrf_exempt
@login_required
def update_in_matrix(request, item_id):
    if request.method == 'POST':
        try:
            item = Item.objects.get(id=item_id, user=request.user)
            data = json.loads(request.body)
            item.in_matrix = data.get('in_matrix', item.in_matrix)
            item.save()
            return JsonResponse({'success': True})
        except Item.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

@csrf_exempt
@login_required
def remove_item_clone(request, item_id):
    if request.method == 'POST':
        try:
            item = Item.objects.get(id=item_id, user=request.user)
            item.position_x = None
            item.position_y = None
            item.priority = None
            item.in_matrix = False
            item.save()
            return JsonResponse({'success': True})
        except Item.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

@csrf_exempt
@login_required
def update_position(request, item_id):
    if request.method == 'POST':
        try:
            item = Item.objects.get(id=item_id, user=request.user)
            data = json.loads(request.body)
            item.position_x = data.get('position_x', item.position_x)
            item.position_y = data.get('position_y', item.position_y)
            item.priority = data.get('priority', item.priority)
            item.save()
            return JsonResponse({'success': True})
        except Item.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)