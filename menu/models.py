from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q


# Keep these helpers importable because prior migration files reference them.
def validate_image_size(image):
    max_size = 5 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError("Images must be 5 MB or smaller.")


def validate_image_content(image):
    from PIL import Image, UnidentifiedImageError

    try:
        image.seek(0)
        with Image.open(image) as decoded_image:
            if decoded_image.width * decoded_image.height > 40_000_000:
                raise ValidationError("Images must be 40 megapixels or smaller.")
            decoded_image.verify()
    except (UnidentifiedImageError, OSError, SyntaxError, Image.DecompressionBombError):
        raise ValidationError("Upload a valid image file.")
    finally:
        image.seek(0)


class Category(models.Model):
    name = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "name", "pk")
        verbose_name_plural = "categories"

    def clean(self):
        super().clean()
        self.name = self.name.strip()
        if not self.name:
            raise ValidationError({"name": "Enter a category name."})

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="items")

    class Meta:
        ordering = ("name", "pk")
        constraints = [
            models.CheckConstraint(condition=Q(price__gte=0), name="menu_item_price_nonnegative"),
        ]

    def clean(self):
        super().clean()
        self.name = self.name.strip()
        self.description = self.description.strip()
        if not self.name:
            raise ValidationError({"name": "Enter a menu item name."})

    def __str__(self):
        return self.name
