from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:item_id>", views.listing, name="listings"),
    path("post_item", views.post_item, name="post_item"),
    path("place_bid", views.bid, name="place_bid"),
    path("add_watchlist", views.add_to_watchlist, name="add_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("remove_watchlist", views.remove_watchlist, name="remove_watchlist"),
    path("close_auction", views.close_bid, name="close_auction"),
    path("category", views.categories, name="category"),
    path("post_comment", views.comment, name="post_comment")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
