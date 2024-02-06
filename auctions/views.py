from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
import datetime
from .models import User  ,Listing ,Comment,Paid

from django.contrib import messages




def index(request):
    categorie_list_with_paid = Listing.objects.all()
    # # categorie_list_with_paid = Listing.objects.select_related('user_id')
    # auctions = Listing.objects.all().order_by('id').reverse()
    # print(Paid.objects.latest('Listings'))
    # # latest_entry = MyModel.objects.get(id=entry_id)
    # obj=Listing.objects.filter(Listing.objects.all()).all()
    # latest_entry = Paid.objects.order_by('Listings_id').first()
    # print(latest_entry)
    # for i in latest_entry:
    #     print(i)
    
    # subjects=Listing.objects.all()
    # print(subjects)
    # obj=Paid.objects.filter(id__in=subjects)[0:1]
 

    # for i in obj:
    #     print(i.id,i.Listings ,i.Paid_amount)
        
   
        
  
    # categorie_list_with_paid=[]
    return render(request, "auctions/index.html", {'categorie_list':categorie_list_with_paid})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        amount = request.POST["amount"]
        url = request.POST["url"]
        category = request.POST["category"]
        try:
            list = Listing.objects.create(title=title,description=description,amount=amount,url=url,category=category )

            list.save()
            return render(request, "auctions/create_Listing.html",{"meesage":"Creat Sucess"})

        except IntegrityError:
               return render(request, "auctions/create_Listing.html",{"meesage":IntegrityError})
    else:
         return render(request, "auctions/create_Listing.html")


def categories(request):
    categorie_list = Listing.objects.values_list('category').distinct()
    return render(request, "auctions/categories.html" ,{'categorie_list':categorie_list})


def view_categories(request,categori):
    categorie_list =Listing.objects.all().filter(category=categori)
    return render(request, "auctions/view_categories.html",{'categories':categori,'categorie_list':categorie_list})



def listing(request,id):
    categorie_list = Listing.objects.get(pk=id)
    publication = Comment.objects.select_related('user_id').all().values()
    try:
       
       comments =Comment.objects.all().filter(Listing_id=id).values()
       return render(request, "auctions/Listing.html",{'categorie_list':categorie_list ,'Comment':comments} )

    except :
        comments=[]

    return render(request, "auctions/Listing.html",{'categorie_list':categorie_list ,'Comment':comments} )

def add_comment(request): 
    if request.method == "POST":
        title = request.POST["title"]
        comment = request.POST["comment"]
        Listing_id = request.POST["listId"]
        user_id = request.POST["userId"]
        try:
            add_commentes = Comment.objects.create(title=title,comment=comment,Listing_id=Listing_id,user_id=user_id)
            add_commentes.save()
            # return render(request, "auctions/create_Listing.html",{"meesage":"Creat Sucess"})
            return HttpResponseRedirect( reverse("listing", kwargs={"id": Listing_id}))

        except IntegrityError:
               return HttpResponseRedirect( reverse("listing", kwargs={"id": Listing_id},),{"meesage":'Comment not ADD'})
    else:
        return HttpResponseRedirect( reverse("listing", kwargs={"id": Listing_id}))


def paid(request):
    if request.method == "POST":
        Paid_amount = request.POST["amount"]       
        Listings_id = request.POST["paid_listId"]
        user_bids_id = request.POST["paid_userId"]
        amountChek =Listing.objects.all().filter(id=Listings_id).values()
        if  amountChek[0]['amount'] >= float(Paid_amount) or amountChek[0]['endAmont'] >= float(Paid_amount)  :
            messages.success(request, '<p class="alret alert-warning p-3">The entered amount is smaller than the current amount. </p>')
            return HttpResponseRedirect(reverse("listing", kwargs={"id":Listings_id} ))

        try:              
            add_commentes = Paid.objects.create(Paid_amount=Paid_amount, user_bids_id=user_bids_id, Listing_id=Listings_id )
            add_commentes.save()
            
            updt=Listing.objects.filter(id=Listings_id).update(endAmont=Paid_amount)
        
            messages.success(request, '<p class="alret alert-success p-3">Add Paid success. </p>')
            return HttpResponseRedirect(reverse("listing", kwargs={"id":Listings_id} ))
        
        except IntegrityError:
            messages.success(request, '<p class="alret alert-success p-3">Erorr :paid did not add </p>')
            return HttpResponseRedirect(reverse("listing", kwargs={"id":Listings_id} ))
    return HttpResponseRedirect( reverse("index"))
    
def end_paid(request):
    if request.method == "POST":
            
        Listings_id = request.POST["end_listId"]
        Listing.objects.filter(id=Listings_id).update(status="Close")

    return HttpResponseRedirect( reverse("listing", kwargs={"id": Listings_id})) 

def watchlist(request):
    if "watchlist" not in request.session:
               request.session["watchlist"] = []   
    if request.method == "POST":
        Listings_id = request.POST["Watchlist"]


                  
        request.session["watchlist"] += [int(Listings_id)]
        print(request.session["watchlist"])
        categorie_list=getwatchlist(request.session["watchlist"])
        return render(request, "auctions/watchlist.html" ,{'categorie_lists':categorie_list})
    categorie_list=getwatchlist(request.session["watchlist"])
    return render(request, "auctions/watchlist.html" ,{'categorie_lists':categorie_list})


def Romvewatchlist(request):
    if request.method == "POST":
        RomveWatchlist = request.POST["RomveWatchlist"]
        RomveWatchlist=int(RomveWatchlist)
        updat=[]
        for i in request.session["watchlist"]:
           if i != RomveWatchlist:      
             updat += [i]     
        request.session["watchlist"]=[]   
        request.session["watchlist"]+= updat  
   
        # print( request.session["watchlist"]) 
        categorie_list=getwatchlist(request.session["watchlist"])
 
        return render(request, "auctions/watchlist.html" ,{'categorie_lists':categorie_list})
    categorie_list=getwatchlist(request.session["watchlist"])
    return render(request, "auctions/watchlist.html" ,{'categorie_lists':categorie_list})

def getwatchlist(q):
    watclist=[]
    for i in q : 
        watclist += Listing.objects.all().filter(id=i).values()
    return watclist
    