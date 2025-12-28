from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),  # Default home route
    path('home/<slug:category_slug>/', views.home_view, name='home_by_category'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.update_profile_view, name='profile'),
    path('category/<str:title>/', views.category_view, name='category'),
    path('cart/', views.cart_view, name='cart'),
     path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"), 
    path('product/<int:pk>/', views.product_detail_view, name='product'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),
    path('cart/add/<int:product_id>/', views.create_cart_item, name='add_to_cart'),
    # path('upload/', views.upload_image, name='upload_image'),
    # path('images/', views.view_images, name='view_images'),
    # path('images/delete/<int:image_id>/', views.delete_image, name='delete_image'),
    # path('cart/update/<str:cart_id>/', views.update_cart_view, name='update_cart'),
    # path('cart/delete/<str:cart_id>/', views.delete_cart_item, name='delete_cart'),
]



