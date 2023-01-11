from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.urls import reverse

class User(AbstractUser):
    pass


class Item(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    name = models.CharField(max_length=100)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    end_date = models.DateTimeField()
    image = models.ImageField(upload_to='items/', null=True, blank=True)

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return None


class Bid(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="auction_item")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_winning = models.BooleanField(default=False)

class Comments(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add=True)




    