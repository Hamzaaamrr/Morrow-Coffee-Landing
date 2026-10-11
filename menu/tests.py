from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Category, MenuItem


class PublicMenuTests(TestCase):
    def test_public_page_renders_database_menu_without_removed_fields(self):
        category = Category.objects.create(name="Coffee", display_order=1)
        MenuItem.objects.create(
            name="Oat latte",
            description="Espresso with oat milk",
            price="4.50",
            category=category,
        )

        response = self.client.get(reverse("menu:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Coffee")
        self.assertContains(response, "Oat latte")
        self.assertContains(response, "Espresso with oat milk")
        self.assertContains(response, "4.50")
        self.assertNotContains(response, "Currently unavailable")
        self.assertNotContains(response, "menu-item-image")
        self.assertContains(response, 'data-scroll-reveal="lift"')
        self.assertContains(response, 'data-scroll-reveal="photo"')

    def test_menu_items_are_ordered_by_name(self):
        category = Category.objects.create(name="Coffee")
        MenuItem.objects.create(name="Zebra mocha", price="5.00", category=category)
        MenuItem.objects.create(name="Americano", price="3.00", category=category)

        response = self.client.get(reverse("menu:home"))

        self.assertLess(response.content.index(b"Americano"), response.content.index(b"Zebra mocha"))

    def test_public_page_shows_empty_category_and_no_category_states(self):
        Category.objects.create(name="Desserts")
        response = self.client.get(reverse("menu:home"))
        self.assertContains(response, "More menu items coming soon.")

        Category.objects.all().delete()
        response = self.client.get(reverse("menu:home"))
        self.assertContains(response, "Our menu is being prepared.")


class MenuAdminAccessTests(TestCase):
    def test_admin_requires_login(self):
        response = self.client.get("/admin/menu/menuitem/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response["Location"])

    def test_superuser_can_open_menu_item_manager(self):
        User = get_user_model()
        User.objects.create_superuser(username="manager", email="manager@example.test", password="safe-test-password")
        self.client.login(username="manager", password="safe-test-password")

        response = self.client.get("/admin/menu/menuitem/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Select menu item to change")

    def test_menu_item_model_no_longer_has_removed_fields(self):
        field_names = {field.name for field in MenuItem._meta.get_fields()}

        self.assertTrue({"name", "description", "price", "category"}.issubset(field_names))
        self.assertTrue({"available", "display_order", "image"}.isdisjoint(field_names))
