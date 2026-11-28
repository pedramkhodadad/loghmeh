from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from restaurants.models import Food
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from discounts.models import Discount
from .models import Order, OrderItem


def cart_detail(request):
    cart = request.session.get("cart", {})
    cart_items = []
    total_price = 0

    for food_id, quantity in cart.items():
        food = get_object_or_404(Food, id=food_id)

        item_total = food.price * quantity
        total_price += item_total

        cart_items.append({
            "food": food,
            "quantity": quantity,
            "item_total": item_total,
        })

    return render(request, "orders/cart.html", {
        "cart_items": cart_items,
        "total_price": total_price,
    })


@require_POST
def cart_add(request, food_id):
    food = get_object_or_404(Food, id=food_id, is_available=True)

    cart = request.session.get("cart", {})

    # بررسی اینکه سبد خرید متعلق به رستوران دیگری نباشد
    if cart:
        first_food_id = next(iter(cart))
        first_food = get_object_or_404(Food, id=first_food_id)

        if first_food.restaurant_id != food.restaurant_id:
            messages.warning(
                request,
                "سبد خرید شما شامل غذاهای رستوران دیگری است. ابتدا سبد خرید فعلی را خالی کنید."
            )
            return redirect("restaurants:detail", pk=food.restaurant.pk)

    food_id = str(food.id)

    cart[food_id] = cart.get(food_id, 0) + 1

    request.session["cart"] = cart
    request.session.modified = True

    messages.success(request, f"{food.name} به سبد خرید اضافه شد.")

    return redirect("restaurants:detail", pk=food.restaurant.pk)

def cart_remove(request, food_id):
    cart = request.session.get("cart", {})
    food_id = str(food_id)

    if food_id in cart:
        del cart[food_id]
        request.session["cart"] = cart
        request.session.modified = True

    return redirect("orders:cart")

@require_POST
def cart_update(request, food_id):
    cart = request.session.get("cart", {})
    food_id = str(food_id)

    if food_id in cart:
        action = request.POST.get("action")

        if action == "increase":
            cart[food_id] += 1

        elif action == "decrease":
            cart[food_id] -= 1

            if cart[food_id] <= 0:
                del cart[food_id]

        request.session["cart"] = cart
        request.session.modified = True

    return redirect("orders:cart")

@login_required
def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        messages.warning(request, "سبد خرید شما خالی است.")
        return redirect("orders:cart")

    cart_items = []
    total_price = 0
    restaurant = None

    for food_id, quantity in cart.items():
        food = get_object_or_404(Food, id=food_id)

        if not food.is_available:
            messages.error(request, f"{food.name} دیگر موجود نیست.")
            return redirect("orders:cart")

        if restaurant is None:
            restaurant = food.restaurant

        elif restaurant.id != food.restaurant_id:
            messages.error(request, "سبد خرید نمی‌تواند شامل غذاهای چند رستوران باشد.")
            return redirect("orders:cart")

        item_total = food.price * quantity
        total_price += item_total

        cart_items.append({
            "food": food,
            "quantity": quantity,
            "item_total": item_total,
        })

    discount_amount = 0
    discount = None
    final_price = total_price

    if request.method == "POST":
        address = request.POST.get("delivery_address", "").strip()
        discount_code = request.POST.get("discount_code", "").strip()

        if not address:
            messages.error(request, "لطفاً آدرس تحویل را وارد کنید.")
            return redirect("orders:checkout")

        if discount_code:
            discount = Discount.objects.filter(
                restaurant=restaurant,
                code__iexact=discount_code,
                is_active=True,
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now()
            ).first()

            if not discount:
                messages.error(request, "کد تخفیف نامعتبر یا منقضی شده است.")
                return redirect("orders:checkout")

            discount_amount = total_price * discount.percentage / 100
            final_price = total_price - discount_amount

        with transaction.atomic():
            order = Order.objects.create(
                customer=request.user,
                restaurant=restaurant,
                discount=discount,
                total_price=final_price,
                delivery_address=address,
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    food=item["food"],
                    quantity=item["quantity"],
                    price=item["food"].price,
                )

        request.session["cart"] = {}
        messages.success(request, "سفارش شما با موفقیت ثبت شد.")

        return redirect("orders:my_orders")

    return render(request, "orders/checkout.html", {
        "cart_items": cart_items,
        "total_price": total_price,
        "discount_amount": discount_amount,
        "final_price": final_price,
    })


@login_required
def my_orders(request):
    orders = Order.objects.filter(
        customer=request.user
    ).prefetch_related(
        "items__food"
    ).select_related(
        "restaurant"
    ).order_by("-created_at")

    return render(request, "orders/my_orders.html", {
        "orders": orders
    })
