from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User  ,Listing ,Comment,Paid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from django import forms
from . import addform
    
def index(request):
    categorie_list_with_paid = Listing.objects.select_related('user')
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


# @login_required
@login_required(login_url='/login')
def create_listing(request):
    # get form 
    if request.method == "POST":
        form = addform.creatlist(request.POST)
        user = request.user.id
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            amount = form.cleaned_data["amount"]
            url = request.POST["url"]
            category = request.POST["category"]
    
        #  add default value to null url or category
        if not url :
            url ='null'
        if category == 'null':
            category='No Category Listed'
        # sav data in database
        try:
            list = Listing.objects.create(title=title,description=description,amount=amount,url=url,category=category,user_id=user,endAmont=amount)
            list.save()
            # return render(request, 'auctions/add.html', {'form': form})
            return render(request, "auctions/creatList.html",{"meesage":"Creat Sucess" ,'form': form})
        # error massege 
        except :
               return render(request, "auctions/creatList.html",{"error":"failed to create this listing",'form': form})
    else:
         form = addform.creatlist()
         return render(request, "auctions/creatList.html",{'form': form})


@login_required(login_url='/login')
def categories(request):
    #  a sort catogry from data base 
    categorie_list = Listing.objects.values_list('category').distinct()
    return render(request, "auctions/categories.html" ,{'categorie_list':categorie_list})


@login_required(login_url='/login')
def view_categories(request,categori):
    #  view all items under select category
    categorie_list =Listing.objects.all().filter(category=categori)
    return render(request, "auctions/index.html",{'categories':categori,'categorie_list':categorie_list})



def listing(request,id):
    #  view listing  
    #  get datt for seleactd list 
       categorie_list = Listing.objects.select_related('user').get(pk=id)
    #  get all comment for this list 
       comments=Comment.objects.select_related('user').filter(Listing_id=id)
    #    git all bid to this list 
       Toatal_Baid= Paid.objects.select_related('user_bids').filter(Listing_id=id)
    #  get last bid for this list 
       current=Toatal_Baid.last()
    # mesag view 
       return render(request, "auctions/Listing.html",{'categorie_list':categorie_list ,'Comment':comments ,
                                                       'Toatal_Baid':Toatal_Baid ,'current':current } )



@login_required(login_url='/login')
def add_comment(request): 
    # get form 
    if request.method == "POST":
        title = request.POST["title"]
        comment = request.POST["comment"]
        Listing_id = request.POST["listId"]
        user_id = request.POST["userId"]
        
        # insert data to comment table 
        try:
            add_commentes = Comment.objects.create(title=title,comment=comment,Listing_id=Listing_id,user_id=user_id)
            add_commentes.save()
            return HttpResponseRedirect( reverse("listing", kwargs={"id": Listing_id}))
        except :
        # error message 
               return HttpResponseRedirect( reverse("listing", kwargs={"id": Listing_id},),{"meesage":'Comment not ADD'})
    else:
        return HttpResponseRedirect( reverse("index"))

@login_required(login_url='/login')
def paid(request):
    # gei bid form 
    if request.method == "POST":
        Paid_amount = request.POST["amount"]       
        Listings_id = request.POST["paid_listId"]
        user_bids_id = request.POST["paid_userId"]
        amountChek =Listing.objects.all().filter(id=Listings_id).values()
    #   confirm bid not less than current amount
        if  amountChek[0]['amount'] >= float(Paid_amount) or amountChek[0]['endAmont'] >= float(Paid_amount)  :
            messages.success(request, '<p class="alret alert-warning p-3">The entered amount is smaller than the current amount. </p>')
            return HttpResponseRedirect(reverse("listing", kwargs={"id":Listings_id} ))
    #   updat bid in paid tabel  also ubdat end amount in listing tabel 
        try:              
            add_commentes = Paid.objects.create(Paid_amount=Paid_amount, user_bids_id=user_bids_id, Listing_id=Listings_id )
            add_commentes.save()     
            Listing.objects.filter(id=Listings_id).update(endAmont=Paid_amount ,updated_at=datetime.datetime.now())
            messages.success(request, '<p class="alret alert-success p-3">Add Paid success. </p>')
            return HttpResponseRedirect(reverse("listing", kwargs={"id":Listings_id} ))
    # error message
        except:
            messages.success(request, '<p class="alret alert-success p-3">Erorr :paid did not add </p>')
            return HttpResponseRedirect(reverse("listing", kwargs={"id":Listings_id} ))
    return HttpResponseRedirect( reverse("index"))

@login_required(login_url='/login')   
def end_paid(request):
    if request.method == "POST":
    #  close listing 
        Listings_id = request.POST["end_listId"]
        Listing.objects.filter(id=Listings_id).update(status="Close")
        return HttpResponseRedirect( reverse("listing", kwargs={"id": Listings_id})) 
    return HttpResponseRedirect( reverse("index"))

@login_required(login_url='/login')
def watchlist(request):
    #  creat session for watchlist
    if "watchlist" not in request.session:
        request.session["watchlist"] = []  
    # get watchlist form  
    if request.method == "POST":
        Listings_id = request.POST["Watchlist"]      
    #  add iteam to watchlist  
        request.session["watchlist"] += [int(Listings_id)]
    # get  list for all items by  watchlist function  
        categorie_list=getwatchlist(request.session["watchlist"])
        return HttpResponseRedirect( reverse("listing", kwargs={"id": Listings_id}))
    
    categorie_list=getwatchlist(request.session["watchlist"])
    return render(request, "auctions/index.html" ,{'categorie_list':categorie_list , 'Watch_list':'Watch list'})

@login_required(login_url='/login')
def Romvewatchlist(request):
    if request.method == "POST":
        RomveWatchlist = request.POST["RomveWatchlist"]
        RomveWatchlist=int(RomveWatchlist)
        # romve iteam from watchlist session
        updat=[]
        for i in request.session["watchlist"]:
           if i != RomveWatchlist:      
             updat += [i]     
        request.session["watchlist"]=[]   
        request.session["watchlist"]+= updat  
        return HttpResponseRedirect( reverse("listing", kwargs={"id": RomveWatchlist}))
    
    categorie_list=getwatchlist(request.session["watchlist"])
    return render(request, "auctions/index.html" ,{'categorie_list':categorie_list , 'Watch_list':'Watch list'})

# 
def getwatchlist(q):
    # get all data from database for items saved in watchlist session
    watclist=[]
    for i in q : 
        watclist += Listing.objects.all().filter(id=i).values()
    return watclist


