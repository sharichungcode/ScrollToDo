"""
URL configuration for scrolltodo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from tasks import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('account/', views.account_view, name='account'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('ajax-auth/', views.ajax_auth_view, name='ajax_auth'),
    path(
        'create_item_list/', 
        views.create_item_list_view, 
        name='create_item_list'
    ),
    path('create_item/', views.create_item_view, name='create_item'),
    path('create_items/', views.create_items_view, name='create_items'),
    path(
        'item_classification/', views.item_classification_view, 
        name='item_classification'
    ),
    path(
        'item_list/<int:list_id>/', views.item_list_detail_view, 
        name='item_list_detail'
    ),
    path(
        'delete-selected-lists/', views.delete_selected_lists_view, 
        name='delete_selected_lists'
    ),
    path(
        'delete-item/<int:item_id>/', views.delete_item_view, 
        name='delete_item'
    ),
    path('delete_items/', views.delete_items, name='delete_items'),
    path(
        'update-priority/<int:item_id>/', views.update_priority_view, 
        name='update_priority'
    ),
    path(
        'update-position/<int:item_id>/', views.update_position_view, 
        name='update_position'
    ),
    path(
        'update-in-matrix/<int:item_id>/', views.update_in_matrix, 
        name='update_in_matrix'
    ),
    path(
        'remove-item-clone/<int:item_id>/', views.remove_item_clone, 
        name='remove_item_clone'
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
