from django.db import models

from commodity.models import Warehouse, Product
from django.utils import timezone


class PriceTagType(models.Model):
    tag_type_name = models.CharField(max_length=100, unique=True, verbose_name="Название типа ценника")
    tag_type_description = models.TextField(blank=True, null=True, verbose_name="Описание типа ценника")
    class Meta:
        verbose_name = "Тип ценника"
        verbose_name_plural = "Типы ценников"
    def __str__(self):
        return self.tag_type_name


class Employee(models.Model):  # ЗАМЕНИТЬ //ЭТО ВРЕМЕННО
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic or ''}"


class PriceList(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник")
    class Meta:
        verbose_name = "Список ценников"
        verbose_name_plural = "Списки ценников"
    def __str__(self):
        return f"Список ценников от {self.creation_date.strftime('%Y-%m-%d %H:%M')}"


class PriceTagProduct(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="Склад")
    price_list = models.ForeignKey(PriceList, on_delete=models.CASCADE, null=True, verbose_name="Список ценников")
    tag_type = models.ForeignKey(PriceTagType, on_delete=models.CASCADE, verbose_name="Тип ценника")
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, verbose_name="Продукт")
    set_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Установленная цена")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status_stop_list = models.BooleanField(null=True, blank=True, verbose_name="Статус нахождения в стоп-листе")
    class Meta:
        verbose_name = "Ценник"
        verbose_name_plural = "Ценники"

    def __str__(self):
        return f"Ценник {self.tag_type.tag_type_name} для {self.product.name}"

    def save(self, *args, **kwargs):
        if not self.price_list:
            try:
                self.price_list = PriceList.objects.all().filter(creation_date__date=timezone.now().date()).latest(
                    'creation_date')
            except PriceList.DoesNotExist:
                pass
        super().save(*args, **kwargs)


class RequestStopList(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    price_tag = models.ForeignKey(PriceTagProduct, on_delete=models.CASCADE, verbose_name="Ценник продукта")
    num_req_stop_list = models.PositiveIntegerField(verbose_name="Номер обращения", editable=False)
    reason = models.TextField(verbose_name="Причина добавления в стоп-лист")

    def save(self, *args, **kwargs):
        if not self.num_req_stop_list:
            last_request = RequestStopList.objects.all().order_by('-num_req_stop_list').first()
            self.num_req_stop_list = (last_request.num_req_stop_list if last_request else 0) + 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Запрос в стоп-лист"
        verbose_name_plural = "Запросы в стоп-лист"

    def __str__(self):
        return f"Запрос №{self.num_req_stop_list}"


class StatusResponse(models.Model):
    status_name = models.CharField(max_length=100, verbose_name="Название статуса")
    status_description = models.CharField(max_length=1000, verbose_name="Описание статуса")

    def __str__(self):
        return self.status_name

    class Meta:
        verbose_name = "Статус ответа"
        verbose_name_plural = "Статусы ответов"


class HCResponse(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="ID сотрудника")
    response_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата прихода ответа")
    status_response = models.ForeignKey(StatusResponse, on_delete=models.CASCADE, verbose_name="ID статуса ответа")

    def __str__(self):
        return f"Ответ ГК({self.employee.first_name}, {self.employee.last_name}, {self.response_date.strftime('%Y-%m-%d %H:%M')}, {self.status_response.status_name})"

    class Meta:
        db_table = 'hc_response'
        verbose_name = 'Ответ ГК'
        verbose_name_plural = 'Ответы ГК'



class HCRequest(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    commodity_expert = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Эксперт по товарам")
    status_response = models.ForeignKey(StatusResponse, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Статус ответа от ГК")
    response = models.ForeignKey(HCResponse, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ответ от ГК")
    quantity_product = models.PositiveIntegerField(verbose_name="Количество продукта")
    num_req_stop_list = models.ForeignKey(RequestStopList, on_delete=models.CASCADE, verbose_name="Номер в стоп-листе")


    def __str__(self):
        return f"Запрос к ГК от {self.creation_date.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Запрос к ГК"
        verbose_name_plural = "Запросы к ГК"


class Action(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    action_name = models.CharField(max_length=1000, verbose_name="Название акции")
    action_description = models.CharField(max_length=1000, verbose_name="Описание акции")
    action_start_date = models.DateTimeField(verbose_name="Дата начала акции")
    action_end_date = models.DateTimeField(verbose_name="Дата окончания акции")
    percent = models.PositiveIntegerField(null=True, verbose_name='Процент скидки')

    def __str__(self):
        return self.action_name

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"