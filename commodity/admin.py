import base64

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
import barcode
from barcode.writer import ImageWriter
from io import BytesIO

from .forms import WriteOffOperationForm, TransferOperationForm
from .models import (
    Product,
    ProductImage,
    ProductAttribute,
    Warehouse,
    Stock,
    ReceivingOperation,
    TransferOperation,
    WriteOffOperation,
    InventoryCheck, TypeProduct,
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'type', # Добавлено отображение типа продукта
        'manufacturer_name',
        'manufacturer_country',
        'manufacturer_code',
        'dimensions',
        'unit_of_measurement',
        'shelf_life_days',
        'barcode',
        'start_price',# Добавлено отображение начальной цены
    )
    search_fields = ('sku', 'name', 'manufacturer_name', 'manufacturer_country', 'barcode')
    list_filter = ('manufacturer_country', 'shelf_life_days', 'type') # Добавлен фильтр по типу продукта
    ordering = ('name',)
    fields = (
        'sku',
        'name',
        'type', # Добавлено поле для выбора типа продукта
        'manufacturer_name',
        'manufacturer_country',
        'manufacturer_code',
        'dimensions',
        'unit_of_measurement',
        'shelf_life_days',
        'barcode',
        'additional_info',
        'start_price', # Добавлено поле начальной цены
        'barcode_image',
    )
    readonly_fields = ('barcode_image',)

    def barcode_image(self, obj):
        if obj.barcode:
            try:
                ean = barcode.get('ean13', obj.barcode, writer=ImageWriter())
                buffer = BytesIO()
                ean.write(buffer)
                base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
                return mark_safe(f'<img src="data:image/png;base64,{base64_image}" alt="Штрих-код" height="150" />')
            except Exception as e:
                return f"Ошибка генерации штрих-кода: {e}"
        return "Штрих-код отсутствует"

    barcode_image.short_description = "Штрих-код"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    search_fields = ('product__name',)
    ordering = ('product',)


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute_name', 'attribute_value')
    search_fields = ('attribute_name', 'attribute_value', 'product__name')
    list_filter = ('attribute_name',)
    ordering = ('attribute_name',)


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')
    ordering = ('name',)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'quantity', 'expiration_date')
    search_fields = ('product__name', 'warehouse__name')
    list_filter = ('warehouse', 'expiration_date')
    ordering = ('product',)


@admin.register(ReceivingOperation)
class ReceivingOperationAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'warehouse',
        'quantity',
        'expiration_date',
        'status',
        'reason',
        'created_at'
    )
    search_fields = ('product__name', 'warehouse__name', 'reason')
    list_filter = ('status', 'expiration_date', 'created_at')
    ordering = ('-created_at',)

@admin.register(TransferOperation)
class TransferOperationAdmin(admin.ModelAdmin):
    form = TransferOperationForm
    list_display = (
        'product',
        'from_warehouse',
        'to_warehouse',
        'quantity',
        'created_at'
    )
    search_fields = ('product__name', 'from_warehouse__name', 'to_warehouse__name')
    list_filter = ('from_warehouse', 'to_warehouse', 'created_at')
    ordering = ('-created_at',)

@admin.register(WriteOffOperation)
class WriteOffOperationAdmin(admin.ModelAdmin):
    form = WriteOffOperationForm
    list_display = (
        'product',
        'warehouse',
        'quantity',
        'reason',
        'comment',
        'created_at'
    )
    search_fields = ('product__name', 'warehouse__name', 'reason', 'comment')
    list_filter = ('reason', 'created_at')
    ordering = ('-created_at',)


@admin.register(InventoryCheck)
class InventoryCheckAdmin(admin.ModelAdmin):
    list_display = ('warehouse', 'date', 'discrepancies', 'created_at')
    search_fields = ('warehouse__name', 'discrepancies')
    list_filter = ('date', 'created_at')
    ordering = ('-date',)


@admin.register(TypeProduct)
class TypeProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'max_percent_of_markdown', 'days_of_markdown', 'max_percent_of_price_change')
    search_fields = ('name', 'description')
    list_filter = ('max_percent_of_markdown', 'days_of_markdown', 'max_percent_of_price_change')
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Скидки', {
            'fields': ('max_percent_of_markdown', 'days_of_markdown')
        }),
        ('Изменение цены', {
            'fields': ('max_percent_of_price_change',)
        }),
    )