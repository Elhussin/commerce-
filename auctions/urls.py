from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("categorieView/<str:categori>", views.view_categories, name="categorieView"),
    path("categories", views.categories, name="categories"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("Romvewatchlist", views.Romvewatchlist, name="Romvewatchlist"),
    path("comment", views.add_comment, name="comment"),
    path("paid", views.paid, name="paid"),
     path("endPaid", views.end_paid, name="endPaid"),
    

 
]



      