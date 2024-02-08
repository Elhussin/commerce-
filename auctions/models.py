from django.contrib.auth.models import AbstractUser
from django.db import models




class User(AbstractUser):
    pass




class Listing(models.Model):                
        title = models.CharField(max_length=64)
        description =models.CharField(max_length=200)
        amount = models.FloatField(max_length=64)
        endAmont = models.FloatField(max_length=64,default=0)
        url =models.CharField(max_length=250)
        category =models.CharField(max_length=64)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="EnterUser")
        status=models.CharField(max_length=64 ,default='open')
        def __str__(self):
            return f"{self.id} {self.title} {self.description} {self.amount} {self.url}  {self.category}"
        



class Comment(models.Model):
    title =models.CharField(max_length=64)
    comment =models.TextField()
    Listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="Listing" )
    Comment_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User")




class Paid(models.Model):
    Paid_amount = models.FloatField(max_length=64)
    user_bids = models.ForeignKey(User, on_delete=models.CASCADE, related_name="UserId")
    Listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listID")
