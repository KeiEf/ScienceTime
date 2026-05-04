from django.contrib import admin
from .models import Post, PostView, Genre, Category, Note, NoteView, Field, File, Ad, Subject, Product
from django.utils.html import format_html
from django.db import connection
from django.urls import path
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from taggit.models import Tag, TaggedItem

admin.site.register(Product)
#admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Genre)
#admin.site.register(Note)
#admin.site.register(Field)
#admin.site.register(Subject)
admin.site.register(File)
#admin.site.register(Ad)



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'id', 'author', 'category', 'post_date', "daily_views", "total_views", 'state')
    list_editable = ('author','category', 'state')
    list_filter = ('author','category', 'state') 

    def daily_views(self, obj):
        return PostView.get_view_counts(obj)["daily"]

    def weekly_views(self, obj):
        return PostView.get_view_counts(obj)["weekly"]

    def total_views(self, obj):
        return PostView.get_view_counts(obj)["total"]

    daily_views.short_description = "Daily Views"
    weekly_views.short_description = "Weekly Views"
    total_views.short_description = "Total Views"

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'author', 'post_date', "daily_views", "total_views", 'state')
    list_editable = ( 'author','state',)
    list_filter = ( 'author','field','state',)

    def daily_views(self, obj):
        return NoteView.get_view_counts(obj)["daily"]

    def weekly_views(self, obj):
        return NoteView.get_view_counts(obj)["weekly"]

    def total_views(self, obj):
        return NoteView.get_view_counts(obj)["total"]

    daily_views.short_description = "Daily Views"
    weekly_views.short_description = "Weekly Views"
    total_views.short_description = "Total Views"

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('name', 'click_count', "view_count", "get_ctr")

    def get_ctr(self, obj):
        return f"{obj.get_ctr():.2f}%"
    
    get_ctr.short_description = "Click-Through Rate (CTR)"


#@admin.register(Field)
#class FieldAdmin(admin.ModelAdmin):
#    list_display = ('field', 'subject')
#    list_editable = ('subject',)
 

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'field', 'field_eng', 'subject', 'subject_id')
    # Or specify fields explicitly:
    # list_display = [f.name for f in Field._meta.fields if f.name != 'subject_old']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'name_eng')
    #pass

class DatabaseAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('database-diagnostics/', self.admin_site.admin_view(self.database_diagnostics), 
                 name='database-diagnostics'),
        ]
        return custom_urls + urls
    
    def database_diagnostics(self, request):
        with connection.cursor() as cursor:
            # Check table structure
            cursor.execute("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'website_field'
            """)
            schema = cursor.fetchall()
            
            # Check for data inconsistencies
            cursor.execute("""
                SELECT id, subject_id, pg_typeof(subject_id) 
                FROM website_field 
                WHERE subject_id IS NULL OR pg_typeof(subject_id) != 'integer'
            """)
            bad_records = cursor.fetchall()
            
        context = {
            'schema': schema,
            'bad_records': bad_records,
            'opts': self.model._meta,
        }
        return render(request, 'admin/database_diagnostics.html', context)

admin.site.register([], DatabaseAdmin)  # Register at root URL