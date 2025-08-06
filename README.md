---
noteId: "ecf252a058c911f0b176514fd594de82"
tags: []

---

# ShopSphere

A modern, animated, and fully-featured e-commerce web application built with Django.

## Features
- User registration and authentication
- Modern, animated, and responsive UI
- Product categories and product detail pages
- Add to cart, cart management, and checkout
- User profile with image upload
- Order history and PDF invoice generation
- Admin dashboard (Django admin + Jazzmin theme)

## Tech Stack
- **Backend:** Django 5.x
- **Frontend:** HTML5, CSS3 (custom + utility classes), JavaScript
- **Database:** SQLite (default, easy to swap for Postgres/MySQL)
- **Styling:** Modern CSS, Google Fonts, CSS animations
- **Admin:** Jazzmin for a beautiful Django admin experience

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd shopsphere/ecom_app
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   Or use Pipenv:
   ```sh
   pipenv install
   pipenv shell
   ```

3. **Apply migrations:**
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser (for admin):**
   ```sh
   python manage.py createsuperuser
   ```

5. **Run the development server:**
   ```sh
   python manage.py runserver
   ```

6. **Access the app:**
   - Open [http://localhost:8000/](http://localhost:8000/) in your browser.
   - Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Project Structure
```
shopsphere/
  ecom_app/
    app/
      models.py
      views.py
      forms.py
      templates/
      static/
      ...
    manage.py
    ...
```

## Customization
- Add your own product images to `app/static/images/products/`.
- Update categories and featured products in the Django admin.
- Tweak styles in `app/static/styles/main.css` for your brand.

## Credits
- Built with Django and love by [Your Name/Team].
- Jazzmin for admin theming.

## License
This project is for educational/demo purposes. For production, add your own license and security hardening. 