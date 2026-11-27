
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant
from .forms import RestaurantForm
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models.deletion import ProtectedError
from .models import Restaurant, Food
from .forms import FoodForm

def owner_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if request.user.role != 'owner':
            return HttpResponseForbidden(
                'شما اجازه دسترسی به این بخش را ندارید.'
            )

        return view_func(request, *args, **kwargs)

    return wrapper


@login_required
@owner_required
def restaurant_list(request):

    restaurants = Restaurant.objects.filter(
        owner=request.user
    ).order_by('-created_at')

    return render(
        request,
        'restaurants/restaurant_list.html',
        {'restaurants': restaurants}
    )


@login_required
@owner_required
def restaurant_create(request):

    if request.method == 'POST':

        form = RestaurantForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            restaurant = form.save(commit=False)

            restaurant.owner = request.user

            restaurant.save()

            return redirect('restaurants:restaurant_list')

    else:

        form = RestaurantForm()

    return render(
        request,
        'restaurants/restaurant_form.html',
        {'form': form}
    )


@login_required
@owner_required
def restaurant_detail(request, pk):

    restaurant = get_object_or_404(
        Restaurant,
        pk=pk,
        owner=request.user
    )

    return render(
        request,
        'restaurants/restaurant_detail.html',
        {'restaurant': restaurant}
    )

@login_required
@owner_required
def restaurant_owner_list(request):

    restaurants = Restaurant.objects.filter(
        owner=request.user
    ).order_by('-created_at')

    return render(
        request,
        'restaurants/restaurant_list.html',
        {'restaurants': restaurants}
    )

@login_required
@owner_required
def restaurant_update(request, pk):

    restaurant = get_object_or_404(
        Restaurant,
        pk=pk,
        owner=request.user
    )

    if request.method == 'POST':

        form = RestaurantForm(
            request.POST,
            request.FILES,
            instance=restaurant
        )

        if form.is_valid():

            form.save()

            return redirect('restaurants:restaurant_list')

    else:

        form = RestaurantForm(instance=restaurant)

    return render(
        request,
        'restaurants/restaurant_form.html',
        {
            'form': form,
            'restaurant': restaurant
        }
    )


@login_required
@owner_required
def restaurant_delete(request, pk):

    restaurant = get_object_or_404(
        Restaurant,
        pk=pk,
        owner=request.user
    )

    if request.method == 'POST':

        restaurant.delete()

        return redirect('restaurants:restaurant_list')

    return render(
        request,
        'restaurants/restaurant_confirm_delete.html',
        {'restaurant': restaurant}
    )

@login_required
def food_list(request, restaurant_id):

    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id,
        owner=request.user
    )

    foods = Food.objects.filter(
        restaurant=restaurant
    )

    return render(
        request,
        'restaurants/food_list.html',
        {
            'restaurant': restaurant,
            'foods': foods
        }
    )

@login_required
def food_create(request, restaurant_id):

    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id,
        owner=request.user
    )

    if request.method == 'POST':

        form = FoodForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            food = form.save(commit=False)
            food.restaurant = restaurant
            food.save()

            messages.success(request, 'غذا با موفقیت اضافه شد.')

            return redirect(
                'restaurants:food_list',
                restaurant_id=restaurant.id
            )

    else:
        form = FoodForm()

    return render(
        request,
        'restaurants/food_form.html',
        {
            'form': form,
            'restaurant': restaurant,
            'title': 'افزودن غذای جدید'
        }
    )

@login_required
def food_update(request, restaurant_id, food_id):

    food = get_object_or_404(
        Food,
        id=food_id,
        restaurant__id=restaurant_id,
        restaurant__owner=request.user
    )

    if request.method == 'POST':

        form = FoodForm(
            request.POST,
            request.FILES,
            instance=food
        )

        if form.is_valid():

            form.save()

            messages.success(request, 'اطلاعات غذا ویرایش شد.')

            return redirect(
                'restaurants:food_list',
                restaurant_id=restaurant_id
            )

    else:
        form = FoodForm(instance=food)

    return render(
        request,
        'restaurants/food_form.html',
        {
            'form': form,
            'restaurant': food.restaurant,
            'title': 'ویرایش غذا'
        }
    )

@login_required
def food_delete(request, restaurant_id, food_id):

    food = get_object_or_404(
        Food,
        id=food_id,
        restaurant__id=restaurant_id,
        restaurant__owner=request.user
    )

    if request.method == 'POST':

        try:
            food.delete()
            messages.success(request, 'غذا حذف شد.')

        except ProtectedError:
            messages.error(
                request,
                'این غذا در سفارش‌های قبلی استفاده شده و قابل حذف نیست. آن را ناموجود کنید.'
            )

        return redirect(
            'restaurants:food_list',
            restaurant_id=restaurant_id
        )

    return render(
        request,
        'restaurants/food_confirm_delete.html',
        {
            'food': food,
            'restaurant': food.restaurant
        }
    )

@login_required
@require_POST
def food_toggle_availability(request, restaurant_id, food_id):

    food = get_object_or_404(
        Food,
        id=food_id,
        restaurant__id=restaurant_id,
        restaurant__owner=request.user
    )

    food.is_available = not food.is_available
    food.save(update_fields=['is_available'])

    return redirect(
        'restaurants:food_list',
        restaurant_id=restaurant_id
    )

