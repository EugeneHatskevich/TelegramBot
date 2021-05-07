from telegram.ext import CallbackContext
from ugc.management.commands import bot
from ugc.models import PassiveMonitoring


def passive_notification(context: CallbackContext):
    """Функция для уведомлений по пассивному мониторингу"""
    passive_monitoring_list = PassiveMonitoring.objects.all()
    for i in passive_monitoring_list:
        product_id = i.text
        chat_id = i.profile.external_id
        try:
            change_default = 100 - (product_id.current_price / product_id.old_price * 100)
            change_operator = 100 - (product_id.operator_price / product_id.old_price * 100)
            if (change_default >= bot.all_monitoring_percent and change_operator >= bot.all_monitoring_percent
                or change_operator >= bot.all_monitoring_percent) and (
                    product_id.operator_price and product_id.current_price):
                context.bot.send_message(chat_id,
                                         text=f'Привет! Ты просил не беспокоить, но произошло неординарное событие и '
                                              f'товар, '
                                              f' о котором ты меня спрашивал сильно подешевел! Вот это удача. '
                                              f'Мы можем предложить {product_id.product_name} за '
                                              f'{product_id.operator_price} ' \
                                              f'{product_id.operator_message}, в каталоге онлайнер ' \
                                              f'он представлен по минимальной цене {product_id.current_price}')
            elif (change_default >= bot.all_monitoring_percent) and product_id.current_price:
                context.bot.send_message(chat_id,
                                         text=f'Привет! Ты просил не беспокоить, но произошло неординарное событие и товар,'
                                              f' о котором ты меня спрашивал сильно подешевел! Вот это удача. '
                                              f'{product_id.product_name} с минимальной ценой представлен в каталоге онлайнер' \
                                              f'{product_id.product_url}.')
        except ZeroDivisionError:
            continue
