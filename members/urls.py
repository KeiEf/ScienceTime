from django.urls import path
from . import views
#from .views import UserRegisterView
app_name = 'members' 

urlpatterns = [
#    path('register/', UserRegisterView.as_view(), name='register'),
    path('', views.dashboard, name='dashboard'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('category/<int:category_id>/create_thread/', views.create_thread, name='create_thread'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('message/<int:message_id>/delete/', views.delete_message, name='delete_message'),
    path('message/<int:message_id>/edit/', views.edit_message, name='edit_message'),
    path('message/<int:message_id>/like/', views.toggle_like, name='toggle_like'),
    path('signup/efilism/', views.SignUpView.as_view(), name='signup'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('notification/<int:notification_id>/delete/', views.delete_notification, name='delete_notification'),
]