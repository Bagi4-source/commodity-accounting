from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import ReceivingOperation, WriteOffOperation, TransferOperation, Stock


@receiver(post_save, sender=ReceivingOperation)
def update_stock_on_receiving(sender, instance, created, **kwargs):
    if not created:
        return

    product = instance.product
    warehouse = instance.warehouse
    quantity_received = instance.quantity

    stock, stock_created = Stock.objects.get_or_create(
        product=product,
        warehouse=warehouse,
        defaults={'quantity': quantity_received}
    )

    if instance.status == "accepted":
        stock.quantity += quantity_received
        stock.save()


@receiver(post_save, sender=WriteOffOperation)
def validate_and_update_stock_on_write_off(sender, instance, **kwargs):
    product = instance.product
    warehouse = instance.warehouse
    quantity_to_write_off = instance.quantity

    try:
        stock = Stock.objects.get(product=product, warehouse=warehouse)
        if stock.quantity < quantity_to_write_off:
            raise ValidationError("Недостаточно товара на складе для списания.")
        # Уменьшаем количество в остатках
        stock.quantity -= quantity_to_write_off
        if stock.quantity == 0:
            stock.delete()
        else:
            stock.save()
    except Stock.DoesNotExist:
        raise ValidationError("Товар отсутствует на складе, списание невозможно.")


@receiver(post_save, sender=TransferOperation)
def update_stock_on_transfer(sender, instance, created, **kwargs):
    product = instance.product
    from_warehouse = instance.from_warehouse
    to_warehouse = instance.to_warehouse
    quantity_to_transfer = instance.quantity

    # Уменьшаем количество на складе, откуда товар перемещается
    try:
        from_stock = Stock.objects.get(product=product, warehouse=from_warehouse)
        if from_stock.quantity < quantity_to_transfer:
            raise ValidationError("Недостаточно товара на складе для перемещения.")
        from_stock.quantity -= quantity_to_transfer

        if from_stock.quantity == 0:
            from_stock.delete()
        else:
            from_stock.save()
    except Stock.DoesNotExist:
        raise ValidationError("Товар отсутствует на складе, перемещение невозможно.")

    # Увеличиваем количество на складе, куда товар перемещается
    to_stock, to_stock_created = Stock.objects.get_or_create(
        product=product,
        warehouse=to_warehouse,
        defaults={'quantity': quantity_to_transfer}
    )

    if not to_stock_created:
        to_stock.quantity += quantity_to_transfer
        to_stock.save()
