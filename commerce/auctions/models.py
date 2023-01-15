from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.urls import reverse
from django.utils.timezone import datetime

class User(AbstractUser):
    pass


class Item(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    image_file = models.ImageField(upload_to='items/', null=True, blank=True)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=100)

    

    def create_item(name, description, starting_price, image_file, image_url, category, seller):
        item = Item(title=name,
                    description=description,
                    starting_price=starting_price,
                    image_url=image_url,
                    image_file=image_file,
                    category=category,
                    seller=seller)
        item.image_file = image_file
        item.save()
        return item



class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="auction_item")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_winning = models.BooleanField(default=False)





class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watcher")
    item = models.ManyToManyField(Item, blank=True, related_name= "items")


    def add_watchlist(user, item):
          watchlist = WatchList.objects.get_or_create(user=user)[0]
          watchlist.item.add(item)
          watchlist.save()
          return watchlist




class Comments(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

