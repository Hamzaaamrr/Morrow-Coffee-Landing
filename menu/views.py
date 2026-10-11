from django.db import DatabaseError
from django.shortcuts import render

from .models import Category


def home(request):
    menu_error = False
    try:
        categories = Category.objects.prefetch_related("items").all()
        # Evaluate inside the guarded block so database connection errors reach the template.
        categories = list(categories)
        for category in categories:
            category.ordered_items = category.items.all()
    except DatabaseError:
        categories = []
        menu_error = True

    return render(request, "menu/home.html", {"categories": categories, "menu_error": menu_error})
