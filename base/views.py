from django.contrib import messages
from django.shortcuts import render, redirect
from .utils import validate_picture, paginate_posts, search
from .models import Post, Comment, Like, Follower
from users.models import User
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def index(request):
    users = User.objects.filter().order_by('-date_joined')[:4]
    posts, search_query = search(request)
    custom_range, posts = paginate_posts(request, posts, 2)
    context = {'posts': posts, 'custom_range': custom_range, 'search_query': search_query,
               'users': users}
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def comments(request, pk):
    post = Post.objects.get(id=pk)

    if request.method == "POST":
        content = request.POST.get("content")
        comment = Comment.objects.create(post=post, user=request.user, content=content)
        comment.save()

    comments = post.comment_set.all()

    context = {'comments': comments, "post": post}
    return render(request, "base/comments.html", context)


@login_required(login_url='login')
def user_posts(request):
    posts = request.user.post_set.all()
    custom_range, posts = paginate_posts(request, posts, 2)
    context = {'posts': posts, 'custom_range': custom_range}

    return render(request, "base/user-posts.html", context)


@login_required(login_url='login')
def follow_user(request, pk):
    if request.method == "POST":
        user = request.user
        followed_user = User.objects.get(id=pk)

        try:
            follower_obj = Follower.objects.get(user=user, followed=followed_user)
            follower_obj.delete()
        except:
            follower_obj = Follower.objects.create(user=user, followed=followed_user)
            follower_obj.save()

        return redirect("profile-view", followed_user.id)


@login_required(login_url='login')
def create_post(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        if not(validate_picture(image)):
            messages.error(request, "فایل ورودی معتبر نیست.")
            return redirect("create-post")

        post = Post.objects.create(user=request.user, title=title, content=content, image=image)
        post.save()

        return redirect("home")

    return render(request, 'base/create-post.html', {})


@login_required(login_url='login')
def update_post(request, pk):
    post = Post.objects.get(id=pk, user=request.user)
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        if image:
            if not(validate_picture(image)):
                messages.error(request, "فایل ورودی معتبر نیست.")
                return redirect("update-post")
            else:
                post.image = image

        if title:
            post.title = title

        if content:
            post.content = content

        post.save()

    return render(request, "base/update-post.html", {"post": post})


@login_required(login_url='login')
def delete_post(request, pk):
    if request.method == "POST":
        post = Post.objects.get(id=pk, user=request.user)
        post.delete()
        return redirect("home")


@login_required(login_url='login')
def like_post(request, pk):

    post = Post.objects.get(id=pk)
    user = request.user

    if Like.objects.filter(user=user, post=post).exists():
        like = Like.objects.get(user=user, post=post)
        like.delete()
    else:
        like = Like.objects.create(post=post, user=user)
        like.save()

    return redirect("home")





