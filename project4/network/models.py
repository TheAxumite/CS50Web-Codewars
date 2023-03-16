from django.contrib.auth.models import AbstractUser
from django.db import models
import json



class User(AbstractUser):
    followers = models.ManyToManyField(
        "self", related_name="list_of_followers", blank=True)
    following = models.ManyToManyField(
        "self", related_name="list_of_following", blank=True)

    def follow(self, profile_id):
        user_to_follow = User.objects.get(id=profile_id)
        if user_to_follow.followers.filter(id=self.id).exists():
            return False
        user_to_follow.followers.add(self)
        return True

    def count_followers_and_following(self):
        return {"followers":self.followers.count(), "following":self.followers.count()}


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
            return {"liked":True, "like_count": post.post_likes.count()}
        post = cls.objects.get(pk=post)
        post.post_likes.add(user)
        return {"liked":False, "like_count": post.post_likes.count()}



    def serialize(self):
        if self.user in self.post_likes.all():
            likes = True
        else:
            likes = False
        return {
            "id": self.id,
            "user": self.user.username,
            "post": self.post,
            "post_likes": self.post_likes.count(),
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "current_user_like": likes
            
        }




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
