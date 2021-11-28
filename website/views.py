from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post


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

