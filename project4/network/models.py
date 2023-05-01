from django.contrib.auth.models import AbstractUser
from django.db import models
import json
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.utils import IntegrityError


class User(AbstractUser):
    followers = models.ManyToManyField(
        "self", related_name="list_of_followers", blank=True, symmetrical=False)
    following = models.ManyToManyField(
        "self", related_name="list_of_following", blank=True, symmetrical=False)

    @classmethod
    def follow_unfollow(cls, target, currentprofile):
        user = User.objects.get(username=currentprofile)
        target_profile = User.objects.get(username=target)

        if target_profile.username in user.followers.all():
            return {"followers": True}
        else:
            user.following.add(target_profile)
            target_profile.followers.add(user)
            return {"followers": user.followers.count()}

    def check_following(self, profile_id):
        user_to_follow = User.objects.get(id=profile_id)
        if user_to_follow.followers.filter(id=self.id).exists():
            return True

    def count_followers_and_following(user):
        count = User.objects.get(username=user)
        return {"followers": count.followers.count(), "following": count.following.count()}

    def following_list(self):
        followinglist = User.objects.get(id=self.id)
        return followinglist.following


class Posts(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="poster")
    timestamp = models.DateTimeField(auto_now_add=True)
    post = models.TextField()
    original_post = models.BooleanField(default=True)
    post_likes = models.ManyToManyField(
        "User", related_name="list_of_post_likes")
    parent_comment = models.OneToOneField(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="parent")
    child_comments = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="child_comments_lists")

    @classmethod
    def add_post(cls, post, user):
        return cls.objects.create(post=post, user=user)

    @classmethod
    def add_comment(cls, post, parent_id, user):
        parent_post = Posts.objects.get(pk=parent_id)
        child_comment = cls.objects.create(
            post=post, user=user, original_post=False, parent_comment=parent_post)
        parent_post.child_comments.add(child_comment)
        return child_comment

    @classmethod
    def CommentCount(cls, id):
        return int(cls.objects.get(pk=id).child_comments.count())

    @classmethod
    def load_comment(cls, id):
        post = Posts.objects.get(pk=id)

    @classmethod
    def like_post(cls, post_id, user):
        post = cls.objects.get(pk=post_id)
        
        if user in post.post_likes.all():
            post.post_likes.remove(user)
            return {"liked": True, "like_count": post.post_likes.count()}
        else:
            post.post_likes.add(user)
            return {"liked": False, "like_count": post.post_likes.count()}

    @classmethod
    def edit_post(cls, id, updated_post):
        try:
            post = cls.objects.get(pk=id)
            post.post = updated_post
            post.save()
            post.full_clean()
            return cls.objects.get(pk=id).post
        except ObjectDoesNotExist:
            return "Post has been deleted"
        except ValidationError as e:
            return f"Validation error: {e}"
        except IntegrityError as e:
            return f"Integrity error: {e}"

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
