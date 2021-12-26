from django.contrib import admin
from .models import Post, Product, Genre, Category, Note, Field, Book

admin.site.register(Product)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Note)
admin.site.register(Field)
admin.site.register(Book)