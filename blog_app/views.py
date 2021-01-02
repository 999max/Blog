from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Post, Comment
from .forms import PostForm, CommentForm


# Create your views here.


def index(request):
    context = {'title': 'Welcome to Blog'}
    return render(request, 'blog_app/index.html', context)


@login_required
def posts(request):
    posts = Post.objects.filter(owner=request.user).order_by('-date_added')
    context = {'title': 'All Posts', 'posts': posts}
    return render(request, 'blog_app/posts.html', context)


@login_required
def post(request, post_id):
    post = Post.objects.get(pk=post_id)
    # check if this post belongs to the owner
    if post.owner != request.user:
        raise Http404

    comments = post.comment_set.order_by('-date_added')
    context = {'title': 'Post', 'post': post, 'comments': comments}
    return render(request, 'blog_app/post.html', context)


@login_required
def new_post(request):
    """Create new Post"""
    if request.method != 'POST':
        # creates empty form
        form = PostForm()
    else:
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            return redirect('blog_app:posts')
    context = {'title': 'Create New Post', 'form': form}
    return render(request, 'blog_app/new_post.html', context)


@login_required()
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    # check if this post belongs to the owner
    if post.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog_app:posts')
    context = {'title': 'Edit Post', 'form': form, 'post': post}
    return render(request, 'blog_app/edit_post.html', context)


@login_required
def new_comment(request, post_id):
    """Create comment for post."""
    post = Post.objects.get(id=post_id)

    if request.method != 'POST':
        form = CommentForm()
    else:
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.owner = request.user
            comment.save()
            return redirect('blog_app:post', post_id=post_id)

    context = {'title': 'New Comment', 'post': post, 'form': form}
    return render(request, 'blog_app/new_comment.html', context)


@login_required
def edit_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    # check if this comment belongs to the owner
    if comment.owner != request.user:
        raise Http404

    post = comment.post
    if request.method != 'POST':
        form = CommentForm(instance=comment)
    else:
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog_app:post', post_id=post.id)

    context = {'title': "Edit Comment", 'form': form, 'comment': comment, 'post': post}
    return render(request, 'blog_app/edit_comment.html', context)