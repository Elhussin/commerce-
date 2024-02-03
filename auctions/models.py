from django.contrib.auth.models import AbstractUser
from django.db import models




class User(AbstractUser):
    pass




class auction_listings(models.Model):                
        title = models.CharField(max_length=64)
        description =models.CharField(max_length=64)
        amount = models.CharField(max_length=64)
        url =models.CharField(max_length=64)
        category =models.CharField(max_length=64)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="EnterUser")
        status=models.CharField(max_length=64 ,default=0)
        def __str__(self):
            return f"{self.id} {self.title} {self.description} {self.amount} {self.url}  {self.category}"
        



class Comment(models.Model):
    title =models.CharField(max_length=64)
    comment =models.TextField()
    auction_listings_id = models.ForeignKey(auction_listings, on_delete=models.CASCADE, related_name="auction_listings")
    created_Comment_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User")




class Paid(models.Model):
    Paid_amount = models.CharField(max_length=64)
    user_bids_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="UserId")
    listings_id = models.ForeignKey(auction_listings, on_delete=models.CASCADE, related_name="listID")
