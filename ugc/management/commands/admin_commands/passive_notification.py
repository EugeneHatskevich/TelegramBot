from telegram.ext import CallbackContext
from ugc.management.commands import bot
from ugc.models import PassiveMonitoring


def passive_notification(context: CallbackContext):
    """Функция для уведомлений по пассивному мониторингу"""
    passive_monitoring_list = PassiveMonitoring.objects.all()
    for i in passive_monitoring_list:
        product_id = i.text
        chat_id = i.profile.external_id
        change = 100 - (product_id.current_price / product_id.old_price * 100)
        if change >= bot.all_monitoring_percent:
            context.bot.send_message(chat_id, i.text.product_url)
            context.bot.send_message(chat_id,
                                     text=f'Привет! Ты просил не беспокоить, но произошло неординарное событие и товар,'
                                          f' о котором ты меня спрашивал сильно подешевел! Вот это удача. '
                                          f'Его стоимость составляет {product_id.current_price} рублей. '
                                          f'Рассказать где его приобрести по такой цене?')
            i.delete()
