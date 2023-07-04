from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json

from .models import User, Post, Follow, Like


def index(request):
    posts = Post.objects.all().order_by("-date")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    likes = Like.objects.all()

    whoYouLiked = []
    try:
        for like in likes:
            if like.user == request.user:
                whoYouLiked.append(like.post.id)
    except:
        whoYouLiked = []

    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "whoYouLiked": whoYouLiked
    })


def profile(request, id):
    following = User.objects.get(id=id)
    posts = Post.objects.filter(user=following).order_by("-date")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    try: 
        follower_id = list(Follow.objects.filter(following_id=id).values_list('follower', flat=True))
        followers = list(User.objects.filter(id__in=follower_id).values_list('username', flat=True))
        following_count = Follow.objects.filter(follower=following).count()
        followers_count = Follow.objects.filter(following=following).count()
        return render(request, "network/profile.html", {
            "following": following,
            "followers": followers,
            "following_count": following_count,
            "followers_count": followers_count,
            "page_obj": page_obj
        })

    except:
        following_count = Follow.objects.filter(follower=following).count()
        followers_count = Follow.objects.filter(following=following).count()
        return render(request, "network/profile.html", {
            "following": following,
            "following_count": following_count,
            "followers_count": followers_count,
            "page_obj": page_obj
        })


@login_required
def following(request):
    following = list(Follow.objects.filter(follower=request.user).values_list('following', flat=True))
    posts = Post.objects.filter(user__in=following).order_by("-date")

    likes = Like.objects.all()
    whoYouLiked = []
    try:
        for like in likes:
            if like.user == request.user:
                whoYouLiked.append(like.post.id)
    except:
        whoYouLiked = []

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "page_obj": page_obj,
        "whoYouLiked": whoYouLiked
    })


@login_required
def follow(request, id):
    if request.method == "POST":
        following = User.objects.get(id=id)
        follow = Follow(follower=request.user, following=following)
        follow.save()
        return HttpResponseRedirect(reverse("profile", args=(id,)))

    return HttpResponseNotFound("404")


@login_required
def unfollow(request, id):
    if request.method == "POST":
        following = User.objects.get(id=id)
        follow = Follow.objects.get(follower=request.user, following=following)
        follow.delete()
        return HttpResponseRedirect(reverse("profile", args=(id,)))

    return HttpResponseNotFound("404")


@login_required
def new_post(request):
    if request.method == "POST":
        data = request.POST.get("text")
        post = Post(user=request.user, text=data)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    
    return HttpResponseNotFound('404')


@csrf_exempt
@login_required
def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=post_id)
        edit_post.text = data["text"]
        edit_post.save()
        return JsonResponse({"message": "Change successful", "data": data["text"]})


@login_required
def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    newLike = Like(user=user, post=post)
    newLike.save()
    post.likes += 1
    post.save()
    return JsonResponse({"message": "Like added!"})


@login_required
def unlike(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Like.objects.get(user=user, post=post)
    like.delete()
    post.likes -= 1
    post.save()
    return JsonResponse({"message": "Like removed!"})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
