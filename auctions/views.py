from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime
from .models import User  ,auction_listings ,Comment,Paid


def index(request):
    categorie_list = auction_listings.objects.all()
    return render(request, "auctions/index.html", {'categorie_list':categorie_list})


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
            list = auction_listings.objects.create(title=title,description=description,amount=amount,url=url,category=category )

            list.save()
            return render(request, "auctions/create_listing.html",{"meesage":"Creat Sucess"})

        except IntegrityError:
               return render(request, "auctions/create_listing.html",{"meesage":IntegrityError})
    else:
         return render(request, "auctions/create_listing.html")


def categories(request):
    categorie_list = auction_listings.objects.values_list('category').distinct()
    return render(request, "auctions/categories.html" ,{'categorie_list':categorie_list})


def view_categories(request,categori):
    categorie_list =auction_listings.objects.all().filter(category=categori)
    return render(request, "auctions/view_categories.html",{'categories':categori,'categorie_list':categorie_list})



def listing(request,id):
    categorie_list = auction_listings.objects.get(pk=id)
    publication = Comment.objects.select_related('user_id').all().values()
    try:
       
       comments =Comment.objects.all().filter(auction_listings_id=id).values()
       return render(request, "auctions/listing.html",{'categorie_list':categorie_list ,'Comment':comments} )

    except :
        comments=[]

    return render(request, "auctions/listing.html",{'categorie_list':categorie_list ,'Comment':comments} )

def add_comment(request): 
    if request.method == "POST":
        title = request.POST["title"]
        comment = request.POST["comment"]
        auction_listings_id = request.POST["listId"]
        user_id = request.POST["userId"]
        try:
            add_commentes = Comment.objects.create(title=title,comment=comment,auction_listings_id_id=auction_listings_id,user_id_id=user_id)
            add_commentes.save()
            # return render(request, "auctions/create_listing.html",{"meesage":"Creat Sucess"})
            return HttpResponseRedirect( reverse("listing", kwargs={"id": auction_listings_id}))

        except IntegrityError:
               return HttpResponseRedirect( reverse("listing", kwargs={"id": auction_listings_id},),{"meesage":'Comment not ADD'})
    else:
        return HttpResponseRedirect( reverse("listing", kwargs={"id": auction_listings_id}))


def paid(request):
    if request.method == "POST":
        Paid_amount = request.POST["amount"]       
        listings_id = request.POST["paid_listId"]
        user_bids_id = request.POST["paid_userId"]
        amountChek =auction_listings.objects.all().filter(id=listings_id).values()
        if  amountChek[0]['amount'] >= Paid_amount:
            redirect = reverse("listing", kwargs={"id":listings_id})
            return HttpResponseRedirect(redirect,{"meesage":'amount not accepet'})
        add_amount =Paid.objects.all().filter(listings_id=listings_id).values()
        print(add_amount)
        if add_amount :
            for i in add_amount : 
                if i['Paid_amount']>=Paid_amount:
                     redirect = reverse("listing", kwargs={"id":listings_id})
                     return HttpResponseRedirect(redirect,{"meesage":'amount not accepet'})
        try:
            add_commentes = Paid.objects.create(Paid_amount=Paid_amount, user_bids_id_id=user_bids_id, listings_id_id=listings_id )
            add_commentes.save()
            print('done')
            return HttpResponseRedirect( reverse("listing", kwargs={"id": listings_id}))
        
        except IntegrityError:
               return HttpResponseRedirect( reverse("listing", kwargs={"id": listings_id}),{"meesage":'Comment not ADD'}) 
    return HttpResponseRedirect( reverse("index"))
    
def end_paid(request):
    if request.method == "POST":
            
        listings_id = request.POST["end_listId"]
        auction_listings.objects.filter(id=listings_id).update(status="Close")

    return HttpResponseRedirect( reverse("listing", kwargs={"id": listings_id})) 

def watchlist(request):
    if "watchlist" not in request.session:
               request.session["watchlist"] = []   
    if request.method == "POST":
        listings_id = request.POST["Watchlist"]


                  
        request.session["watchlist"] += [int(listings_id)]
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
        watclist += auction_listings.objects.all().filter(id=i).values()
    return watclist
    