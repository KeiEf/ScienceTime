from django.urls import path
from . import views 
from .views import TestView, HomeView, , PostDetailView

urlpatterns = [
	path('', HomeView.as_view(), name="index"),
	path('test', TestView.as_view(), name="test"),	
    path('post/<int:pk>', PostDetailView.as_view(), name="post_detail"),
    ]

