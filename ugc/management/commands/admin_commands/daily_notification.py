from ugc.models import ActiveMonitoring
import datetime


def daily_notification(context):
    """Функция для ежедневного могиторинга"""
    active_monitoring_list = ActiveMonitoring.objects.all()
    for i in active_monitoring_list:
        product_id = i.text
        chat_id = i.profile.external_id
        actually = int((i.time_published + datetime.timedelta(hours=3)).strftime('%d'))
        now = int(datetime.datetime.today().strftime('%d'))
        result_time = now - actually
        if result_time != 0:
            if float(i.text.operator_price) == 0.0:
                context.bot.send_message(chat_id, i.text.product_url)
                cashback_message = ''
                if i.text.cashback:
                    cashback_message = f'Так же можно получить {i.text.cashback}% кэшбэк при оплате ' \
                                       f'картой «Онлайнер клевер».'
                if product_id.current_price > product_id.old_price:
                    context.bot.send_message(chat_id,
                                             text=f'Привет. Цена стала больше чем вчера и составляет '
                                                  f'{product_id.current_price} '
                                                  f'рублей. Завтра, возможно, будет дороже. \n {cashback_message}')
                elif product_id.current_price == product_id.old_price:
                    context.bot.send_message(chat_id,
                                             text=f'Привет, на сегодняшний день цена товара осталась прежней и '
                                                  f'составляет '
                                                  f'{product_id.current_price} рублей. \n {cashback_message}')
                elif product_id.current_price < product_id.old_price:
                    context.bot.send_message(chat_id, f'Привет. Удивительно, но цена понизилась и составляет '
                                                      f'{product_id.current_price} рублей. Надо срочно брать, пока не '
                                                      f'подорожало. \n {cashback_message}')
            else:
                message = f'Мы можем предложить {i.text.product_name} за {i.text.operator_price} ' \
                          f'{i.text.operator_message}, в каталоге онлайнер ' \
                          f'он представлен по минимальной цене {i.text.current_price}'
                context.bot.send_message(chat_id, text=message)
