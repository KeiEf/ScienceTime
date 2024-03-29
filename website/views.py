from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormView
from .models import Product, Post, Genre, Category, Note, Field, Book, File
from .forms import PostForm, EditForm, EditProductForm, ContactForm,PostNoteForm, EditNoteForm, EditNoteContentForm,  EditNoteReferenceForm, AddFieldForm,EditFieldForm, ImgUpForm

from django.db.models import Max, Case, When, Sum, Count, Q, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse

# Create your views here.

class TestView(ListView):
   model = Post
   template_name = 'test.html'


class HomeView(ListView):
   model = Post
   template_name = 'index.html'

   def get_context_data(self):
        context={}
        product_list = Product.objects.all().order_by('-views')
        post_list = Post.objects.filter(state="published").order_by('-post_date')

        context["product_list"] = product_list
        context["post_list"] = post_list
        return context
#   get_latest_entries(self):
 #     latest_news = Post.object.filer


class ManageView(ListView):
   model = Post
   template_name = './manage/manage.html'


   def get_context_data(self, *args, **kwargs):
       context = {}

       q_word = self.request.GET.get('query')
       sort = self.request.GET.get('sort')
       if sort == "view":
          object_list =  Note.objects.filter(state="published").order_by('-views')
       elif sort == "inv_view":
          object_list =  Note.objects.filter(state="published").order_by('views')
       elif sort == "date":
          object_list =  Note.objects.filter(state="published").order_by('-post_date')
       elif sort == "inv_date":
          object_list =  Note.objects.filter(state="published").order_by('post_date')
       elif sort == "all":
          object_list =  Note.objects.all.order_by('post_date') 
       elif sort == "private":
          object_list =  Note.objects.filter(state="private").order_by('post_date')         

       elif q_word:
          object_list = Note.objects.filter(
                Q(title__icontains=q_word) 
                | Q(note_tags__name__icontains=q_word)  | Q(content1__icontains=q_word) 
                | Q(content2__icontains=q_word) 
                | Q(quotes__icontains=q_word) | Q(reference__icontains=q_word) 
                | Q(subject__icontains=q_word) | Q(intro__icontains=q_word)
                | Q(abstract__icontains=q_word) | Q(caption__icontains=q_word)
                ).distinct()

       else:        
          object_list =  Note.objects.filter(state="private").order_by('-post_date')

       paginator = Paginator(object_list, 10) # num per page
       page = self.request.GET.get('page', 1)
       try:
           pages = paginator.page(page)
       except PageNotAnInteger:
    	     pages = paginator.page(1)
       except EmptyPage:
           pages = paginator.page(1)

       popular_list = Post.objects.filter(state="published").order_by('-views')   
       popular_items = Product.objects.all().order_by('-views') 
       context["popular_items"] = popular_items        
       context["pages"] = pages
       context["popular_list"] = popular_list
       context["sort"] = sort
       return context

class PostView(ListView):
   model = Post
   template_name = 'posts.html'

   def get_context_data(self, *args, **kwargs):

        context={}
        object_list = Post.objects.filter(state="published").order_by('-post_date')
        popular_list = Post.objects.filter(state="published").order_by('-views')      
        popular_items = Product.objects.order_by('-views')

        phys_list = Post.objects.filter(category="物理と天文", state="published").order_by('-post_date')
        env_list = Post.objects.filter(category="環境", state="published").order_by('-post_date')
        health_list = Post.objects.filter(category="医療と健康", state="published").order_by('-post_date')
        bio_list = Post.objects.filter(category="生物", state="published").order_by('-post_date')
        mind_list = Post.objects.filter(category="脳と心", state="published").order_by('-post_date')
        anth_list = Post.objects.filter(category="人類学", state="published").order_by('-post_date')
        math_list = Post.objects.filter(category="数学", state="published").order_by('-post_date')

        cat_menu = Category.objects.all()
        cat_menu = super(PostView, self).get_context_data(*args, **kwargs)
        cat_menu_list = Category.objects.all()

        context["cat_menu"] = cat_menu
        context["cat_menu_list"] = cat_menu_list

        context["object_list"] = object_list
        context["popular_list"] = popular_list
        context["popular_items"] = popular_items  

        context["phys_list"] = phys_list
        context["env_list"] = env_list  
        context["health_list"] = health_list 
        context["bio_list"] = bio_list
        context["mind_list"] = mind_list  
        context["anth_list"] = anth_list 
        context["math_list"] = math_list           
        return context

class AllPostView(ListView):
   model = Post
   template_name = 'post_all.html'

   def get_context_data(self, *args, **kwargs):
       context = {}
       cat_menu = Category.objects.all()
       popular_list = Post.objects.filter(state="published").order_by('-views')   
       popular_items = Product.objects.order_by('-views')
       
       q_word = self.request.GET.get('query')
       sort = self.request.GET.get('sort')
       if sort == "view":
          object_list =  Post.objects.filter(state="published").order_by('-views')
       elif sort == "inv_view":
          object_list =  Post.objects.filter(state="published").order_by('views')
       elif sort == "date":
          object_list =  Post.objects.filter(state="published").order_by('-post_date')
       elif sort == "inv_date":
          object_list =  Post.objects.filter(state="published").order_by('post_date')
       elif sort == "private":
          object_list =  Post.objects.filter(state="private").order_by('-post_date')

       elif q_word:
          object_list = Post.objects.filter(
                Q(title__icontains=q_word) | Q(author__username__icontains=q_word) 
                | Q(post_tags__name__icontains=q_word)  | Q(content__icontains=q_word) 
                ).distinct()
       else:        
          object_list =  Post.objects.filter(state="published").order_by('-post_date')

       paginator = Paginator(object_list, 30) # num per page
       page = self.request.GET.get('page', 1)
       try:
         	pages = paginator.page(page)
       except PageNotAnInteger:
    	    pages = paginator.page(1)
       except EmptyPage:
          	pages = paginator.page(1)

       context["popular_list"] = popular_list
       context["popular_items"] = popular_items        
       context["cat_menu"] = cat_menu
       context["pages"] = pages
       context["sort"] = sort
       return context


class PostTagView(ListView):
    model = Post
    template_name ='post_all.html'

    def get_context_data(self, *args, **kwargs):
        context = {}
        cat_menu = Category.objects.all()
        popular_list = Post.objects.filter(state="published").order_by('-views')   
        popular_items = Product.objects.order_by('-views')

        q_word = self.request.GET.get('query')
        sort = self.request.GET.get('sort')
        if sort == "view":
          tag_posts = Post.objects.filter(post_tags__slug=self.kwargs.get('tag_slug')).order_by('-views')
        elif sort == "inv_view":
          tag_posts = Post.objects.filter(post_tags__slug=self.kwargs.get('tag_slug')).order_by('views')
        elif sort == "date":
          tag_posts = Post.objects.filter(post_tags__slug=self.kwargs.get('tag_slug')).order_by('-post_date')
        elif sort == "inv_date":
          tag_posts = Post.objects.filter(post_tags__slug=self.kwargs.get('tag_slug')).order_by('post_date')

        elif q_word:
          tag_posts = Post.objects.filter(
                Q(title__icontains=q_word) | Q(author__username__icontains=q_word) 
                | Q(post_tags__name__icontains=q_word)  | Q(content__icontains=q_word) 
                ).distinct()

        else: 
          tag_posts = Post.objects.filter(post_tags__slug=self.kwargs.get('tag_slug')).order_by('-post_date')

        paginator = Paginator(tag_posts, 30) # num per page
        page = self.request.GET.get('page', 1)
        try:
         	pages = paginator.page(page)
        except PageNotAnInteger:
    	    pages = paginator.page(1)
        except EmptyPage:
          	pages = paginator.page(1)

        context["popular_list"] = popular_list
        context["popular_items"] = popular_items        
        context["cat_menu"] = cat_menu
        context["pages"] = pages
        context["sort"] = sort
        return context


def CategoryView(request, cats):

    cat_menu = Category.objects.all()
    q_word = request.GET.get('query')
    sort = request.GET.get('sort')
    if sort == "view":
       category_posts = Post.objects.filter(category=cats.replace('-',' '), state="published").order_by('-views')
    elif sort == "inv_view":
       category_posts = Post.objects.filter(category=cats.replace('-',' '), state="published").order_by('views')
    elif sort == "date":
       category_posts = Post.objects.filter(category=cats.replace('-',' '), state="published").order_by('-post_date')
    elif sort == "inv_date":
       category_posts = Post.objects.filter(category=cats.replace('-',' '), state="published").order_by('post_date')

    elif q_word:
       category_posts = Post.objects.filter(
                Q(title__icontains=q_word) | Q(author__username__icontains=q_word) 
                | Q(post_tags__name__icontains=q_word)  | Q(content__icontains=q_word) 
                ).distinct()

    else:  
       category_posts = Post.objects.filter(category=cats.replace('-',' '), state="published").order_by('-post_date')

    popular_list = Post.objects.filter(state="published").order_by('-views')   
    popular_items = Product.objects.order_by('-views') 

    paginator = Paginator(category_posts, 30) # num per page
    page = request.GET.get('page', 1)

    try:
    	pages = paginator.page(page)
    except PageNotAnInteger:
    	pages = paginator.page(1)
    except EmptyPage:
    	pages = paginator.page(1)

    return render(request, 'category.html', {
        'cats':cats.title().replace('-',' '), 
        'category_posts':category_posts, 
        'cat_menu':cat_menu,
        'popular_list': popular_list,
        'popular_items': popular_items,
        'pages': pages,
        'sort': sort
        })


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_details.html'

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        post.views += 1
        post.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        popular_list = Post.objects.filter(state="published").order_by('-views')   
        popular_items = Product.objects.order_by('-views') 
        related_entries = Post.objects.filter(state="published", post_tags__slug__in=list(self.object.post_tags.values_list('slug', flat=True))).exclude(id=self.object.id).distinct()
        related_books = Book.objects.filter(book_tags__slug__in=list(self.object.post_tags.values_list('slug', flat=True))).distinct().order_by('-views')
        context["related_books"] = related_books
        context["related_posts"] = self.object.post_tags.similar_objects()
        context["popular_list"] = popular_list
        context["popular_items"] = popular_items        
        context["cat_menu"] = cat_menu
        context['related_entries'] = related_entries
        return context

class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'

    def form_valid(self, form):
        firma = form.save()
        return redirect('post_detail', firma.pk)    

class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'

    def get_success_url(self):
        #messages.success(self.request, '投稿を編集しました。')
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})

###########

class ProductView(ListView):
   model = Product
   template_name = 'products.html'
   paginate_by = 30

   def get_context_data(self, *args, **kwargs):

        context={}
        object_list = Product.objects.all().order_by('-post_date')
        popular_list = Product.objects.all().order_by('-views')      

        fashion_list = Product.objects.filter(genre="ファッション").order_by('-views')
        toy_list = Product.objects.filter(genre="おもちゃ").order_by('-views')
        merch_list = Product.objects.filter(genre="雑貨").order_by('-views')

        genre_menu = Genre.objects.all()
      #  genre_menu_list = Category.objects.all()

        context["genre_menu"] = genre_menu
        context["object_list"] = object_list
        context["popular_list"] = popular_list

        context["fashion_list"] = fashion_list
        context["toy_list"] = toy_list 
        context["merch_list"] = merch_list             
        return context


def GenreView(request, gens):

    sort = request.GET.get('sort')

    if sort:
       genre_posts = Product.objects.filter(sub_genre=sort)
    else:        
       genre_posts = Product.objects.filter(genre=gens.replace('-',' ')).order_by('-views')

    if sort == 'all':
       genre_posts = Product.objects.filter(genre=gens.replace('-',' ')).order_by('-views')

    genre_menu = Genre.objects.all()
    popular_items = Product.objects.order_by('-views') 
    fashion_genre = {'Tシャツ' : 'Tシャツ', 
                      'フーディ': 'フーディ',
                      'キャップ' : 'キャップ' 
                      }
    toy_genre = {'力学' : '力学',
                 '光と電磁気' : '光と電磁気',
                 '熱力学' : '熱力学',
                 '流体' : '流体',
                 '数学他': '数学他' ,
                 '化学': '化学'}
    merch_genre = {'トートバッグ' : 'トートバッグ',
                 'タンブラー' : 'タンブラー',
                 'マグカップ' : 'マグカップ',
                 'インテリア' : 'インテリア',
                 '文房具' : '文房具',
                  }                 

    paginator = Paginator(genre_posts, 9) # num per page
    page = request.GET.get('page', 1)

    try:
    	pages = paginator.page(page)
    except PageNotAnInteger:
    	pages = paginator.page(1)
    except EmptyPage:
    	pages = paginator.page(1)
               
    return render(request, 'genre.html', {
        'gens':gens.title().replace('-',' '), 
        'genre_posts':genre_posts, 
        'genre_menu':genre_menu,
        'popular_items': popular_items,
        'fashion_genre': fashion_genre,
        'toy_genre': toy_genre,
        'merch_genre': merch_genre,        
        'pages': pages,
        'sort': sort
        })


##class ProductDetailView(DetailView):
##   model = Product
##    template_name = 'product_details.html'

##    def get(self, request, *args, **kwargs):
##        product = get_object_or_404(Product, id=self.kwargs['pk'])
##        product.views += 1
##        product.save()
##        return super().get(request, *args, **kwargs)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_details.html'

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['pk'])
        product.views += 1
        product.save()
        return super().get(request, *args, **kwargs)
        
    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        popular_list = Post.objects.filter(state="published").order_by('-views')
        related_product = Product.objects.filter(tags__slug__in=list(self.object.tags.values_list('slug', flat=True))).exclude(id=self.object.id).distinct()
        popular_items = Product.objects.all().order_by('-views') 
        context["popular_items"] = popular_items        
        context["popular_list"] = popular_list
        context["related_product"] = related_product
        return context

class TagIndexView(ListView):
    model = Product
    template_name ='genre.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(tags__slug=self.kwargs.get('tag_slug'))


class UpdateProductView(UpdateView):
    model = Product
    form_class = EditProductForm
    template_name = 'update_product.html'

    def get_success_url(self):
        #messages.success(self.request, '投稿を編集しました。')
        return reverse_lazy('product_detail', kwargs={'pk': self.kwargs['pk']})


#### Note 


def FieldView(request, subj):

    field_list = Field.objects.filter(subj_eng=subj.replace('-',' ')).order_by('ordering')
    return render(request, 'subject.html', {
        'field_list':field_list, 
        'subj':subj,
        })

class FieldDetailView(DetailView):
    model = Field
    template_name = 'field_details.html'
  #  slug_url_kwarg = 'slug_field_eng'
   # slug_field = 'field_eng'

 #   def subject(self, request, *args, **kwargs):
 #     field = get_object_or_404(Field, field_eng=self.kwargs['field_eng'])
 #     subj = field.subj_eng
 #     return render(request, 'field_details.html', {
 #       'subj':subj,
 #       }) 

    def get_context_data(self, *args, **kwargs):
        context = super(FieldDetailView, self).get_context_data(*args, **kwargs)
        popular_list = Post.objects.filter(state="published").order_by('-views')   
        popular_items = Product.objects.order_by('-views') 
        context["popular_list"] = popular_list
        context["popular_items"] = popular_items        
        return context

   # def get(self, request, *args, **kwargs):
     #   field = get_object_or_404(Field, field_eng=self.kwargs['field_eng'])
   #     field = get_object_or_404(Field, field_eng=self.kwargs['field_eng'])
    #field = field.field_eng.replace(' ', '_')
#        eng = field.field_eng
   #     return super().get(request, *args, **kwargs)



class NoteDetailView(DetailView):
    model = Note
    template_name = 'note_details.html'
    
    def get(self, request, *args, **kwargs):
        note = get_object_or_404(Note, id=self.kwargs['pk'])
        note.views += 1
        note.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(NoteDetailView, self).get_context_data(*args, **kwargs)
        popular_items = Product.objects.all().order_by('-views') 
        related_books = Book.objects.filter(book_tags__slug__in=list(self.object.note_tags.values_list('slug', flat=True))).distinct().order_by('-views')
        context["popular_items"] = popular_items
        context["related_books"] = related_books
        return context


class AllNoteView(ListView):
   model = Note
   template_name = 'note_all.html'

   def get_context_data(self, *args, **kwargs):
       context = {}

       q_word = self.request.GET.get('query')
       sort = self.request.GET.get('sort')
       if sort == "view":
          object_list =  Note.objects.filter(state="published").order_by('-views')
       elif sort == "inv_view":
          object_list =  Note.objects.filter(state="published").order_by('views')
       elif sort == "date":
          object_list =  Note.objects.filter(state="published").order_by('-post_date')
       elif sort == "inv_date":
          object_list =  Note.objects.filter(state="published").order_by('post_date')
       elif sort == "all":
          object_list =  Note.objects.all.order_by('post_date') 
       elif sort == "private":
          object_list =  Note.objects.filter(state="private").order_by('post_date')         

       elif q_word:
          object_list = Note.objects.filter(
                Q(title__icontains=q_word) 
                | Q(note_tags__name__icontains=q_word)  | Q(content1__icontains=q_word) 
                | Q(content2__icontains=q_word) 
                | Q(quotes__icontains=q_word) | Q(reference__icontains=q_word) 
                | Q(subject__icontains=q_word) | Q(intro__icontains=q_word)
                | Q(abstract__icontains=q_word) | Q(caption__icontains=q_word)
                ).distinct()

       else:        
          object_list =  Note.objects.filter(state="published").order_by('-post_date')


       paginator = Paginator(object_list, 30) # num per page
       page = self.request.GET.get('page', 1)
       try:
           pages = paginator.page(page)
       except PageNotAnInteger:
    	     pages = paginator.page(1)
       except EmptyPage:
           pages = paginator.page(1)

       popular_list = Post.objects.filter(state="published").order_by('-views')   
       popular_items = Product.objects.all().order_by('-views') 
       context["popular_items"] = popular_items        
       context["pages"] = pages
       context["popular_list"] = popular_list
       context["sort"] = sort
       return context


class NoteTagView(ListView):
    model = Note
    template_name ='note_all.html'

    def get_context_data(self, *args, **kwargs):
        context = {}
        cat_menu = Category.objects.all()
        popular_list = Post.objects.filter(state="published").order_by('-views')   
        popular_items = Product.objects.order_by('-views')
        
        q_word = self.request.GET.get('query')
        sort = self.request.GET.get('sort')
        if sort == "view":
          tag_posts = Note.objects.filter(note_tags__slug=self.kwargs.get('tag_slug')).order_by('-views')
        elif sort == "inv_view":
          tag_posts = Note.objects.filter(note_tags__slug=self.kwargs.get('tag_slug')).order_by('views')
        elif sort == "date":
          tag_posts = Note.objects.filter(note_tags__slug=self.kwargs.get('tag_slug')).order_by('-post_date')
        elif sort == "inv_date":
          tag_posts = Note.objects.filter(note_tags__slug=self.kwargs.get('tag_slug')).order_by('post_date')

        elif q_word:
          object_list = Note.objects.filter(
                Q(title__icontains=q_word) 
                | Q(note_tags__name__icontains=q_word)  | Q(content1__icontains=q_word) 
                | Q(content2__icontains=q_word) 
                | Q(quotes__icontains=q_word) | Q(reference__icontains=q_word) 
                | Q(subject__icontains=q_word) | Q(intro__icontains=q_word)
                | Q(abstract__icontains=q_word) | Q(caption__icontains=q_word)
                ).distinct()

        else: 
          tag_posts = Note.objects.filter(note_tags__slug=self.kwargs.get('tag_slug')).order_by('-post_date')

        paginator = Paginator(tag_posts, 30) # num per page
        page = self.request.GET.get('page', 1)
        try:
         	pages = paginator.page(page)
        except PageNotAnInteger:
    	    pages = paginator.page(1)
        except EmptyPage:
          	pages = paginator.page(1)

        context["popular_list"] = popular_list
        context["popular_items"] = popular_items        
        context["cat_menu"] = cat_menu
        context["pages"] = pages
        context["sort"] = sort
        return context


class AddNoteView(CreateView):
    model = Note
    form_class = PostNoteForm
    template_name = 'add_note.html'

    def form_valid(self, form):
        firma = form.save()
        return redirect('note_detail', firma.pk)    

class UpdateNoteView(UpdateView):
    model = Note
    form_class = EditNoteForm
    template_name = 'update_note.html'

    def get_success_url(self):
        #messages.success(self.request, '投稿を編集しました。')
        return reverse_lazy('note_detail', kwargs={'pk': self.kwargs['pk']})

class UpdateNoteContentView(UpdateView):
    model = Note
    form_class = EditNoteContentForm
    template_name = 'update_note.html'

    def get_success_url(self):
        #messages.success(self.request, '投稿を編集しました。')
        return reverse_lazy('note_detail', kwargs={'pk': self.kwargs['pk']})

class UpdateNoteReferenceView(UpdateView):
    model = Note
    form_class = EditNoteReferenceForm
    template_name = 'update_note.html'

    def get_success_url(self):
        #messages.success(self.request, '投稿を編集しました。')
        return reverse_lazy('note_detail', kwargs={'pk': self.kwargs['pk']})

class AddFieldView(CreateView):
    model = Field
    form_class = AddFieldForm
    template_name = 'add_field.html'

    def get_success_url(self):
        #messages.success(self.request, '投稿を編集しました。')
        return reverse_lazy('all_notes')


class UpdateFieldView(UpdateView):
    model = Field
    form_class = EditFieldForm
    template_name = 'update_field.html'

    def get_success_url(self):
        #messages.success(self.request, '投稿を編集しました。')
        return reverse_lazy('all_notes')

#### Contact form ####

class ContactFormView(FormView):
    template_name = 'contact/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_result')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class ContactResultView(TemplateView):
    template_name = 'contact/contact_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success'] = "お問い合わせは正常に送信されました。"
        return context


def api_click(request, pk):

    book = Book.objects.get(id=pk)
    book.views += 1
    book.save()
    return JsonResponse({"views":book.views})



#############


class ImgUploadView(CreateView):
    model = File
    template_name = 'image_upload.html'
    form_class = ImgUpForm

    def form_valid(self, form):
        firma = form.save()
        return redirect('file_uploaded', firma.pk)

class FileUploadedView(DetailView):
    model = File
    template_name = 'file_uploaded.html'

    def get(self, request, *args, **kwargs):
       file = get_object_or_404(File, id=self.kwargs['pk'])
       return super().get(request, *args, **kwargs)

class FileListView(ListView):
    model = File
    template_name = 'file_list.html'
    def get_context_data(self):
        context={}
        object_list = File.objects.filter(uploader=self.request.user).order_by('-post_date')
        paginator = Paginator(object_list, 5) # num per page
        page = self.request.GET.get('page', 1)

        try:
         	pages = paginator.page(page)
        except PageNotAnInteger:
    	    pages = paginator.page(1)
        except EmptyPage:
          	pages = paginator.page(1)

        context["pages"] = pages
        return context
###


