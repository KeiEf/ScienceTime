from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, Post, Genre, Category
from .forms import PostForm, EditForm
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
        product_list = Product.objects.all()
        post_list = Post.objects.all()

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

        phys_list = Post.objects.filter(category="physics and astronomy", state="published").order_by('-post_date')
        env_list = Post.objects.filter(category="environment", state="published").order_by('-post_date')
        health_list = Post.objects.filter(category="medical and health", state="published").order_by('-post_date')


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
   paginate_by = 20
   def get_queryset(self):
       object_list =  Post.objects.filter(state="published").order_by('-post_date')
       return object_list

class PostTagView(ListView):
    model = Post
    template_name ='post_all.html'
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        context = {}
        object_list = Post.objects.filter(post_tags__slug=self.kwargs.get('tag_slug'))
        cat_menu = Category.objects.all()
        popular_list = Post.objects.filter(state="published").order_by('-views')   
        popular_items = Product.objects.order_by('-views') 

        context["popular_list"] = popular_list
        context["popular_items"] = popular_items        
        context["cat_menu"] = cat_menu
        context["object_list"] = object_list           
        return context

def CategoryView(request, cats):
    paginate_by = 20
    cat_menu = Category.objects.all()
    category_posts = Post.objects.filter(category=cats.replace('-',' '), state="published")
    total = category_posts.count()
    popular_list = Post.objects.filter(state="published").order_by('-views')   
    popular_items = Product.objects.order_by('-views')                   
    return render(request, 'category.html', {
        'cats':cats.title().replace('-',' '), 
        'category_posts':category_posts, 
        'cat_menu':cat_menu,
        'popular_list': popular_list,
        'popular_items': popular_items   
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
        context["related_posts"] = self.object.post_tags.similar_objects()[:3]
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

        fashion_list = Product.objects.filter(genre="fashion").order_by('-post_date')
        toy_list = Product.objects.filter(genre="toy").order_by('-post_date')
        merch_list = Product.objects.filter(genre="merch").order_by('-post_date')

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
    paginate_by = 20
    genre_menu = Genre.objects.all()
    genre_posts = Product.objects.filter(genre=gens.replace('-',' ')) 
    popular_items = Product.objects.order_by('-views') 
    fashion_genre = {'T-shirts' : 'T-shirts', 'hoodie': 'hoodie' }
    toy_genre = {'mechanics' : 'mechanics', 'maths_and_others': 'maths_and_others' }             
    return render(request, 'genre.html', {
        'gens':gens.title().replace('-',' '), 
        'genre_posts':genre_posts, 
        'genre_menu':genre_menu,
        'popular_items': popular_items,
        'fashion_genre': fashion_genre,
        'toy_genre': toy_genre        
        })

'''
   def get_context_data(self):
        context={}
        toy_list = Product.objects.filter(category="toy")
        T_list = Product.objects.filter(category="T-shirts")

        context["toy_list"] = toy_list
        context["T_list"] = T_list
        return context
'''


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

