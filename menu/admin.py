from django.contrib import admin

from .models import Category, MenuItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order", "item_count")
    list_editable = ("display_order",)
    search_fields = ("name",)
    ordering = ("display_order", "name")

    @admin.display(description="Menu items")
    def item_count(self, category):
        return category.items.count()


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price")
    list_editable = ("price",)
    list_filter = ("category",)
    search_fields = ("name", "description", "category__name")
    autocomplete_fields = ("category",)
    list_select_related = ("category",)
    list_per_page = 50
    ordering = ("category__display_order", "name")
