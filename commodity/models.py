from django.db import models
from django.contrib.auth.models import User

from shared.models.noUpdateMixin import NoUpdateModel
from shared.models.timestampMixin import TimestampMixin
from shared.models.userTrackingMixin import UserTrackingMixin


class TypeProduct(models.Model):
    name = models.CharField(max_length=1000, verbose_name="Название")
    description = models.CharField(max_length=1000, verbose_name="Описание")
    max_percent_of_markdown = models.IntegerField(verbose_name="Максимальный процент скидки")
    days_of_markdown = models.IntegerField(verbose_name="Количество дней скидки")
    max_percent_of_price_change = models.IntegerField(verbose_name="Максимальный процент изменения цены")

    def __str__(self): # Исправлено на str
        return self.name

    class Meta:
        verbose_name = 'Тип продукта' # Русское название в единственном числе
        verbose_name_plural = 'Типы продуктов' # Русское название во множественном числе


class Product(TimestampMixin, UserTrackingMixin):
    sku = models.CharField(max_length=50, unique=True, verbose_name="Артикул")
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    manufacturer_name = models.CharField(max_length=100, verbose_name="Название компании производителя")
    manufacturer_country = models.CharField(max_length=100, verbose_name="Страна производителя")
    manufacturer_code = models.CharField(max_length=50, verbose_name="Код компании изготовителя")
    dimensions = models.CharField(max_length=100, verbose_name="Размеры")
    unit_of_measurement = models.CharField(max_length=50, verbose_name="Единицы измерения")
    shelf_life_days = models.PositiveIntegerField(verbose_name="Технический срок годности (дни)")
    barcode = models.CharField(max_length=50, unique=True, verbose_name="Штрих-код")
    additional_info = models.TextField(blank=True, null=True, verbose_name="Дополнительная информация")
    type = models.ForeignKey(TypeProduct, on_delete=models.CASCADE,null=True, verbose_name="Категория товара")
    start_price = models.DecimalField(max_digits=10, decimal_places=2,null=True, verbose_name="Начальная цена")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Товар")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение")

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"

    def __str__(self):
        return f"Изображение для {self.product.name}"


class ProductAttribute(models.Model):
    """
    Модель для хранения характеристик конкретного товара:
    - product: связь с товаром
    - attribute_name: название характеристики (например, цвет, размер и т.д.)
    - attribute_value: значение характеристики
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attributes", verbose_name="Товар")
    attribute_name = models.CharField(max_length=100, verbose_name="Название характеристики")
    attribute_value = models.CharField(max_length=200, verbose_name="Значение характеристики")

    class Meta:
        verbose_name = "Характеристика товара"
        verbose_name_plural = "Характеристики товаров"

    def __str__(self):
        return f"{self.attribute_name}: {self.attribute_value} ({self.product.name})"


class Warehouse(models.Model):
    """
    Модель для описания склада:
    - name: название или код склада
    - location: адрес или местоположение
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name="Местоположение")

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"

    def __str__(self):
        return self.name


class Stock(models.Model):
    """
    Модель для учёта остатков товаров на складах:
    - product: какой товар хранится
    - warehouse: на каком складе
    - quantity: текущее количество единиц товара
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_items", verbose_name="Товар")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="stock_items", verbose_name="Склад")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    expiration_date = models.DateField(null=True, blank=True, verbose_name="Срок годности")

    class Meta:
        unique_together = ('product', 'warehouse')
        verbose_name = "Остаток"
        verbose_name_plural = "Остатки"

    def __str__(self):
        return f"{self.product.name} на {self.warehouse.name}: {self.quantity}"


class ReceivingOperation(TimestampMixin, UserTrackingMixin, NoUpdateModel):
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    warehouse = models.ForeignKey(
        "Warehouse",
        on_delete=models.CASCADE,
        verbose_name="Склад"
    )
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    expiration_date = models.DateField(verbose_name="Срок годности")
    status = models.CharField(
        max_length=50,
        choices=[
            ("accepted", "Принято"),
            ("rejected", "Отклонено")
        ],
        verbose_name="Статус"
    )
    reason = models.TextField(
        blank=True,
        null=True,
        verbose_name="Причина отклонения"
    )

    class Meta:
        verbose_name = "Приемка товара"
        verbose_name_plural = "Приемки товаров"

    def __str__(self):
        return f"Приемка: {self.product.name} ({self.quantity} шт.) - {self.get_status_display()}"


class TransferOperation(TimestampMixin, UserTrackingMixin, NoUpdateModel):
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    from_warehouse = models.ForeignKey(
        "Warehouse",
        on_delete=models.CASCADE,
        related_name="transfers_out",
        verbose_name="Из склада"
    )
    to_warehouse = models.ForeignKey(
        "Warehouse",
        on_delete=models.CASCADE,
        related_name="transfers_in",
        verbose_name="В склад"
    )
    quantity = models.PositiveIntegerField(verbose_name="Количество")

    class Meta:
        verbose_name = "Перемещение товара"
        verbose_name_plural = "Перемещения товаров"

    def __str__(self):
        return (
            f"Перемещение: {self.product.name}, "
            f"{self.quantity} шт. из {self.from_warehouse.name} в {self.to_warehouse.name}"
        )


class WriteOffOperation(TimestampMixin, UserTrackingMixin, NoUpdateModel):
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    warehouse = models.ForeignKey(
        "Warehouse",
        on_delete=models.CASCADE,
        verbose_name="Склад"
    )
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    reason = models.CharField(max_length=100, verbose_name="Причина списания")
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Комментарий"
    )

    class Meta:
        verbose_name = "Списание товара"
        verbose_name_plural = "Списания товаров"

    def __str__(self):
        return f"Списание: {self.product.name} ({self.quantity} шт.), причина: {self.reason}"


class InventoryCheck(TimestampMixin, UserTrackingMixin):
    warehouse = models.ForeignKey(
        "Warehouse",
        on_delete=models.CASCADE,
        verbose_name="Склад"
    )
    date = models.DateField(verbose_name="Дата инвентаризации")
    discrepancies = models.TextField(
        blank=True,
        null=True,
        verbose_name="Несоответствия"
    )

    class Meta:
        verbose_name = "Инвентаризация"
        verbose_name_plural = "Инвентаризации"

    def __str__(self):
        return f"Инвентаризация склада {self.warehouse.name} от {self.date}"
