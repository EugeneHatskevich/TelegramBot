from ugc.models import ActiveMonitoring
import datetime


def daily_notification(context):
    """Функция для ежедневного могиторинга"""
    active_monitoring_list = ActiveMonitoring.objects.all()
    for i in active_monitoring_list:
        product_id = i.text
        chat_id = i.profile.external_id
        actually = str(i.time_published).split('-')[2].split()[0]
        now = str(datetime.datetime.today()).split('-')[2].split()[0]
        result_time = int(now) - int(actually)
        if result_time in [1, -27, -28, -29, -30]:
            context.bot.send_message(chat_id, i.text.product_url)
            if product_id.current_price > product_id.old_price:
                context.bot.send_message(chat_id,
                                         text=f'Привет. Цена стала больше чем вчера и составляет {product_id.current_price} '
                                              f'рублей. Завтра, возможно, будет дороже.')
            elif product_id.current_price == product_id.old_price:
                context.bot.send_message(chat_id,
                                         text=f'Привет, на сегодняшний день цена товара осталась прежней и составляет '
                                              f'{product_id.current_price} рублей. Так же можно получить 7% кэшбэк при '
                                              f'оплате картой «Онлайнер клевер».')
            elif product_id.current_price < product_id.old_price:
                context.bot.send_message(chat_id, f'Привет. Удивительно, но цена понизилась и составляет '
                                                  f'{product_id.current_price} рублей. Надо срочно брать, пока не '
                                                  f'подорожало.')
