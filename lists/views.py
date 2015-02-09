from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import List, Item

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def view_list(request, list_id):
    list_ = List.objects.get(id = list_id)
    return render(request, 'list.html', { 'list' : list_ })

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(list = list_, text = request.POST['item_text'])
    return redirect('/lists/%d/' % (list_.id,))

def add_item(request, list_id):
    list_ = List.objects.get(id = list_id)
    new_item = Item.objects.create(list = list_, text = request.POST['item_text'])
    return redirect('/lists/%d/' % (list_.id,))

def reset_lists(request):
    Item.objects.filter().delete()
    List.objects.filter().delete()
    return redirect('/')
