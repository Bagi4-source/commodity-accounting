from django.db import models
from django.contrib.auth.models import User

from commodity.middleware import get_current_user


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True


class UserTrackingMixin(models.Model):
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name="Изменено пользователем")

    def save(self, *args, **kwargs):
        self.modified_by = get_current_user()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Product(TimestampMixin, UserTrackingMixin):
    sku = models.CharField(max_length=50, unique=True, verbose_name="Артикул")
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    manufacturer_name = models.CharField(max_length=100, verbose_name="Название компании производителя")
    manufacturer_country = models.CharField(max_length=100, verbose_name="Страна производителя")
    manufacturer_code = models.CharField(max_length=50, verbose_name="Код компании изготовителя")
    dimensions = models.CharField(max_length=100, verbose_name="Размеры")
    unit_of_measurement = models.CharField(max_length=50, verbose_name="Единицы измерения")
    shelf_life_days = models.PositiveIntegerField(verbose_name="Технический срок годности (дни)")
    barcode = models.CharField(max_length=50, verbose_name="Штрих-код")
    additional_info = models.TextField(blank=True, null=True, verbose_name="Дополнительная информация")

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

    class Meta:
        unique_together = ('product', 'warehouse')
        verbose_name = "Остаток"
        verbose_name_plural = "Остатки"

    def __str__(self):
        return f"{self.product.name} на {self.warehouse.name}: {self.quantity}"
