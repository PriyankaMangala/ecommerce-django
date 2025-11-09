Django E-Commerce Web App

Live demo: https://ecommerce-django-ozr1.onrender.com

Features
- Product listing, cart, checkout
- Admin panel to add/edit products (images uploaded to Cloudinary)
- Deployed on Render

How to test
1. Visit the live URL above.
2. Admin panel: https://ecommerce-django-ozr1.onrender.com/admin/
   - (If you used the DB pushed to GitHub, use the credentials you created)
3. Add a product in admin and upload an image — it will be stored on Cloudinary.

Run locally
```bash
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
