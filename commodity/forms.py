from django import forms
from .models import WriteOffOperation, Stock, Product, Warehouse, TransferOperation


class WriteOffOperationForm(forms.ModelForm):
    class Meta:
        model = WriteOffOperation
        fields = ['product', 'warehouse', 'quantity', 'reason', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ограничиваем выбор товаров только теми, которые есть в остатках
        self.fields['product'].queryset = Product.objects.filter(stock_items__isnull=False).distinct()

        # Ограничиваем выбор склада только теми, которые имеют остатки для выбранного товара
        if 'product' in self.data:
            try:
                product_id = int(self.data.get('product'))
                self.fields['warehouse'].queryset = Warehouse.objects.filter(stock_items__product_id=product_id).distinct()
            except (ValueError, TypeError):
                pass  # игнорируем ошибки преобразования

        elif self.instance.pk:
            self.fields['warehouse'].queryset = Warehouse.objects.filter(stock_items__product=self.instance.product).distinct()

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        product = self.cleaned_data.get('product')
        warehouse = self.cleaned_data.get('warehouse')

        if product and warehouse:
            stock = Stock.objects.filter(product=product, warehouse=warehouse).first()
            if stock and quantity > stock.quantity:
                raise forms.ValidationError(f"Максимальное количество для списания: {stock.quantity}")

        return quantity


class TransferOperationForm(forms.ModelForm):
    class Meta:
        model = TransferOperation
        fields = ['product', 'from_warehouse', 'to_warehouse', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ограничиваем выбор товаров только теми, которые есть в остатках
        self.fields['product'].queryset = Product.objects.filter(stock_items__isnull=False).distinct()

        # Ограничиваем выбор склада, откуда товар перемещается, только теми, которые имеют остатки для выбранного товара
        if 'product' in self.data:
            try:
                product_id = int(self.data.get('product'))
                self.fields['from_warehouse'].queryset = Warehouse.objects.filter(stock_items__product_id=product_id).distinct()
            except (ValueError, TypeError):
                pass  # игнорируем ошибки преобразования

        elif self.instance.pk:
            self.fields['from_warehouse'].queryset = Warehouse.objects.filter(stock_items__product=self.instance.product).distinct()

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        product = self.cleaned_data.get('product')
        from_warehouse = self.cleaned_data.get('from_warehouse')

        if product and from_warehouse:
            stock = Stock.objects.filter(product=product, warehouse=from_warehouse).first()
            if stock and quantity > stock.quantity:
                raise forms.ValidationError(f"Максимальное количество для перемещения: {stock.quantity}")

        return quantity