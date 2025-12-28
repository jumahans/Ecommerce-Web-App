from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import UserUpdateForm, UserProfileForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from .models import Product,Category, MyCart, Order, OrderItem, UserProfile
from reportlab.pdfgen import canvas
from .forms import MyCartForm
from .forms import UserUpdateForm, UserProfileForm
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def index_view(request):
    return render(request, "index.html")

def home_view(request):
    categories = Category.objects.all()
    category_products = {cat.title: Product.objects.filter(category=cat) for cat in categories}
    return render(request, 'home.html', {"category_products": category_products})


@csrf_exempt
def login_view(request):
    error_message = ''
    if request.method == 'POST':
        username = request.POST.get('username') or request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get("next") or 'home'
            return redirect(next_url)
        error_message = "invalid credentials"
    return render(request, "index.html", {'error_message':error_message})



@login_required
def profile_view(request):
    user = request.user
    profile = user.profile  

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile
    })

@csrf_exempt
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    return redirect('home')   

from django.http import JsonResponse

def create_cart_item(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        cart_item, created = MyCart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={"quantity": quantity, "price": product.price, "total_products": quantity},
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.total_products = cart_item.quantity
            cart_item.save()
        messages.success(request, "Item added to cart!")
        return redirect('product', pk=product.product_id)
    return redirect('product', pk=product.product_id)

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(MyCart, id=item_id, user=request.user)
    cart_item.delete()
    return redirect("cart")

@login_required
def update_profile_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form, 'profile': profile})


def category_view(request, title):
    category = get_object_or_404(Category, title = title)
    product = Product.objects.filter(category=category)
    return render(request, 'home.html', {'category':category}, {'product':product})

from django.shortcuts import render
from .models import MyCart

def cart_view(request):
    cart_items = MyCart.objects.filter(user=request.user)
    total_price = sum(item.price * item.quantity for item in cart_items)
    context = {
        "cart_items": cart_items,
        "total_price": total_price,
    }
    return render(request, 'cart.html', context)





def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)  
    return render(request, 'product_details.html', {'product': product})


@login_required
def checkout(request):
    cart_items = MyCart.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('cart')
    
    # Calculate total
    total_price = sum(item.price * item.quantity for item in cart_items)
    
    if request.method == "POST":
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code', '')
        notes = request.POST.get('notes', '')
        payment_method = request.POST.get('payment_method')
        
        # ✅ Validate payment method
        if not payment_method:
            messages.error(request, "Please select a payment method!")
            context = {
                'cart_items': cart_items,
                'total_price': total_price,
            }
            return render(request, "checkout.html", context)
        
        # ✅ Validate required fields
        if not all([first_name, last_name, email, phone, address, city]):
            messages.error(request, "Please fill in all required fields!")
            context = {
                'cart_items': cart_items,
                'total_price': total_price,
            }
            return render(request, "checkout.html", context)
        
        try:
            # Create order with shipping information
            order = Order.objects.create(
                user=request.user,
                customer=request.user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                postal_code=postal_code,
                notes=notes,
                payment_method=payment_method or 'cod',  # ✅ Fallback to 'cod'
                payment_status='Processing',
                order_status='Processing',
                total_price=total_price,
            )
            
            # Create order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity,
                    total_products=len(cart_items),
                    tracking_id=generate_tracking_id(),
                    order_status='Pending',
                )
            
            # Clear cart
            cart_items.delete()
            
            messages.success(request, f"Order {order.order_id} placed successfully!")
            return redirect('order_confirmation', order_id=order.id)
            
        except Exception as e:
            messages.error(request, f"Error processing order: {str(e)}")
            context = {
                'cart_items': cart_items,
                'total_price': total_price,
            }
            return render(request, "checkout.html", context)
    
    # GET request - show checkout form
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, "checkout.html", context)


def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'checkout.html', context)

def download_invoice(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return generate_invoice(order)

import uuid

def generate_tracking_id():
    return str(uuid.uuid4())[:12]  # Generate a 12-character unique tracking ID



def generate_invoice(order):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="invoice_{order.id}.pdf"'  # ✅ Fixed typo
    
    pdf = canvas.Canvas(response)
    pdf.drawString(100, 800, f"Invoice for Order #{order.id}")
    pdf.drawString(100, 780, f"Total: ${order.total_price}")
    pdf.showPage()
    pdf.save()

    return response  # ✅ This will return the generated PDF as a downloadable file
# @login_required 
# def upload_image(request): 
#     if request.method == 'POST': 
#         form = UserImageForm(request.POST, request.FILES) 
#         if form.is_valid(): 
#             image = form.save(commit=False) 
#             image.user = request.user 
#             image.save() 
#             messages.success(request, 'Image uploaded successfully!') 
#             return redirect('profile') 
#         else: form = UserImageForm()
        
#     return render(request, 'profile.html', {"form": form})

# @login_required
# def view_images(request):
#     images = UserImage.objects.filter(user=request.user).order_by('-uploaded_at')
#     return render(request, 'myapp/view_images.html', {'images': images})


# @login_required 
# def delete_image(request, image_id): 
#     image = get_object_or_404(UserImage, id=image_id, user=request.user)
#     if request.method == 'POST':
#         image.image.delete() 
#         image.delete()        
#         messages.success(request, 'Image deleted successfully!')
#         return redirect('view_images')

#     return render(request, 'profile.html', {'image': imag

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})