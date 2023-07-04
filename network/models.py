from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Follow(models.Model):
    following = models.ForeignKey(User, related_name="who_is_followed", on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name="who_follows", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.follower} is following {self.following}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    text = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.DecimalField(default=0, max_digits=5, decimal_places=0)

    def __str__(self):
        return f"Post {self.id} made by {self.user}, liked {self.likes} times"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_like")

    def __str__(self):
        return f"{self.user} liked {self.post}"