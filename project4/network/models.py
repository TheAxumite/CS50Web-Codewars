from django.contrib.auth.models import AbstractUser
from django.db import models
import json


class User(AbstractUser):
    followers = models.ManyToManyField(
        "self", related_name="list_of_followers", blank=True, symmetrical=False)
    following = models.ManyToManyField(
        "self", related_name="list_of_following", blank=True, symmetrical=False)

    @classmethod
    def follow_unfollow(cls, username, profile):
        user = User.objects.get(username=username)
        target_profile = User.objects.get(username=profile)

        if target_profile in user.followers.all():
            return {"followers": True}
        else:
            user.followers.add(target_profile)
            target_profile.following.add(user)
            return {"followers": user.followers.count()}

    def check_following(self, profile_id):
        user_to_follow = User.objects.get(id=profile_id)
        if user_to_follow.followers.filter(id=self.id).exists():
            return True

    def count_followers_and_following(user):
        count = User.objects.get(username=user)
        return {"followers": count.followers.count(), "following": count.following.count()}


class Posts(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="poster")
    timestamp = models.DateTimeField(auto_now_add=True)
    post = models.TextField()
    post_likes = models.ManyToManyField(
        "User", related_name="list_of_post_likes")

    @classmethod
    def add_post(cls, post, user):
        return cls.objects.create(post=post, user=user)

    @classmethod
    def like_post(cls, post, user):
        if user in cls.objects.get(pk=post).post_likes.all():
            post = cls.objects.get(pk=post)
            post.post_likes.remove(user)
            return {"liked": True, "like_count": post.post_likes.count()}
        post = cls.objects.get(pk=post)
        post.post_likes.add(user)
        return {"liked": False, "like_count": post.post_likes.count()}

    def serialize(self, user):
        if user in self.post_likes.all():
            likes = True
        else:
            likes = False
        return {
            "id": self.id,
            "user": self.user.username,
            "post": self.post,
            "post_likes": self.post_likes.count(),
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "current_user_like": likes}


class Comments(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter")
    comment = models.TextField()
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="list_of_likes")

    @classmethod
    def list_comments(cls, post_id):
        return cls.objects.filter(post=post_id)

    @classmethod
    def post_comment(cls, comment, user, post):
        return cls.objects.create(comment=comment, user=user, post=post)

    @classmethod
    def like_comment(cls, user, comment_id):
        comment_to_like = Comments.objects.get(pk=comment_id)
        comment_to_like.likes.add(user)

    @classmethod
    def unlike_comment(cls, user, comment_id):
        comment_to_like = Comments.objects.get(pk=comment_id)
        comment_to_like.likes.remove(user)
