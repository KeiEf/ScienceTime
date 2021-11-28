from django.urls import path
#from . import views 
from .views import TestView, HomeView##, ProductView, PostView, TagIndexView, ProductDetailView, PostDetailView, AddPostView, UpdatePostView, AllPostView, PostTagView, GenreView, CategoryView

urlpatterns = [
	path('', HomeView.as_view(), name="index"),
	path('test', TestView.as_view(), name="test"),	
	]

