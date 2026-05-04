from django.urls import path
from . import views 
from django.views.generic import TemplateView
from .views import HomeView, admin_dashboard, ad_click, \
                   add_note, NoteDetailView, add_post, AllNoteView, TagNoteView, \
                   PostDetailView, AllPostView, \
                   SubjectDetailView, FieldDetailView
                    #, #, FieldView, 

urlpatterns = [
	path('', HomeView.as_view(), name="index"),
    path('ads.txt', TemplateView.as_view(template_name='ads.txt', content_type='text/plain')),  
	path('note/<int:pk>', NoteDetailView.as_view(), name="note_detail"),
    path('note/all/', AllNoteView.as_view(), name='all_notes'),
    path('note/tag/<slug:tag_slug>/', TagNoteView.as_view(), name='notes_by_tag'),
    path('note/add/', add_note, name='add_note'),
    path('note/edit/<int:pk>', views.edit_note, name="update_note"),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path("ad_click/<int:ad_id>/", ad_click, name="ad_click"),
	path('post/<int:pk>', PostDetailView.as_view(), name="post_detail"),
    path('post/add/', add_post, name='add_post'),
    path('post/edit/<int:pk>', views.edit_post, name="update_post"),
    path('post/post_top/', views.post_top, name='post_top'),
    path('post/all/', AllPostView.as_view(), name='all_posts'),
	path('subject/<int:pk>/', SubjectDetailView.as_view(), name="subject"),	
	path('field/<int:pk>', FieldDetailView.as_view(), name="field_detail"),
	path('field/edit/<int:pk>', views.edit_field, name="update_field"),
]




'''
urlpatterns = [

	path('management', ManageView.as_view(), name="management"),	
	#path('test', TestView.as_view(), name="test"),	
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

    path('note/tags/<slug:tag_slug>/', views.NoteTagView.as_view(), name='note_by_tag'),
    path('add_note/', AddNoteView.as_view(), name="add_note"),
    path('note/edit_content/<int:pk>', UpdateNoteContentView.as_view(), name="update_content_note"),
    path('note/edit_reference/<int:pk>', UpdateNoteReferenceView.as_view(), name="update_reference_note"),

  	path('add_field/', AddFieldView.as_view(), name="add_field"),	
	path('subject/edit/<int:pk>/', UpdateFieldView.as_view(), name="update_field"),

	path('contact/', ContactFormView.as_view(), name='contact_form'),
    path('contact/result/', ContactResultView.as_view(), name='contact_result'),
    #path('ads.txt', TemplateView.as_view(template_name='ads/ads.txt', content_type='text/plain')),
    path('image_upload', ImgUploadView.as_view(), name="image_upload"),
    path('file_uploaded/<int:pk>', FileUploadedView.as_view(), name="file_uploaded"),
    path('file_list', FileListView.as_view(), name="file_list"),
    #path('ads/', views.ad_list, name='ad_list'),
    #path('ads/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    #path('ads/new/', views.ad_create, name='ad_create'),
    #path('ads/<int:ad_id>/edit/', views.ad_update, name='ad_update'),
    #path('ads/<int:ad_id>/delete/', views.ad_delete, name='ad_delete'),
    #path("ad_click/<int:ad_id>/", ad_click, name="ad_click"),
	##path('test_products/<int:pk>', TestProductDetailView.as_view(), name="test_product_detail"),
    ]

'''