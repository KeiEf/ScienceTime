
import random
from django.db import models
from django.db.models import Sum, OuterRef, Subquery, Value, F, Q
from django.db.models.functions import Coalesce
from taggit.models import Tag
from django.utils.timezone import now
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.views.generic import ListView, DetailView
from .models import Post, PostView, Note, NoteView, Subject, Field, Ad, AdClick
from .forms import AddNoteForm, EditNoteForm, AddPostForm, EditPostForm, EditFieldForm

#==============
class HomeView(ListView):
#==============
   model = Post
   template_name = 'index.html'
   #template_name = 'test.html'

@staff_member_required
def admin_dashboard(request):
    total_notes = Note.objects.count()
    published_notes = Note.objects.filter(state="published").count()
    draft_notes = Note.objects.filter(state="draft").count()
    total_users = User.objects.count()

    context = {
        "total_notes": total_notes,
        "published_notes": published_notes,
        "draft_notes": draft_notes,
        "total_users": total_users,
    }

    return render(request, "manage/admin_dashboard.html", context)




#*** Note ***
#==============
class NoteDetailView(DetailView):
#==============
    model = Note
    template_name = 'notes/note_details.html'

    def get(self, request, *args, **kwargs):
        note = get_object_or_404(Note, id=self.kwargs['pk'])

        # Update daily views
        today = now().date()
        note_view, created = NoteView.objects.get_or_create(note=note, date=today)
        if not created:
            note_view.count = F('count') + 1
            note_view.save()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(NoteDetailView, self).get_context_data(*args, **kwargs)
        note = self.get_object()

        context["tags"] = note.tags.all()  # Show tags for the note
        # Get the tags associated with the current note
        tags = note.tags.all() 

        context["tags"] = tags
        context["view_counts"] = NoteView.get_view_counts(note)

        def get_ad_by_shape(shape, tags):
            ads = Ad.objects.filter(shape=shape, tags__in=tags).order_by('-click_count')

            if ads.exists():
                # Find the maximum click_count among the filtered ads
                max_click_count = ads.first().click_count

                # Filter ads with the maximum click_count
                top_ads = ads.filter(click_count=max_click_count)

                # Randomly select one ad from the top ads
                ad = random.choice(top_ads)
            else:
                # Fallback: Pick a random ad of the same shape if no matching tags
                ad = Ad.objects.filter(shape=shape).order_by('?').first()

            if ad:  # Ensure only the displayed ad is counted
                ad.increment_view_count()

            return ad
        
        # Get one ad per size
        context["ad_v"] = get_ad_by_shape('vertical', tags)
        context["ad_h"] = get_ad_by_shape('horizontal', tags)
        context["ad_q"] = get_ad_by_shape('square', tags)

        return context

@login_required
def add_note(request):
    if request.method == 'POST':
        form = AddNoteForm(request.POST, request.FILES)
        if form.is_valid():
            # commit=Falseで一時保存。
            # この時点で、フォームから送信された author (管理者が選んだユーザー) が note に入ります。
            note = form.save(commit=False)
            
            # 【権限チェック】管理権限がない一般ユーザーの場合は、強制的に自分のIDで上書きする
            if not request.user.is_superuser:
                note.author = request.user
                
            note.save()
            form.save_m2m()  # TaggableManager (tags) の保存に必須
            
            messages.success(request, "Note created successfully!")
            return redirect(note.get_absolute_url())
        else:
            messages.error(request, "Please correct the errors below.")
            print("FORM ERRORS:", form.errors)  # デバッグ用
    else:
        form = AddNoteForm()
    
    return render(request, 'notes/add_note.html', {
        'form': form,
        'title': 'Add New Note',
        'edit_mode': False,
        # 'current_user' は削除しました（Djangoテンプレートには常に {{ user }} が存在するため）
    })

@login_required
def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk)

    # （オプション）作成者本人か管理者以外は編集画面を開けないようにする
    if note.author != request.user and not request.user.is_superuser:
        raise PermissionDenied
    
    if request.method == 'POST':
        original_author = note.author
        
        form = EditNoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            updated_note = form.save(commit=False)
            
            # 【重要】管理権限がないユーザーからのPOSTの場合は、authorを元に戻す（改ざん防止）
            if not request.user.is_superuser:
                updated_note.author = original_author
                
            updated_note.save()
            form.save_m2m() # TagsなどMany-to-Manyフィールドがある場合は必須
            return redirect(updated_note.get_absolute_url())
    else:
        form = EditNoteForm(instance=note)
        
    return render(request, 'notes/update_note.html', {
        'form': form,
        'now': now(),
        'edit_mode': True,
        'title': f'Edit {note.title}'
    })

#==============
class AllNoteView(ListView):
#==============

    model = Note
    template_name = "notes/note_all.html"  # Template to be used
    context_object_name = "notes"
    paginate_by = 20  # Default pagination

    def get_queryset(self):

        if self.request.user.is_staff or self.request.user.is_superuser:
            # Admins can see both published and draft notes
            queryset = self.model.objects.filter(state__in=["published", "draft"])
        else:
            # Regular users only see published notes
            queryset = self.model.objects.filter(state="published")


        today = now().date()

        # Aggregate total views per note
        total_views = NoteView.objects.filter(note=OuterRef('pk')).values('note').annotate(
            total=Coalesce(Sum('count'), Value(0))  # Replace None with 0
        ).values('total')

        # Aggregate today's views per note
        daily_views = NoteView.objects.filter(note=OuterRef('pk'), date=today).values('note').annotate(
            daily=Coalesce(Sum('count'), Value(0))  # Replace None with 0
        ).values('daily')

        # Annotate Note model
        queryset = queryset.annotate(
            total_views=Coalesce(Subquery(total_views), Value(0)),
            daily_views=Coalesce(Subquery(daily_views), Value(0))
        )

        # Search functionality (title, content, and tags)
        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(field__field__icontains=search_query) | 
                Q(caption__icontains=search_query) | 
                Q(quotes__icontains=search_query) | 
                Q(abstract__icontains=search_query) | 
                Q(intro__icontains=search_query) | 
                Q(content__icontains=search_query) | 
                Q(reference__icontains=search_query) | 
                Q(tags__name__icontains=search_query)  
            ).distinct()

        # Sorting logic
        order_by = self.request.GET.get("order_by", "date_desc")
        order_mapping = {
            "date_desc": "-post_date",
            "date_asc": "post_date",
            "views_desc": "-total_views",  # Sort by total views (most first)
            "views_asc": "total_views",    # Sort by total views (least first)
            "daily_views_desc": "-daily_views",  # Sort by today's views (most first)
            "daily_views_asc": "daily_views",    # Sort by today's views (least first)
            "title_asc": "title",
            "title_desc": "-title",
        }

        return queryset.order_by(order_mapping.get(order_by, "-post_date"))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        per_page = self.request.GET.get("per_page", 20)  # Default: 20

        try:
            per_page = int(per_page)
            if per_page > 100:
                per_page = 100  # Limit max per page
        except ValueError:
            per_page = 20

        paginator = Paginator(self.get_queryset(), per_page)
        page = self.request.GET.get("page")

        try:
            notes = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page.
            notes = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver the last page.
            notes = paginator.page(paginator.num_pages)


        def get_ad_by_shape(shape):
            ads = Ad.objects.filter(shape=shape).order_by('-click_count')

            if ads.exists():
                # Find the maximum click_count among the filtered ads
                max_click_count = ads.first().click_count

                # Filter ads with the maximum click_count
                top_ads = ads.filter(click_count=max_click_count)

                # Randomly select one ad from the top ads
                ad = random.choice(top_ads)
            else:
                # Fallback: Pick a random ad of the same shape if no matching tags
                ad = Ad.objects.filter(shape=shape).order_by('?').first()

            if ad:  # Ensure only the displayed ad is counted
                ad.increment_view_count()

            return ad
        
        # Get one ad per size
        context["ad_v"] = get_ad_by_shape('vertical')
        context["ad_h"] = get_ad_by_shape('horizontal')
        context["ad_q"] = get_ad_by_shape('square')

        context["notes"] = notes
        context["per_page"] = per_page  # Keep per_page value for template
        context["search_query"] = self.request.GET.get("q", "")  # Keep search value for template

        return context

class TagNoteView(AllNoteView):
    """View for displaying notes filtered by a specific tag"""

    def get(self, request, *args, **kwargs):
        # Debug output
        print("\n=== REQUEST DATA ===")
        print("URL:", request.path)
        print("GET params:", request.GET)
        print("URL kwargs:", kwargs)
        
        response = super().get(request, *args, **kwargs)
        return response

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_slug = self.kwargs.get('tag_slug')
        tag = get_object_or_404(Tag, slug=tag_slug)
        return queryset.filter(tags__name__in=[tag.name]).distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the tag and add to context
        tag_slug = self.kwargs.get('tag_slug')
        context['active_tag'] = get_object_or_404(Tag, slug=tag_slug)
        
        # Handle pagination
        per_page = self.request.GET.get('per_page', 20)
        try:
            per_page = int(per_page)
            if per_page < 1 or per_page > 100:
                per_page = 20
        except (ValueError, TypeError):
            per_page = 20
            
        paginator = Paginator(self.get_queryset(), per_page)
        page_number = self.request.GET.get('page', 1)
        
        try:
            notes = paginator.page(page_number)
        except PageNotAnInteger:
            notes = paginator.page(1)
        except EmptyPage:
            notes = paginator.page(paginator.num_pages)
            
        # Create parameters without tag (since it's in URL)
        params = self.request.GET.copy()
        if 'tag' in params:
            del params['tag']
        if 'page' in params:
            del params['page']
            
        context.update({
            'notes': notes,
            'per_page': per_page,
            'params': params,
        })
        
        return context
    
#*** Ads ***
def ad_click(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    user_ip = request.META.get("REMOTE_ADDR", "0.0.0.0")

    # Save the click record
    AdClick.objects.create(ad=ad, user_ip=user_ip)

    # Increase the click count
    ad.click_count += 1
    ad.save(update_fields=["click_count"])

    return JsonResponse({"message": "Click recorded!"})

def get_ad_by_shape(shape):
    ad = Ad.objects.filter(shape=shape).order_by('-click_count').first()
    if ad:
        ad.increment_view_count()  # Track the ad display
    return ad


#***POST***
#==============
class PostDetailView(DetailView):
#==============

    model = Post
    template_name = 'posts/post_details.html'

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])

        # Update daily views
        today = now().date()
        post_view, created = PostView.objects.get_or_create(post=post, date=today)
        if not created:
            post_view.count = F('count') + 1
            post_view.save()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        post = self.get_object()

        # Get related posts (same category OR shared tags)
        related_posts = Post.objects.filter(
            Q(category=post.category) | 
            Q(tags__in=post.tags.all()),
            state='published').exclude(pk=post.pk).distinct().order_by('-post_date')[:3]  
        
        context["related_posts"] = related_posts

        context["tags"] = post.tags.all()  # Show tags for the note
        # Get the tags associated with the current note
        tags = post.tags.all() 

        context["tags"] = tags
        context["view_counts"] = PostView.get_view_counts(post)

        def get_ad_by_shape(shape, tags):
            ads = Ad.objects.filter(shape=shape, tags__in=tags).order_by('-click_count')

            if ads.exists():
                # Find the maximum click_count among the filtered ads
                max_click_count = ads.first().click_count

                # Filter ads with the maximum click_count
                top_ads = ads.filter(click_count=max_click_count)

                # Randomly select one ad from the top ads
                ad = random.choice(top_ads)
            else:
                # Fallback: Pick a random ad of the same shape if no matching tags
                ad = Ad.objects.filter(shape=shape).order_by('?').first()

            if ad:  # Ensure only the displayed ad is counted
                ad.increment_view_count()

            return ad
        
        # Get one ad per size
        context["ad_v"] = get_ad_by_shape('vertical', tags)
        context["ad_h"] = get_ad_by_shape('horizontal', tags)
        context["ad_q"] = get_ad_by_shape('square', tags)

        return context


@login_required
def add_post(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Step 1: Save with commit=False
                post = form.save(commit=False)
                
                # Step 2: Set required fields NOT in the form
                post.author = request.user
                    
                # Step 3: Final save
                post.save()
                
                # Step 4: Save many-to-many relations
                form.save_m2m()
                
                messages.success(request, "Post created successfully!")
                return redirect(post.get_absolute_url())
                
            except Exception as e:
                messages.error(request, f"Error saving note: {str(e)}")
                # Print full error to console for debugging
                print(f"SAVE ERROR: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below")
            # Print form errors to console
            print("FORM ERRORS:", form.errors)
    else:
        form = AddPostForm()
    
    return render(request, 'posts/add_post.html', {
        'form': form,
        'title': 'Add New Post',
        'edit_mode': False,
        'current_user': request.user  # Pass user to template        
    })



@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = EditPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(post.get_absolute_url())
    else:
        form = EditPostForm(instance=post)
    return render(request, 'posts/update_post.html', {
        'form': form,
        'now': now(),
        'edit_mode': True,
        'title': f'Edit {post.title}'
    })



#==============
def post_top(request):
#==============

    posts = Post.objects.order_by('-post_date').filter(state="published")

    trending_date_threshold = now() - timedelta(days=7)
    
    # Get trending posts (most viewed in last 7 days)
    trending_posts = Post.objects.filter(
        state="published",
        views_per_day__date__gte=trending_date_threshold
    ).annotate(
        recent_views=models.Sum('views_per_day__count')
    ).order_by('-recent_views')[:4]

    latest_posts = posts[:4]
    remaining_posts = posts[5:11]

    # Fetch posts by category
    space_posts   = posts.filter(category='chemistry').order_by('-post_date')[:2]
    physics_posts = posts.filter(category='physics').order_by('-post_date')[:2]
    biology_posts = posts.filter(category='biology').order_by('-post_date')[:2]
    tech_posts    = posts.filter(category='tech').order_by('-post_date')[:2]
    popular_items = posts.filter(category='merch').annotate(total_views=Sum('views_per_day__count')).order_by('-total_views')[:4] 
    featured_post = posts.exclude(category ="merch").order_by('-post_date')[0]
    #featured_post = Post.objects.filter(state='published').order_by('-post_date')[0]

    context = {
        'trending_posts': trending_posts,
        'latest_posts': latest_posts,
        'remaining_posts': remaining_posts,
        'space_posts': space_posts,
        'physics_posts': physics_posts,
        'biology_posts': biology_posts,
        'tech_posts': tech_posts,
        'featured_post': featured_post,
        'popular_items': popular_items 
    }

    return render(request, 'posts/post_top.html', context)

#==============
class AllPostView(ListView):
#==============
    model = Post
    template_name = "posts/post_all.html"  # Template to be used
    context_object_name = "posts"
    paginate_by = 10  # Default pagination

    def get_queryset(self):

        if self.request.user.is_staff or self.request.user.is_superuser:
            # Admins can see both published and draft notes
            queryset = self.model.objects.filter(state__in=["published", "draft"])
        else:
            # Regular users only see published notes
            queryset = self.model.objects.filter(state="published")

        today = now().date()

        # Aggregate total views per note
        total_views = PostView.objects.filter(post=OuterRef('pk')).values('post').annotate(
            total=Coalesce(Sum('count'), Value(0))  # Replace None with 0
        ).values('total')

        # Aggregate today's views per note
        daily_views = PostView.objects.filter(post=OuterRef('pk'), date=today).values('post').annotate(
            daily=Coalesce(Sum('count'), Value(0))  # Replace None with 0
        ).values('daily')

        # Annotate Note model
        queryset = queryset.annotate(
            total_views=Coalesce(Subquery(total_views), Value(0)),
            daily_views=Coalesce(Subquery(daily_views), Value(0))
        )

        # Search functionality (title, content, and tags)
        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(caption__icontains=search_query) | 
                Q(abstract__icontains=search_query) | 
                Q(content__icontains=search_query) | 
                Q(tags__name__icontains=search_query)  # Assuming tags are stored as ManyToManyField
            ).distinct()

        # Sorting logic
        order_by = self.request.GET.get("order_by", "date_desc")
        order_mapping = {
            "date_desc": "-post_date",
            "date_asc": "post_date",
            "views_desc": "-total_views",  # Sort by total views (most first)
            "views_asc": "total_views",    # Sort by total views (least first)
            "daily_views_desc": "-daily_views",  # Sort by today's views (most first)
            "daily_views_asc": "daily_views",    # Sort by today's views (least first)
            "title_asc": "title",
            "title_desc": "-title",
        }

        return queryset.order_by(order_mapping.get(order_by, "-post_date"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        per_page = self.request.GET.get("per_page", 10)  # Default: 10

        try:
            per_page = int(per_page)
            if per_page > 100:
                per_page = 100  # Limit max per page
        except ValueError:
            per_page = 10

        paginator = Paginator(self.get_queryset(), per_page)
        page = self.request.GET.get("page")

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver the last page.
            posts = paginator.page(paginator.num_pages)

        def get_ad_by_shape(shape):
            ads = Ad.objects.filter(shape=shape).order_by('-click_count')

            if ads.exists():
                # Find the maximum click_count among the filtered ads
                max_click_count = ads.first().click_count

                # Filter ads with the maximum click_count
                top_ads = ads.filter(click_count=max_click_count)

                # Randomly select one ad from the top ads
                ad = random.choice(top_ads)
            else:
                # Fallback: Pick a random ad of the same shape if no matching tags
                ad = Ad.objects.filter(shape=shape).order_by('?').first()

            if ad:  # Ensure only the displayed ad is counted
                ad.increment_view_count()

            return ad

        latest_posts = Post.objects.filter(state="published").order_by('-post_date')[:3]
        trending_posts = self.get_queryset().filter(state="published").order_by('-daily_views')[:3]

        context = {
            'latest_posts': latest_posts,
            "trending_posts": trending_posts,  # Add trending posts to context
        }        

        # Get one ad per size
        context["ad_v"] = get_ad_by_shape('vertical')
        context["ad_h"] = get_ad_by_shape('horizontal')
        context["ad_q"] = get_ad_by_shape('square')

        context["posts"] = posts
        context["per_page"] = per_page  # Keep per_page value for template
        context["search_query"] = self.request.GET.get("q", "")  # Keep search value for template

        return context



#***Field***
class SubjectDetailView(DetailView):

    model = Subject
    template_name = "fields/subject.html"
    context_object_name = "subject"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fields"] = Field.objects.filter(subject=self.object).order_by("ordering")
        return context


#=================
class FieldDetailView(DetailView):
#=================

    model = Field
    template_name = 'fields/field_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super(FieldDetailView, self).get_context_data(*args, **kwargs)
        field = self.get_object()

        def get_ad_by_shape(shape):
            ads = Ad.objects.filter(shape=shape).order_by('-click_count')

            if ads.exists():
                # Find the maximum click_count among the filtered ads
                max_click_count = ads.first().click_count

                # Filter ads with the maximum click_count
                top_ads = ads.filter(click_count=max_click_count)

                # Randomly select one ad from the top ads
                ad = random.choice(top_ads)
            else:
                # Fallback: Pick a random ad of the same shape if no matching tags
                ad = Ad.objects.filter(shape=shape).order_by('?').first()

            if ad:  # Ensure only the displayed ad is counted
                ad.increment_view_count()

            return ad
        
        # Get one ad per size
        context["ad_v"] = get_ad_by_shape('vertical')
        context["ad_h"] = get_ad_by_shape('horizontal')
        context["ad_q"] = get_ad_by_shape('square')

        return context


def edit_field(request, pk):
    field = get_object_or_404(Field, pk=pk)

    if request.method == 'POST':
        form = EditFieldForm(request.POST, request.FILES, instance=field)
        if form.is_valid():
            form.save()
            messages.success(request, 'Field updated successfully!')
            return redirect('field_detail', pk=field.pk)
        else:
            # Print form errors for debugging
            print(form.errors)
    else:
        form = EditFieldForm(instance=field)

    return render(request, 'fields/update_field.html', {'form': form, 'field': field})
