from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm

def order_list(request):
    orders = Order.objects.prefetch_related('items').all().order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})



def order_add(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/order_add.html', {'form': form})

def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/order_edit.html', {'form': form})

def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.delete()
        return redirect('order_list')
    return render(request, 'orders/order_confirm_delete.html', {'order': order})

from django.shortcuts import get_object_or_404

def orderitem_list_by_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all()
    return render(request, 'orders/orderitem_list.html', {'order_items': order_items, 'order': order})

def orderitem_list(request):
    order_items = OrderItem.objects.all().order_by('-order__created_at')
    return render(request, 'orders/orderitem_list.html', {'order_items': order_items})

def orderitem_add(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            order_item.save()
            return redirect('orderitem_list_by_order', order_id=order.id)
    else:
        form = OrderItemForm()
    return render(request, 'orders/orderitem_add.html', {'form': form, 'order': order})

def orderitem_edit(request, pk):
    order_item = get_object_or_404(OrderItem, pk=pk)
    if request.method == "POST":
        form = OrderItemForm(request.POST, instance=order_item)
        if form.is_valid():
            form.save()
            return redirect('orderitem_list_by_order', order_id=order_item.order.id)  # Burada yönlendirmeyi güncelliyoruz
    else:
        form = OrderItemForm(instance=order_item)
    return render(request, 'orders/orderitem_edit.html', {'form': form, 'order_item': order_item})

def orderitem_delete(request, pk):
    order_item = get_object_or_404(OrderItem, pk=pk)
    order_id = order_item.order.id
    if request.method == "POST":
        order_item.delete()
        return redirect('orderitem_list_by_order', order_id=order_id)  # Yönlendirmeyi güncelliyoruz
    return render(request, 'orders/orderitem_confirm_delete.html', {'order_item': order_item})
