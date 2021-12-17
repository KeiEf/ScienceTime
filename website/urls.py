from django.urls import path
from . import views 
from .views import TestView, HomeView, ProductView, PostView, TagIndexView, ProductDetailView, PostDetailView, AddPostView, UpdatePostView, AllPostView, PostTagView, GenreView, CategoryView, ContactFormView, ContactResultView, UpdateProductView, NoteDetailView, FieldView, AllNoteView, NoteTagView


urlpatterns = [
	path('', HomeView.as_view(), name="index"),
	path('test', TestView.as_view(), name="test"),	
    path('add_post/', AddPostView.as_view(), name="add_post"),
    path('news_and_columns/edit/<int:pk>', UpdatePostView.as_view(), name="update_post"),
	path('news_and_columns', PostView.as_view(), name="posts"),   
    path('news_and_columns/tags/<slug:tag_slug>/', views.PostTagView.as_view(), name='post_by_tag'),
	path('news_and_columns/all/', AllPostView.as_view(), name='all_posts'),	
	path('post/<int:pk>', PostDetailView.as_view(), name="post_detail"),
    path('category/<str:cats>/', CategoryView, name='category'),
	path('genre/<str:gens>/', GenreView, name='genre'),	
 	path('products',  ProductView.as_view(), name="products"),
    path('products/edit/<int:pk>', UpdateProductView.as_view(), name="update_product"),
	path('products/tags/<slug:tag_slug>/', views.TagIndexView.as_view(), name='product_by_tag'),
	path('products/<int:pk>', ProductDetailView.as_view(), name="product_detail"),
	path('note/<int:pk>', NoteDetailView.as_view(), name="note_detail"),
    path('note/all/', AllNoteView.as_view(), name='all_notes'),	
    path('note/tags/<slug:tag_slug>/', views.NoteTagView.as_view(), name='note_by_tag'),
	path('subject/<str:subj>/', FieldView, name="subject"),	
	path('contact/', ContactFormView.as_view(), name='contact_form'),
    path('contact/result/', ContactResultView.as_view(), name='contact_result'),

    ]

