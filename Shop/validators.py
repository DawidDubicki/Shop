from django.core.validators import ValidationError
from .models import Product


def cart_nav_validation(item_id):
    # checking if item_id is integer
    if not item_id:
        raise ValidationError("Item_id doesn't exist")
    try:
        isinstance(int(item_id), int)
    except ValueError:
        raise ValidationError('Item id is not integer')
    # checking if Product with item_id exists
    if not Product.objects.filter(id=item_id).exists():
        raise ValidationError("Product with this id doesn't exist")


