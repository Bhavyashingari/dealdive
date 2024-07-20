# Import necessary models and fields for your data.
from django.db import models

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    # other user fields

class Item(models.Model):
    item_id = models.IntegerField(primary_key=True)
    # other item fields

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    rating = models.FloatField()
