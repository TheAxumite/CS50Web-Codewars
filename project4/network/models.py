from django.contrib.auth.models import AbstractUser
from django.db import models
import json
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.utils import IntegrityError
from django.db.models import Q
import uuid


class User(AbstractUser):
    followers = models.ManyToManyField(
        "self", related_name="list_of_followers", blank=True, symmetrical=False)
    following = models.ManyToManyField(
        "self", related_name="list_of_following", blank=True, symmetrical=False)

    @classmethod
    def follow_unfollow(cls, target, currentprofile):
        user = User.objects.get(username=currentprofile)
        target_profile = User.objects.get(username=target)
        if target_profile != currentprofile:
            print(target_profile)
            print(currentprofile)
            if target_profile.username in user.followers.all():
                return {"followers": True}
            else:
                user.following.add(target_profile)
                target_profile.followers.add(user)
                return {"followers": user.followers.count()}
        else:
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
    originalpost = models.BooleanField(default=True)
    postlikes = models.ManyToManyField(
        "User", related_name="list_of_post_likes", blank=True)
    parentcomment = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="parent")
    childcomments = models.ManyToManyField(
        "self", related_name="ListofChildComments", blank=True, symmetrical=False)

    @classmethod
    def add_post(cls, post, user):
        return cls.objects.create(post=post, user=user)

    @classmethod
    def addComment(cls, post, parent_id, user):
        parentpost = Posts.objects.get(pk=parent_id)
        childcomment = cls.objects.create(
            post=post, user=user, originalpost=False, parentcomment=parentpost)
        parentpost.childcomments.add(childcomment)
        return childcomment

    @classmethod
    def CommentCount(cls, id):
        return int(cls.objects.get(pk=id).childcomments.count())

    @classmethod
    def LoadChldComments(cls, id):
        return cls.objects.filter(parentcomment=id).order_by("timestamp")

    @classmethod
    def like_post(cls, post_id, user):
        post = cls.objects.get(pk=post_id)

        if user in post.postlikes.all():
            post.postlikes.remove(user)
            return {"liked": True, "like_count": post.postlikes.count()}
        else:
            post.postlikes.add(user)
            return {"liked": False, "like_count": post.postlikes.count()}

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

    @classmethod
    def following_list(cls, currentuser):
        # Get the list of usernames that the current user is following
        """The .values_list() method is a query method available in Django.
        It is used to retrieve specific field values from a queryset, returning a list of tuples or flat values, depending on the parameters provided.
        The basic syntax for using .values_list() in Django is as follows: queryset.values_list(*fields, flat=False) 
        """
        user = User.objects.get(
            username=currentuser).list_of_following.values_list('pk', flat=True)
        print(user)
        # Old Code for reference
        """query = Q()  # Initialize an empty Q objectz
        # Add conditions for each username in the following list
        for username in following_usernames :
        # Combine Q objects using |= (in-place bitwise OR assignment)
            query |= Q(user=username)
        print(query)
        # Use the query Q object to filter users
        following_users = Posts.objects.filter(user = query).order_by("-timestamp")"""
        """The __in lookup in Django is equivalent to the SQL IN clause. When used in a Django ORM query, 
        it generates SQL that matches any object where the specified field's value is in the provided list."""

        return cls.objects.filter(user__in=user, originalpost=True).order_by("-timestamp")

    def serialize(self, user):
        if user in self.postlikes.all():
            likes = True
        else:
            likes = False
        return {
            "id": self.id,
            "user": self.user.username,
            "post": self.post,
            "post_likes": self.postlikes.count(),
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "current_user_like": likes,
            "parentcomment": str(self.parentcomment),
            "ParentRepliesCount": Posts.objects.filter(parentcomment=self.parentcomment).order_by("-timestamp").count(),
            'replies': self.childcomments.count(),
            'currentprofile': True if self.user.username == user else False}


@classmethod
class channels(models.Model):
    channelReciever = models.ForeignKey('User', on_delete=models.CASCADE, related_name= "reciever")
    channelName = models.TextField()

@classmethod
class messages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.TextField()
    sender = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="messagescriber")
    reciever = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="messagereciever")
    timestamp = models.DateTimeField(auto_now_add=True)

    @classmethod
    def addMessage(cls, message, sender, reciever):
        try:
            sender = Posts.objects.get(pk=sender)
            reciever = Posts.objects.get(pk=reciever)
        except ObjectDoesNotExist:
            return "Post has been deleted"
        except ValidationError as e:
            return f"Validation error: {e}"
        except IntegrityError as e:
            return f"Integrity error: {e}"
        try:
            cls.objects.create(sender=sender, reciever=reciever)
        except ValidationError as e:
                return f"Validation error: {e}"
        except IntegrityError as e:
                return f"Integrity error: {e}"
