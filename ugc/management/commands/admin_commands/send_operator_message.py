# from ugc.models import Product, Message, Profile
# from telegram.ext import CallbackContext
#
#
# # from telegram import InlineKeyboardMarkup, InlineKeyboardButton
#
#
# def send_operator_message(context: CallbackContext):
#     """Отправляет ежедневно в 10.00 сообщения оператора по товарам, которые мониторят пользователи"""
#     product_list = Product.objects.all()
#     for product in product_list:
#         if product.operator_message:
#             message_list = Message.objects.filter(product=product)
#             for message in message_list:
#                 users_list = Profile.objects.filter(external_id=message.profile.external_id)
#                 for user in users_list:
#                     chat_id = user.external_id
#                     product_url = product.product_url
#                     current_price = product.current_price
#                     operator_price = product.operator_price
#                     context.bot.send_message(chat_id, product_url)
#                     message = f'{product.product_name} по цене {str(product.operator_price)} ' \
#                               f'можно {product.operator_message}'
#                     context.bot.send_message(chat_id, f'На этот товар оператор нашел ниже цену, '
#                                                       f'вместо {current_price} цена составляет {operator_price}!\n'
#                                                       f'{message}')

                    # keyboard = [
                    #     [
                    #         InlineKeyboardButton('Да', callback_data=f'yes_{chat_id}_{product.external_id}')
                    #     ],
                    #     [
                    #         InlineKeyboardButton('Нет', callback_data=f'no_{chat_id}_{product.external_id}')
                    #     ]
                    # ]
                    # reply_keyboard = InlineKeyboardMarkup(keyboard)
                    # context.bot.send_message(chat_id, 'Берем?', reply_markup=reply_keyboard)
#
#
# def send_operator_message_waiting(context: CallbackContext):
#     """Отправляет ежедневно в 10.30 сообщения оператора по товарам на которые пользователи оставили желаемую цену"""
#     operator_message_waiting_list = OperatorMessageWaiting.objects.all()
#     for i in operator_message_waiting_list:
#         chat_id = i.monitoring.profile.external_id
#         product_url = i.monitoring.text.product_url
#         operator_price = i.operator_price
#         context.bot.send_message(chat_id, product_url)
#         context.bot.send_message(chat_id,
#                                  text=f'Это снова я! Я долго искал, старался и могу тебе предложить выбранный тобой '
#                                       f'товар за желаемую тобой цену в {operator_price}.')
#         context.bot.send_message(chat_id, 'Я забронировал для тебя данный товар, бронь будет действовать 3 часа.')
#         context.bot.send_message(chat_id, f'Для заказа доставки и оплаты перейди по ссылке: {i.operator_url}')
#         root_object = Message.objects.get(profile=i.monitoring.profile, text=i.monitoring.text)
#         active = ActiveMonitoring.objects.get(id_monitoring=i.monitoring.id_monitoring)
#         i.delete()
#         active.delete()
#         root_object.delete()
