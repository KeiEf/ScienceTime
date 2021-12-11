from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormView
from .models import Product, Post, Genre, Category, Note, Field
from .forms import PostForm, EditForm, EditProductForm, ContactForm
from django.db.models import Max, Case, When, Sum, Count, Q, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
        post_list = Post.objects.all().order_by('-post_date')

        context["product_list"] = product_list
        context["post_list"] = post_list
        return context
#   get_latest_entries(self):
 #     latest_news = Post.object.filer

class PostView(ListView):
   model = Post
   template_name = 'posts.html'

   def get_context_data(self, *args, **kwargs):

        context={}
        object_list = Post.objects.filter(state="published").order_by('-post_date')
        popular_list = Post.objects.filter(state="published").order_by('-views')      

        phys_list = Post.objects.filter(category="物理と天文", state="published").order_by('-post_date')
        env_list = Post.objects.filter(category="環境", state="published").order_by('-post_date')
        health_list = Post.objects.filter(category="医療と健康", state="published").order_by('-post_date')


        cat_menu = Category.objects.all()
        cat_menu = super(PostView, self).get_context_data(*args, **kwargs)
        cat_menu_list = Category.objects.all()

        context["cat_menu"] = cat_menu
        context["cat_menu_list"] = cat_menu_list

        context["object_list"] = object_list
        context["popular_list"] = popular_list

        context["phys_list"] = phys_list
        context["env_list"] = env_list  
        context["health_list"] = health_list           
        return context

class AllPostView(ListView):
   model = Post
   template_name = 'post_all.html'

   def get_context_data(self, *args, **kwargs):
       context = {}
       cat_menu = Category.objects.all()
       popular_list = Post.objects.filter(state="published").order_by('-views')   
       popular_items = Product.objects.order_by('-views')                   
       object_list =  Post.objects.filter(state="published").order_by('-post_date')

       paginator = Paginator(object_list, 20) # num per page
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
       return context


class PostTagView(ListView):
    model = Post
    template_name ='post_all.html'

    def get_context_data(self, *args, **kwargs):
        context = {}
        cat_menu = Category.objects.all()
        popular_list = Post.objects.filter(state="published").order_by('-views')   
        popular_items = Product.objects.order_by('-views')                   
        tag_posts = Post.objects.filter(post_tags__slug=self.kwargs.get('tag_slug')).order_by('-post_date')

        paginator = Paginator(tag_posts, 20) # num per page
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
        return context



def CategoryView(request, cats):

    cat_menu = Category.objects.all()
    category_posts = Post.objects.filter(category=cats.replace('-',' '), state="published").order_by('-post_date')
    total = category_posts.count()
    popular_list = Post.objects.filter(state="published").order_by('-views')   
    popular_items = Product.objects.order_by('-views') 

    paginator = Paginator(category_posts, 20) # num per page
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
        'pages': pages  
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
        context["related_posts"] = self.object.post_tags.similar_objects()
        context["popular_list"] = popular_list
        context["popular_items"] = popular_items        
        context["cat_menu"] = cat_menu
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
                      'キャップ' : 'キャップ' }
    toy_genre = {'力学' : '力学',
                 '光と電磁気' : '光と電磁気',
                 '熱力学' : '熱力学',
                 '流体' : '流体',
                 '数学他': '数学他' ,
                 '化学': '化学'}
    merch_genre = {'トートバッグ' : 'トートバッグ',
                 'タンブラー' : 'タンブラー',
                 'マグカップ' : 'マグカップ'
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
        'pages': pages
        })


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_details.html'

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['pk'])
        product.views += 1
        product.save()
        return super().get(request, *args, **kwargs)

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

    field_list = Field.objects.filter(subj_eng=subj.replace('-',' '))
    return render(request, 'subject.html', {
        'field_list':field_list, 
        'subj':subj,
        })

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
        context["popular_items"] = popular_items
        return context

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