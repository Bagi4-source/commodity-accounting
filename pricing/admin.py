from django.contrib import admin
from .models import HCResponse, StatusResponse, HCRequest, Action
from .models import PriceTagProduct, PriceTagType, PriceList, RequestStopList

@admin.register(PriceTagProduct)
class PriceTagProductAdmin(admin.ModelAdmin):
    list_display = (
        'warehouse',
        'price_list',
        'tag_type',
        'name_with_barcode',  # Новое поле для отображения с штрихкодом
        'set_price',
        'creation_date',
        'status_stop_list',
    )
    search_fields = (
    'product__name', 'product__sku', 'warehouse__name', 'tag_type__tag_type_name')  # Изменено для поиска по имени продукта
    list_filter = ('warehouse', 'price_list', 'tag_type', 'status_stop_list', 'creation_date')
    ordering = ('-creation_date',)
    fields = (
        'warehouse',
        'price_list',
        'tag_type',
        'product',  # Оставляем поле name для выбора
        'set_price',
        'status_stop_list',
    )
    def name_with_barcode(self, obj):
        try:
            barcode_text = obj.product.barcode
            if barcode_text:
                return f"{obj.product.name} ({barcode_text})"
            else:
                return obj.product.name
        except AttributeError:
            return " - "

    name_with_barcode.short_description = "Продукт (Штрихкод)"
    name_with_barcode.admin_order_field = 'product__name'

@admin.register(PriceTagType)
class PriceTagTypeAdmin(admin.ModelAdmin):
    list_display = ('tag_type_name', 'tag_type_description')
    search_fields = ('tag_type_name', 'tag_type_description')
    fields = ('tag_type_name', 'tag_type_description')



@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    list_display = ('creation_date', 'employee')
    search_fields = ('employee__fio',)
    list_filter = ('creation_date', 'employee')
    fields = ('creation_date', 'employee')
    readonly_fields = ('creation_date',)
    autocomplete_fields = ['employee']


@admin.register(RequestStopList)
class RequestStopListAdmin(admin.ModelAdmin):
    list_display = ('num_req_stop_list', 'price_tag', 'creation_date', 'reason')
    readonly_fields = ('creation_date', 'num_req_stop_list')
    search_fields = ('num_req_stop_list',  'reason')
    list_filter = ('creation_date',)


@admin.register(HCResponse)
class HCResponseAdmin(admin.ModelAdmin):
    list_display = ('employee', 'response_date', 'status_response')
    search_fields = ('employee__fio', 'status_response__status_name')
    list_filter = ('response_date', 'status_response_id')
    ordering = ('response_date',)

@admin.register(StatusResponse)
class StatusResponseAdmin(admin.ModelAdmin):
    list_display = ('status_name', 'status_description')
    search_fields = ('status_name',)
    list_filter = ('status_name',)
    ordering = ('status_name',)

@admin.register(HCRequest)
class HCRequestAdmin(admin.ModelAdmin):
    list_display = (
        'creation_date',
        'commodity_expert',
        'status_response',
        'response',
        'quantity_product',
        'num_req_stop_list')
    search_fields = (
        'creation_date',
        'commodity_expert__fio',
        'status_response__status_name',
        'response__employee__fio',
    )
    list_filter = ('creation_date', 'status_response', 'commodity_expert', 'num_req_stop_list')
    ordering = ('creation_date',)
    fields = (
        'commodity_expert',
        'status_response',
        'response',
        'quantity_product',
        'num_req_stop_list'
    )

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('product', 'action_name', 'action_start_date', 'action_end_date', 'percent')
    search_fields = ('action_name', 'product__name', 'percent')
    list_filter = ('action_start_date', 'action_end_date')
    ordering = ('action_start_date',)
    fields = ('product', 'action_name', 'action_start_date', 'action_end_date', 'percent')


