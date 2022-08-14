#  import send_mail from django.core.mail (we will need this function later).
from unicodedata import name
from django.core.mail import send_mail
from coffeeshops.models import CafeOwner, CoffeeShop, CoffeeShopAddress, Drink
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from utils import create_slug


@receiver(post_save, sender=CafeOwner)
def send_new_owner_email(sender, instance, created, **kwargs):
    if created == True:
        send_mail(
            'New Cafe Owner',
            'A new cafe owner has joined named ' + instance.full_name,
            'sender@test.com',
            ["receiver@test.com"],
            fail_silently=False,
        )


@receiver(pre_save, sender=CoffeeShop)
def slugify_coffee_shop(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


@receiver(post_save, sender=CoffeeShop)
def add_default_address(sender, instance, created, **kwargs):
    if created and not instance.location:
        createdLocation = CoffeeShopAddress.objects.create(
            coffee_shop=instance)
        instance.location = createdLocation
        instance.save()


@receiver(post_delete, sender=CoffeeShopAddress)
def restore_default_address(sender, instance, **kwargs):
    # Get the coffee shop from the deleted instance (hint: use the related name coffee_shop) and store it in a variable called coffee_shop.
    coffee_shop = instance.coffee_shop
    # Create a new CoffeeShopAddress instance.
    defualtLocation = CoffeeShopAddress.objects.create()
    # Set coffee_shop.location equal to the new CoffeeShopAddress object you've created.
    coffee_shop.location = defualtLocation
    # Save your coffee_shop instance.
    coffee_shop.save()


@receiver(pre_save, sender=Drink)
def slugify_coffee_shop(sender, instance, **kwargs):
    # Set instance.is_out_of_stock to False if instance.stock_count is greater than zero and vice-versa.
    if instance.stock_count > 0:
        instance.is_out_of_stock = False
    else:
        instance.is_out_of_stock = True
