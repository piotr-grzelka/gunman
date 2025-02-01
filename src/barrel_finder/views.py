from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from src.barrel_finder.models import Ad, Category


def index_view(request):
    latest = Ad.objects.order_by('-date').all()[:8]
    return render(request, 'barrel_finder/index.html', {
        'latest': latest,
        'categories': Category.objects.all()
    })


def list_all_view(request):
    page = request.GET.get('page', 1)
    items = Ad.objects.order_by('-date').all()
    paginator = Paginator(items, 25)
    page_obj = paginator.get_page(page)
    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page)

    return render(request, 'barrel_finder/list-all.html', {
        'page_obj': page_obj,
    })


def list_search_view(request):
    query = request.GET.get('query')
    page = request.GET.get('page', 1)

    if not query:
        return redirect('/')

    q = Q(name__icontains=query) | Q(description__icontains=query)

    items = Ad.objects.filter(q).order_by('-date').all()
    paginator = Paginator(items, 25)
    page_obj = paginator.get_page(page)
    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page)

    return render(request, 'barrel_finder/list-search.html', {
        'page_obj': page_obj,
        'query': query
    })


def list_category_view(request, category_slug):
    page = request.GET.get('page', 1)
    category = get_object_or_404(Category, slug=category_slug)
    items = Ad.objects.filter(category=category).order_by('-date').all()
    paginator = Paginator(items, 25)
    page_obj = paginator.get_page(page)
    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page)

    return render(request, 'barrel_finder/list-category.html', {
        'page_obj': page_obj,
        'category': category
    })


def ad_view(request, ad_slug):
    ad = get_object_or_404(Ad, slug=ad_slug)
    return render(request, 'barrel_finder/ad.html', {'ad': ad})


def privacy(request):
    return render(request, 'barrel_finder/privacy.html')


def about(request):
    return render(request, 'barrel_finder/about.html')
