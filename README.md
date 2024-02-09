# commerce-


# Auctions Project

This is a Python Django project for creating an auction website where users can buy and sell items through auctions.

## Table of Contents
- [Features](#features)

- [Installation](#installation)


- [Usage](#usage)


  - [Functionality](#functionality)


    - [Active Listings](#index)

    
    - [Login](#login)

    - [Logout](#logout)

    - [Register](#register)



    - [Create Listing](#createlisting)

    - [Categories](#categories)


    - [Listing View](#listingview)

    - [Comments](#comments)


    - [Bid](#bid)

    - [End Bid](#endbid)

    - [Watchlist](#watchlist)

    - [Remove Watchlist](#removewatchlist)

    
- [Contributing](#contributing)
- [License](#license)


## Features

- User Authentication: 
  - Users can register, log in, and log out.
- Create Listings:
  - Users can create new listings for items they want to sell.
- Categories:
  - Listings can be categorized to make it easier for users to find items.
- View Listings:
  - Users can view all listings or filter them by category.
- Add Comments:
  - Users can add comments to listings.
- Bidding:
  - Users can place bids on listings.

- End Bid:
  - Closing auctions and marking items as paid.
- Watchlist:
  - Users can add listings to their watchlist to keep track of them.
- Remove Watchlist:
  - Users can remove listings from their watchlist.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Elhussin/commerce-.git
   ```
2. Navigate to the project directory:
   ```
    cd auctions-project 
   ```
3. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # for Linux/Mac
   venv\Scripts\activate  # for Windows
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run migrations:
   ```
   python manage.py migrate
   ```
6. Start the development server:
   ```
   python manage.py runserver
   ```
7. Open your web browser and go to http://localhost:8000 to view the application.

## Usage

- Register a new account or log in with an existing one.
- Create listings for items you want to sell.
- Browse listings by category or view all listings.
- Place bids on listings you're interested in.
- Add listings to your watchlist to keep track of them.
- Remove listings from your watchlist.
- Close auctions and mark ite
### Functionality

#### Index

The index page displays  all  available list .

#### Login:
   - Users can log in to their accounts.
   
#### Logout: 
   - Users can log out of their accounts.
   
#### Register: 
   - New users can register for an account.

#### CreateListing: 
   - Authenticated users can create new listings for items they want to sell.

#### Categories: 
   - Listings can be categorized to make it easier for users to browse and find items.

#### ListingView: 
   - Users can view detailed information about a listing, including its description, current bid, and other relevant details.

#### Comments: 
   - Users can add comments to listings to ask questions or provide additional information.

#### Bid: 
   - Users can place bids on listings to participate in auctions.


#### EndBid: 
  - Closing auctions and marking items as paid.

#### Watchlist: 
  - Users can add listings to their watchlist to keep track of items they are interested in.

#### RemoveWatchlist: 
  - Users can remove listings from their watchlist.


## Contributing

Pull requests are welcome. 
## License

Open

