from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from accounts.decorators import owner_required
from .models import Order


def _change_status(request, order_id, from_status, to_status, ok_msg, err_msg):
    order = get_object_or_404(Order, id=order_id, restaurant__owner=request.user)
    if order.status != from_status:
        messages.error(request, err_msg)
    else:
        order.status = to_status
        order.save(update_fields=['status'])
        messages.success(request, ok_msg)
    return redirect('orders:restaurant_order_detail', order_id=order.id)


@owner_required
def restaurant_order_list(request):
    orders = (Order.objects.filter(restaurant__owner=request.user)
              .select_related('restaurant', 'customer')
              .prefetch_related('items__food')
              .order_by('-created_at'))
    return render(request, 'orders/order_list.html', {'orders': orders})


@owner_required
def restaurant_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, restaurant__owner=request.user)
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'order_items': order.items.select_related('food'),
    })


@owner_required
@require_POST
def restaurant_order_approve(request, order_id):
    S = Order.Status
    return _change_status(request, order_id, S.PENDING, S.PREPARING,
                          'سفارش تأیید شد.', 'این سفارش در وضعیت قابل تأیید نیست.')


@owner_required
@require_POST
def restaurant_order_cancel(request, order_id):
    S = Order.Status
    return _change_status(request, order_id, S.PENDING, S.CANCELLED,
                          'سفارش لغو شد.', 'این سفارش در وضعیت قابل لغو نیست.')


@owner_required
@require_POST
def restaurant_order_send(request, order_id):
    S = Order.Status
    return _change_status(request, order_id, S.PREPARING, S.SENT,
                          'سفارش ارسال شد.', 'این سفارش قابل ارسال نیست.')


@owner_required
@require_POST
def restaurant_order_deliver(request, order_id):
    S = Order.Status
    return _change_status(request, order_id, S.SENT, S.DELIVERED,
                          'سفارش تحویل داده شد.', 'این سفارش هنوز ارسال نشده است.')