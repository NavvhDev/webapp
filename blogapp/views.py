from django.shortcuts import render, redirect
from . models import Blog, Comment, Category
from django.contrib.auth.decorators import login_required
from .forms import CreateBlogForm, CommentForm
from django.utils.text import slugify
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
def index(request):
    keyword = request.GET.get("search")
    category_id = request.GET.get("category")
    msg = None
    blogs = Blog.objects.all()
    featured_blog = Blog.objects.filter(featured=True).first()

    if keyword:
        blogs = blogs.filter(
            Q(title__icontains=keyword) |
            Q(body__icontains=keyword) |
            Q(category__title__icontains=keyword)
        )
        if not blogs.exists() and featured_blog:
            msg = "There is no article with the keyword. But you may be interested in the featured blog below"
            blogs = [featured_blog]
            
    #widgets category
    if category_id:
        blogs = blogs.filter(category__id=category_id)

    #Pagination
    paginator = Paginator(blogs, 4)
    page = request.GET.get('page')

    try:
        paginated_blogs = paginator.page(page)
    except PageNotAnInteger:
        paginated_blogs = paginator.page(1)
    except EmptyPage:
        paginated_blogs = paginator.page(paginator.num_pages)

    categories = Category.objects.all()
    context = {
        "blogs": paginated_blogs,
        "f_blog": featured_blog if not keyword else None,
        "msg": msg,
        "categories": categories
    }

    return render(request, "blogapp/index.html", context)

def detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    comments = Comment.objects.filter(blog=blog)
    form = CommentForm()
    
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.blog = blog
                comment.user = request.user
                comment.save()
                return redirect('detail', slug=blog.slug)
            
    context = {'blog': blog, "form":form, 'comments':comments}
    return render(request, "blogapp/detail.html", context)

@login_required(login_url="signin")
def create_article(request):
    form = CreateBlogForm
    if request.method == 'POST':
        form = CreateBlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.slug = slugify(request.POST["title"])
            blog.user = request.user
            blog.save()
            messages.success(request, "Article created successfully")
            return redirect("profile")
    context  = {"form":form}
    return render(request, "blogapp/create.html", context)

@login_required(login_url="signin")
def update_article(request, slug):
    update = True
    blog = Blog.objects.get(slug=slug)
    form = CreateBlogForm(instance=blog)
    if request.method == 'POST':
        form = CreateBlogForm(request.POST, request.FILES, instance=blog)
        blog = form.save(commit=False)
        blog.slug = slugify(request.POST["title"])
        blog.save()
        messages.success(request, "Article updated successfully")
        return redirect("profile")

    context = {"update":update, "form":form}
    return render(request, "blogapp/create.html", context)


@login_required(login_url="signin")
def delete_article(request, slug):
    blogs = Blog.objects.filter(user=request.user)
    delete = True
    blog = Blog.objects.get(slug=slug)
    
    if request.method == 'POST':
        blog.delete()
        messages.success(request, "Article deleted successfully")
        return redirect("profile")
    context = {"blog":blog, "delete":delete, "blogs": blogs}
    return render(request, "core/profile.html", context)