# QuickEats 🍔

A fully responsive food ordering web application built with Python and Django. Users can browse a menu, add items to a cart, and place orders via Cash on Delivery or Online Payment. Restaurant owners manage everything through a customised admin panel.

---

## Features

- **User Authentication** — Register, login, and logout securely using Django's built-in authentication system
- **Food Menu** — Browse 15 food items across 5 categories with real photos
- **Search & Filter** — Search food items by name and filter by category
- **Add to Cart** — Add items, update quantity, remove items with live cart count in navbar
- **Snapshot Pricing** — OrderItem stores the price at the moment of ordering. If the restaurant changes a price later, historical orders remain accurate. A deliberate data integrity decision.
- **Checkout System** — Enter delivery address and phone number before placing an order
- **Payment Options** — Cash on Delivery or Mock Online Payment gateway
- **Order History** — View all past orders with status, items, and totals
- **Admin Panel** — Restaurant owner can add/edit food items with photos, manage categories, and update order status from Pending to Delivered

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | Python 3.12 + Django 6.0.3 | Server, routing, business logic |
| Frontend | HTML5 + CSS3 + Bootstrap 5 | UI and responsive design |
| Database | SQLite | Local data storage |
| Fonts | Google Fonts (Playfair Display + Plus Jakarta Sans) | Typography |
| Icons | Bootstrap Icons | UI icons |
| Auth | Django built-in auth | User login/register/logout |

---

## Database Design

Six models power QuickEats:

```
Category     → stores food categories (Burgers, Pizza, Biryani...)
FoodItem     → stores food items with price, description, image
Cart         → one cart per user (OneToOne with User)
CartItem     → items inside the cart with quantity
Order        → a placed order with address, phone, payment method
OrderItem    → items inside an order with snapshot price
```

**Key design decision:** `Cart` uses a `OneToOneField` with `User` — each user has exactly one cart, never multiple. `OrderItem` stores price as a snapshot at order time — not a live reference to `FoodItem.price`. This prevents billing errors if prices change after an order is placed.

---

## How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/ramiz748/QuickEats.git
cd QuickEats

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install django pillow python-decouple

# 4. Create .env file in root folder
# Add: SECRET_KEY=your-secret-key
#      DEBUG=True
#      ALLOWED_HOSTS=*

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create admin account
python manage.py createsuperuser

# 7. Load sample food data
python manage.py shell < seed_data.py

# 8. Run the server
python manage.py runserver
```

Open `http://127.0.0.1:8000` in your browser.

Admin panel: `http://127.0.0.1:8000/admin/`

---

## Project Structure

```
QuickEats/
├── core/                  ← main app
│   ├── models.py          ← 6 database models
│   ├── views.py           ← 13 view functions
│   ├── urls.py            ← 14 URL routes
│   ├── admin.py           ← customised admin panel
│   ├── forms.py           ← register and checkout forms
│   └── context_processors.py ← live cart count for navbar
├── foodorder/             ← project config
│   ├── settings.py
│   └── urls.py
├── templates/             ← 9 HTML templates
├── static/css/            ← custom styles
├── manage.py
└── seed_data.py           ← loads 15 sample food items
```

---

## What I Learned

Building QuickEats taught me how a real web application is structured from the ground up — database design, URL routing, form validation, session-based authentication, and admin customisation. The most important lesson was thinking beyond just making things work — understanding WHY certain decisions exist, like snapshot pricing and the Post/Redirect/Get pattern to prevent duplicate order submissions.

---

## Future Improvements

- Razorpay live payment integration
- Real-time order tracking
- Email confirmation after order placement
- REST API with Django REST Framework for mobile app support
- Deploy on Railway or Render

---

## Author

**Ramiz Raja**
- GitHub: [@ramiz748](https://github.com/ramiz748)
- Project: [QuickEats](https://github.com/ramiz748/QuickEats)

---

*Built with Python & Django — 2026*
