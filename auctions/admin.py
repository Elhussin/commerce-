from django.contrib import admin

# Register your models here.
from .models import auction_listings, Paid ,Comment
# Register your models here.

class auction_listingsAdmin(admin.ModelAdmin):
    list_display = ("__str__", "category")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "comment")
# class PassengerAdmin(admin.ModelAdmin):
#     filter_horizontal = ("flights",)
    

admin.site.register(Comment,CommentAdmin)
admin.site.register(auction_listings, auction_listingsAdmin)
# admin.site.register(Passenger, PassengerAdmin)
