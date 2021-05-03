from django.db import models
from django.utils.crypto import get_random_string


def f():
    d = get_random_string(
                length=10,
                allowed_chars='1234567890'
        )
    return int(d)


# Create your models here.
class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name="Внешний ID пользователя",
        unique=True,
    )
    name = models.TextField(
        verbose_name="Имя пользователя",
    )

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


class Message(models.Model):
    profile = models.ForeignKey(
        to='ugc.Profile',
        verbose_name='Профиль',
        on_delete=models.PROTECT,
    )
    product = models.ForeignKey(
        to='ugc.Product',
        verbose_name="Внешний ID товара",
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(
        verbose_name="Время получения",
        auto_now_add=True,
    )

    def __str__(self):
        return f'Сообщение {self.pk} {self.profile}'

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Product(models.Model):
    external_id = models.CharField(
        max_length=255,
        verbose_name="Внешний ID товара",
        unique=True,
    )
    product_url = models.CharField(
        max_length=255,
        verbose_name="Полный url товара",
    )
    product_name = models.CharField(
        max_length=255,
        verbose_name='Полное название товара',
        default=''
    )
    old_price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0.0,
        verbose_name="Старая цена",
    )
    current_price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0.0,
        verbose_name="Текущая цена",
    )
    average_price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0.0,
        verbose_name="Минимальная цена за 6 месяцев",
    )
    operator_price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0.0,
        verbose_name='Цена предоставленная оператором'
    )
    operator_message = models.TextField(
        max_length=255,
        verbose_name='Сообщение от оператора',
        default=''
    )
    cashback = models.IntegerField(
        verbose_name='Кэшбек от Онлайнера',
        default=0
    )

    def __str__(self):
        return f'#{self.external_id}'

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ActiveMonitoring(models.Model):
    id_monitoring = models.PositiveIntegerField(
        default=f,
        verbose_name='ID мониторинга',
        unique=True
    )
    profile = models.ForeignKey(
        to='ugc.Profile',
        verbose_name='Профиль',
        on_delete=models.PROTECT,
    )
    text = models.ForeignKey(
        to='ugc.Product',
        verbose_name="Внешний ID товара",
        on_delete=models.PROTECT,
    )
    waiting_price = models.PositiveIntegerField(
        verbose_name='Ожидаемая цена пользователя',
        help_text='Если указан 0, значит пользователь не указал желаемую цену',
        default=0,
    )
    time_published = models.DateTimeField(
        verbose_name='Время добавления',
        auto_now_add=True,
    )

    def __str__(self):
        return f'#{self.id_monitoring}'

    class Meta:
        verbose_name = "Активный мониторинг"
        verbose_name_plural = "Активный мониторинг"


class PassiveMonitoring(models.Model):
    profile = models.ForeignKey(
        to='ugc.Profile',
        verbose_name='Профиль',
        on_delete=models.PROTECT,
    )
    text = models.ForeignKey(
        to='ugc.Product',
        verbose_name="Внешний ID товара",
        on_delete=models.PROTECT,
    )
    monitoring_percent = models.PositiveIntegerField(
        verbose_name="Процент мониторинга",
    )

    def __str__(self):
        return f'Запись {self.pk} {self.profile} {self.text}'

    class Meta:
        verbose_name = "Пассивный мониторинг"
        verbose_name_plural = "Пассивный мониторинг"


# class OperatorMessage(models.Model):
#     monitoring = models.ForeignKey(
#         to='ugc.ActiveMonitoring',
#         verbose_name='ID мониторинга',
#         on_delete=models.PROTECT
#     )
#     # product = models.ForeignKey(
#     #     to='ugc.Product',
#     #     verbose_name='ID товара',
#     #     on_delete=models.PROTECT
#     # )
#     operator_price = models.DecimalField(
#         verbose_name='Цена оператора',
#         decimal_places=2,
#         max_digits=10,
#         default=0,
#     )
#     operator_url = models.CharField(
#         verbose_name='Сайт с товаром',
#         max_length=255,
#         default='-',
#     )
#
#     def __str__(self):
#         return f'Сообщение рассылка {self.pk}'
#
#     class Meta:
#         verbose_name = "Сообщение рассылка"
#         verbose_name_plural = "Сообщения рассылка"


# class OperatorMessageWaiting(models.Model):
#     monitoring = models.ForeignKey(
#         to='ugc.ActiveMonitoring',
#         verbose_name='ID мониторинга',
#         on_delete=models.PROTECT
#     )
#     # product = models.ForeignKey(
#     #     to='ugc.Product',
#     #     verbose_name='ID товара',
#     #     on_delete=models.PROTECT
#     # )
#     operator_price = models.DecimalField(
#         verbose_name='Цена оператора',
#         decimal_places=2,
#         max_digits=10,
#         default=0.00,
#     )
#     operator_url = models.CharField(
#         verbose_name='Сайт с товаром',
#         max_length=255,
#         default='-',
#     )
#
#     def __str__(self):
#         return f'Сообщение ожидание {self.pk}'
#
#     class Meta:
#         verbose_name = "Сообщение ожидание"
#         verbose_name_plural = "Сообщения ожидания"
