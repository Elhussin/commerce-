from django.contrib import admin

# Register your models here.
from .models import Listing, Paid ,Comment
    
class ListingAdmin(admin.ModelAdmin):
    list_display = ("__str__", "category")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "comment")

class PaidAdmin(admin.ModelAdmin):
    # filter_horizontal=("Paid_amount",)
    list_display = ("__str__", "Paid_amount")
   

admin.site.register(Comment,CommentAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Paid, PaidAdmin)

