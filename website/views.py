from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, Post ##, Genre, Category
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
