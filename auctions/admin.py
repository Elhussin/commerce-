from django.contrib import admin

# Register your models here.
from .models import Listing, Paid ,Comment
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("__str__", "category")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "comment")
# class PassengerAdmin(admin.ModelAdmin):
#     filter_horizontal = ("flights",)
    

admin.site.register(Comment,CommentAdmin)
admin.site.register(Listing, ListingAdmin)
# admin.site.register(Passenger, PassengerAdmin)
