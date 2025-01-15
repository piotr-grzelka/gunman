from src.barrel_finder.models import Category


def barrel_finder_categories(request):
    return {'bf_categories': Category.objects.all()}