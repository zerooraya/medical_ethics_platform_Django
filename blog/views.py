from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Post, Category
from .forms import PostForm


def is_editor(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def get_categories():
    return Category.objects.all()


# ── Home Page ──────────────────────────────────────────
def home(request):
    posts = Post.objects.filter(status='approved').select_related('author', 'category').order_by('-created_at')
    q = request.GET.get('q', '').strip()
    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(content__icontains=q))
    cat_slug = request.GET.get('category', '').strip()
    if cat_slug:
        posts = posts.filter(category__slug=cat_slug)
    return render(request, 'blog/home.html', {
        'posts': posts,
        'categories': get_categories(),
        'query': q,
        'active_cat': cat_slug,
    })


# ── Approved Posts Page ────────────────────────────────
def approved_posts(request):
    posts = Post.objects.filter(status='approved').select_related('author', 'category').order_by('-created_at')
    cat_slug = request.GET.get('category', '').strip()
    if cat_slug:
        posts = posts.filter(category__slug=cat_slug)
    return render(request, 'blog/approved_posts.html', {
        'posts': posts,
        'categories': get_categories(),
        'active_cat': cat_slug,
    })


# ── Post Detail Page ───────────────────────────────────
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.status != 'approved':
        if not (is_editor(request.user) or request.user == post.author):
            messages.warning(request, 'This post is not publicly available.')
            return redirect('home')
    return render(request, 'blog/post_detail.html', {'post': post})


# ── Create Post Page ───────────────────────────────────
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = 'pending'
            post.save()
            messages.success(request, 'Your post has been submitted and is awaiting editor approval.')
            return redirect('home')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})


# ── Edit Post ──────────────────────────────────────────
@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author and not is_editor(request.user):
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('post-detail', pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            p = form.save(commit=False)
            p.status = 'pending'
            p.save()
            messages.success(request, 'Post updated and re-submitted for approval.')
            return redirect('post-detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/create_post.html', {'form': form, 'edit': True, 'post': post})


# ── Delete Post ────────────────────────────────────────
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author and not is_editor(request.user):
        messages.error(request, 'Permission denied.')
        return redirect('post-detail', pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('home')
    return render(request, 'blog/delete_post.html', {'post': post})


# ── Category Page ──────────────────────────────────────
def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(status='approved', category=category).order_by('-created_at')
    return render(request, 'blog/category_posts.html', {
        'posts': posts,
        'category': category,
        'categories': get_categories(),
    })


# ── Editor Approval Page ───────────────────────────────
@login_required
@user_passes_test(is_editor, login_url='home')
def editor_panel(request):
    pending  = Post.objects.filter(status='pending').select_related('author', 'category').order_by('created_at')
    approved = Post.objects.filter(status='approved').select_related('author', 'category').order_by('-reviewed_at')[:15]
    rejected = Post.objects.filter(status='rejected').select_related('author', 'category').order_by('-reviewed_at')[:15]
    return render(request, 'blog/editor_panel.html', {
        'pending': pending,
        'approved': approved,
        'rejected': rejected,
    })


@login_required
@user_passes_test(is_editor, login_url='home')
def approve_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.status = 'approved'
    post.reviewed_by = request.user
    post.reviewed_at = timezone.now()
    post.save()
    messages.success(request, f'"{post.title}" approved successfully.')
    return redirect('editor-panel')


@login_required
@user_passes_test(is_editor, login_url='home')
def reject_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.status = 'rejected'
    post.reviewed_by = request.user
    post.reviewed_at = timezone.now()
    post.save()
    messages.warning(request, f'"{post.title}" has been rejected.')
    return redirect('editor-panel')
