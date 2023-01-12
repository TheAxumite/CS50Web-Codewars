from .models import *


def create_item(name, description, starting_price, end_date, image, seller):
    item = Item(name=name,
                description=description,
                starting_price=starting_price,
                end_date=end_date,
                image=image,
                seller=seller)
    item.save()
    return item