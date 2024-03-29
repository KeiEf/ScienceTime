from django.urls import path
from . import views 
from .views import TestView, HomeView, ManageView, ProductView, PostView, TagIndexView, ProductDetailView, PostDetailView, AddPostView, UpdatePostView, AllPostView, PostTagView, GenreView, CategoryView, ContactFormView, ContactResultView, UpdateProductView, NoteDetailView, FieldView, AllNoteView, NoteTagView, AddNoteView, UpdateNoteView, UpdateNoteContentView, UpdateNoteReferenceView, AddFieldView, UpdateFieldView,FieldDetailView,ImgUploadView, FileUploadedView,FileListView
##, TestProductDetailView
from django.views.generic import TemplateView


urlpatterns = [
	path('', HomeView.as_view(), name="index"),
	path('management', ManageView.as_view(), name="management"),	
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
    path('add_note/', AddNoteView.as_view(), name="add_note"),
    path('note/edit/<int:pk>', UpdateNoteView.as_view(), name="update_note"),
    path('note/edit_content/<int:pk>', UpdateNoteContentView.as_view(), name="update_content_note"),
    path('note/edit_reference/<int:pk>', UpdateNoteReferenceView.as_view(), name="update_reference_note"),
	path('subject/<str:subj>/', FieldView, name="subject"),	
  	path('add_field/', AddFieldView.as_view(), name="add_field"),	
	path('subject/edit/<int:pk>/', UpdateFieldView.as_view(), name="update_field"),
   	path('subject/field/<slug:slug>/', FieldDetailView.as_view(), name="field_detail"),
	path('contact/', ContactFormView.as_view(), name='contact_form'),
    path('contact/result/', ContactResultView.as_view(), name='contact_result'),
    path("api/book/<int:pk>/click/", views.api_click, name="api_click"),
    path('ads.txt', TemplateView.as_view(template_name='ads/ads.txt', content_type='text/plain')),
    path('image_upload', ImgUploadView.as_view(), name="image_upload"),
    path('file_uploaded/<int:pk>', FileUploadedView.as_view(), name="file_uploaded"),
    path('file_list', FileListView.as_view(), name="file_list"),
	##path('test_products/<int:pk>', TestProductDetailView.as_view(), name="test_product_detail"),
    ]

