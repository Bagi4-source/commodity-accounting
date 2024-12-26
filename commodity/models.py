from django.db import models

class Product(models.Model):
    """
    Модель для описания товара:
    - sku: уникальный идентификатор или код
    - name: название товара
    - description: дополнительное текстовое описание
    - price: цена товара
    """
    sku = models.CharField(max_length=50, unique=True, verbose_name="Артикул")
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Цена")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


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