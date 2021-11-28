from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, Post, Genre, Category


# Create your views here.

class TestView(ListView):
   model = Post
   template_name = 'test.html'


class HomeView(ListView):
   model = Post
   template_name = 'index.html'

   def get_context_data(self):
        context={}
        post_list = Post.objects.all()
        context["post_list"] = post_list
        return context


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

