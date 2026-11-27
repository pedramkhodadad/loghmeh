from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from .models import Order



@login_required
@require_POST
def restaurant_order_approve(request, order_id):

    if request.user.role != 'owner':
        return HttpResponseForbidden(
            'شما اجازه دسترسی به این بخش را ندارید.'
        )

    order = get_object_or_404(
        Order,
        id=order_id,
        restaurant__owner=request.user
    )

    if order.status != Order.Status.PENDING:
        return HttpResponseForbidden(
            'این سفارش در وضعیت قابل تأیید نیست.'
        )

    order.status = Order.Status.PREPARING
    order.save(update_fields=['status'])

    return redirect(
        'orders:restaurant_order_detail',
        order_id=order.id
    )


@login_required
@require_POST
def restaurant_order_cancel(request, order_id):

    if request.user.role != 'owner':
        return HttpResponseForbidden(
            'شما اجازه دسترسی به این بخش را ندارید.'
        )

    order = get_object_or_404(
        Order,
        id=order_id,
        restaurant__owner=request.user
    )

    if order.status != Order.Status.PENDING:
        return HttpResponseForbidden(
            'این سفارش در وضعیت قابل لغو نیست.'
        )

    order.status = Order.Status.CANCELLED
    order.save(update_fields=['status'])

    return redirect(
        'orders:restaurant_order_detail',
        order_id=order.id
    )



@login_required
def restaurant_order_list(request):

    if request.user.role != 'owner':
        return HttpResponseForbidden(
            'شما اجازه دسترسی به این بخش را ندارید.'
        )

    orders = Order.objects.filter(
        restaurant__owner=request.user
    ).select_related(
        'restaurant',
        'customer'
    ).prefetch_related(
        'items__food'
    ).order_by(
        '-created_at'
    )

    context = {
        'orders': orders,
    }

    return render(
        request,
        'orders/order_list.html',
        context
    )
@login_required
def restaurant_order_detail(request, order_id):

    if request.user.role != 'owner':
        return HttpResponseForbidden(
            'شما اجازه دسترسی به این بخش را ندارید.'
        )

    order = get_object_or_404(
        Order,
        id=order_id,
        restaurant__owner=request.user
    )

    order_items = order.items.select_related(
        'food'
    ).all()

    context = {
        'order': order,
        'order_items': order_items,
    }

    return render(
        request,
        'orders/order_detail.html',
        context
    )


@login_required
@require_POST
def restaurant_order_send(request, order_id):

    if request.user.role != 'owner':
        return HttpResponseForbidden(
            'شما اجازه دسترسی به این بخش را ندارید.'
        )

    order = get_object_or_404(
        Order,
        id=order_id,
        restaurant__owner=request.user
    )

    if order.status != Order.Status.PREPARING:
        return HttpResponseForbidden(
            'این سفارش قابل ارسال نیست.'
        )

    order.status = Order.Status.SENT
    order.save(update_fields=['status'])

    return redirect(
        'orders:restaurant_order_detail',
        order_id=order.id
    )


@login_required
@require_POST
def restaurant_order_deliver(request, order_id):

    if request.user.role != 'owner':
        return HttpResponseForbidden(
            'شما اجازه دسترسی به این بخش را ندارید.'
        )

    order = get_object_or_404(
        Order,
        id=order_id,
        restaurant__owner=request.user
    )

    if order.status != Order.Status.SENT:
        return HttpResponseForbidden(
            'این سفارش هنوز ارسال نشده است.'
        )

    order.status = Order.Status.DELIVERED
    order.save(update_fields=['status'])

    return redirect(
        'orders:restaurant_order_detail',
        order_id=order.id
    )
