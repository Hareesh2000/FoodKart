from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.context_processors import get_restaurant

from accounts.utils import check_role_vendor
from menu.forms import CategoryForm, FoodItemForm
from menu.models import Category, FoodItem
from django.contrib import messages

from django.template.defaultfilters import slugify
# Create your views here.

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    restaurant=get_restaurant(request)['restaurant']
    categories=Category.objects.filter(restaurant=restaurant).order_by('created_at')

    context={
        'categories':categories,
    }
    return render(request,'menu/menu_builder.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request,pk=None):
    restaurant=get_restaurant(request)
    category=get_object_or_404(Category,pk=pk)
    fooditems=FoodItem.objects.filter(restaurant=restaurant,category=category)
    context={
        'fooditems':fooditems,
        'category':category,
    }
    return render(request,'menu/fooditems_by_category.html',context)

def add_category(request):
    if request.method=='POST':
        cat_form=CategoryForm(request.POST)
        if cat_form.is_valid():
            category=cat_form.save(commit=False)
            category_name=cat_form.cleaned_data['category_name']
            category.restaurant=get_restaurant(request)
            category.save()
            
            
            category.slug=slugify(category_name)+'-'+str(category.id)
            category.save()
            messages.success(request,'Category added successfully!')
            return redirect('menu_builder')


    else:
        cat_form=CategoryForm()

    context={
        'cat_form':cat_form,
    }
    return render(request,'menu/add_category.html',context)

def edit_category(request,pk=None):
    category=get_object_or_404(Category,pk=pk)
    if request.method=='POST':
        cat_form=CategoryForm(request.POST,instance=category)
        if cat_form.is_valid():
            category=cat_form.save(commit=False)
            category.restaurant=get_restaurant(request)
            category_name=cat_form.cleaned_data['category_name']
            category.slug=slugify(category_name)
            cat_form.save()
            messages.success(request,'Category updated successfully!')
            return redirect('menu_builder')


    else:
        cat_form=CategoryForm(instance=category)

    context={
        'cat_form':cat_form,
        'category':category,
    }
    return render(request,'menu/edit_category.html',context)

def delete_category(request,pk=None):
    category=get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request,"Category has been deleted successfully!")
    return redirect('menu_builder')




def add_fooditem(request):
    if request.method=='POST':
        form=FoodItemForm(request.POST,request.FILES)
        if form.is_valid():
            food=form.save(commit=False)
            food.restaurant=get_restaurant(request)
            food_name=form.cleaned_data['food_name']
            food.slug=slugify(food_name)
            form.save()
            messages.success(request,'Food Item added successfully!')
            return redirect('fooditems_by_category',food.category.id)
    else:
        form=FoodItemForm()
        form.fields['category'].queryset=Category.objects.filter(restaurant=get_restaurant(request))
    context={
        'food_form':form,
    }
    return render(request,'menu/add_fooditem.html',context)



def edit_fooditem(request,pk=None):
    food=get_object_or_404(FoodItem,pk=pk)
    if request.method=='POST':
        form=FoodItemForm(request.POST,request.FILES,instance=food)
        if form.is_valid():
            food=form.save(commit=False)
            food.restaurant=get_restaurant(request)
            food_name=form.cleaned_data['food_name']
            food.slug=slugify(food_name)
            form.save()
            messages.success(request,'Food Item updated successfully!')
            return redirect('fooditems_by_category',food.category.id)


    else:
        form=FoodItemForm(instance=food)
        form.fields['category'].queryset=Category.objects.filter(restaurant=get_restaurant(request))

    context={
        'food_form':form,
        'food':food,
    }
    return render(request,'menu/edit_fooditem.html',context)


def delete_fooditem(request,pk=None):
    food=get_object_or_404(FoodItem,pk=pk)
    food.delete()
    messages.success(request,"Food Item has been deleted successfully!")
    return redirect('fooditems_by_category',food.category.id)
