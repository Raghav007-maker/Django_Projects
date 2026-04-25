from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from rest_framework.viewsets import ModelViewSet # ModelViewSet - To automatically get all CRUD operations
from .models import Post, Comment, PostLike
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated # Built-in permission class
from .permissions import IsAuthorOrReadOnly # Importing your custom permission
from .forms import SignupForm, CreatePostForm, CommentForm

# Create your views here.

# Creating a ViewSet for Post - To handle all crud operations in one class
class PostViewSet(ModelViewSet):
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    # Only logged-in users can access API
    # Applying multiple permissions
    # IsAuthenticated - Only logged-in users can access
    # IsAuthorOrReadOnly - Only author can edit/delete
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        # Automatically assign logged-in user as author
        serializer.save(author=self.request.user)


def home_view(request):
    posts = Post.objects.select_related('author').order_by('-created_at')
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog_app/home.html', {'page_obj': page_obj})


def post_detail_view(request, post_id):
    post = get_object_or_404(Post.objects.select_related('author'), id=post_id)
    comments = post.comments.select_related('user').all()
    user_liked = False
    if request.user.is_authenticated:
        user_liked = PostLike.objects.filter(post=post, user=request.user).exists()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': CommentForm(),
        'user_liked': user_liked,
    }
    return render(request, 'blog_app/post_detail.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form_data = request.POST.copy() if request.method == 'POST' else None
    if form_data:
        entered = form_data.get('username', '').strip()
        if '@' in entered:
            matched_user = User.objects.filter(email__iexact=entered).first()
            if matched_user:
                form_data['username'] = matched_user.username

    form = AuthenticationForm(request, data=form_data)
    form.fields['username'].widget.attrs.update({'class': 'form-control'})
    form.fields['password'].widget.attrs.update({'class': 'form-control'})
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('home')

    return render(request, 'blog_app/login.html', {'form': form})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')

    return render(request, 'blog_app/signup.html', {'form': form})


@login_required
def create_post_view(request):
    form = CreatePostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        Post.objects.create(
            title=form.cleaned_data['title'],
            content=form.cleaned_data['content'],
            author=request.user,
        )
        messages.success(request, 'Post created successfully.')
        return redirect('home')

    return render(request, 'blog_app/create_post.html', {'form': form})


@login_required
def edit_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        messages.error(request, 'You can only edit your own posts.')
        return redirect('post_detail', post_id=post.id)

    initial_data = {
        'title': post.title,
        'content': post.content,
    }
    form = CreatePostForm(request.POST or None, initial=initial_data)
    if request.method == 'POST' and form.is_valid():
        post.title = form.cleaned_data['title']
        post.content = form.cleaned_data['content']
        post.save()
        messages.success(request, 'Post updated successfully.')
        return redirect('post_detail', post_id=post.id)

    return render(request, 'blog_app/edit_post.html', {'form': form, 'post': post})


@login_required
@require_POST
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        messages.error(request, 'You can only delete your own posts.')
        return redirect('post_detail', post_id=post.id)

    post.delete()
    messages.success(request, 'Post deleted successfully.')
    return redirect('home')


@login_required
@require_POST
def toggle_like_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = PostLike.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect('post_detail', post_id=post.id)


@login_required
@require_POST
def add_comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        Comment.objects.create(
            post=post,
            user=request.user,
            content=form.cleaned_data['content'],
        )
        messages.success(request, 'Comment added.')
    else:
        messages.error(request, 'Comment cannot be empty.')
    return redirect('post_detail', post_id=post.id)


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')
