from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Restaurant


def restaurant_list(request):
    query = request.GET.get("q", "").strip()

    restaurants = Restaurant.objects.filter(is_active=True)

    if query:
        restaurants = restaurants.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(foods__name__icontains=query)
        ).distinct()

    return render(
        request,
        "restaurants/restaurant_list.html",
        {
            "restaurants": restaurants,
            "query": query
        }
    )


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(
        Restaurant,
        pk=pk,
        is_active=True
    )

    foods = restaurant.foods.filter(is_available=True)

    return render(
        request,
        "restaurants/restaurant_detail.html",
        {
            "restaurant": restaurant,
            "foods": foods
        }
    )
