
from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Discount
from .forms import DiscountForm


def owner_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if getattr(request.user, 'role', None) != 'owner':
            return HttpResponseForbidden(
                'شما اجازه دسترسی به این بخش را ندارید.'
            )

        return view_func(request, *args, **kwargs)

    return wrapper


@login_required
@owner_required
def discount_list(request):

    discounts = Discount.objects.filter(
        restaurant__owner=request.user
    ).select_related('restaurant').order_by('-start_date')

    return render(
        request,
        'discounts/discount_list.html',
        {
            'discounts': discounts
        }
    )


@login_required
@owner_required
def discount_create(request):

    if request.method == 'POST':

        form = DiscountForm(
            request.POST,
            user=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'کد تخفیف با موفقیت ایجاد شد.'
            )

            return redirect('discounts:discount_list')

    else:

        form = DiscountForm(user=request.user)

    return render(
        request,
        'discounts/discount_form.html',
        {
            'form': form,
            'title': 'ایجاد کد تخفیف'
        }
    )


@login_required
@owner_required
def discount_update(request, pk):

    discount = get_object_or_404(
        Discount,
        pk=pk,
        restaurant__owner=request.user
    )

    if request.method == 'POST':

        form = DiscountForm(
            request.POST,
            instance=discount,
            user=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'کد تخفیف با موفقیت ویرایش شد.'
            )

            return redirect('discounts:discount_list')

    else:

        form = DiscountForm(
            instance=discount,
            user=request.user
        )

    return render(
        request,
        'discounts/discount_form.html',
        {
            'form': form,
            'discount': discount,
            'title': 'ویرایش کد تخفیف'
        }
    )


@login_required
@owner_required
@require_POST
def discount_toggle(request, pk):

    discount = get_object_or_404(
        Discount,
        pk=pk,
        restaurant__owner=request.user
    )

    discount.is_active = not discount.is_active

    discount.save(update_fields=['is_active'])

    messages.success(
        request,
        'وضعیت کد تخفیف تغییر کرد.'
    )

    return redirect('discounts:discount_list')
