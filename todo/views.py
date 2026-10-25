from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from .models import Item
from .forms import ItemForm

# Create your views here.
@staff_member_required
def get_todo_list(request):
    items = Item.objects.all()
    contex = {
        'items': items
    }
    return render(request, 'todo/todo_list.html', contex)


@staff_member_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('get_todo_list')
    
    form = ItemForm()
    contex = {
        'form': form
    }
    return render(request, 'todo/add_item.html', contex)


@staff_member_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('get_todo_list')
    form = ItemForm(instance=item)
    context = {
        'form': form
    }
    return render(request, 'todo/edit_item.html', context)


@staff_member_required
@require_POST
def toggle_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.done = not item.done
    item.save()
    return redirect('get_todo_list')

@staff_member_required
@require_POST
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.done = not item.done
    item.delete()
    return redirect('get_todo_list')
