from django.shortcuts import render, redirect

from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    requested_list = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': requested_list})


def new_list(request):
    new_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=new_list)
    return redirect('/lists/%d/' % (new_list.id))


def add_item(request, list_id):
    requested_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=requested_list)
    return redirect('/lists/%d/' % (requested_list.id))