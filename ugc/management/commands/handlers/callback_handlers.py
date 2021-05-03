from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from ugc.models import Profile, Product, PassiveMonitoring, ActiveMonitoring, Message
from ...commands import bot


def answer_about_monitoring(update: Update, context: CallbackContext):
    chat_id = update.callback_query.message.chat.id
    query = update.callback_query
    query.answer()
    profile = Profile.objects.get(
        external_id=chat_id,
    )
    product = Product.objects.get(
        external_id=context.user_data['product_id']
    )
    del context.user_data['product_id']
    if query.data == 'no':
        passive, _ = PassiveMonitoring.objects.get_or_create(
            profile=profile,
            text=product,
            monitoring_percent=bot.all_monitoring_percent
        )
        update.callback_query.edit_message_text(
            text='ОК, если будет, что-то интересное, я тебе сообщу)'
        )
        return ConversationHandler.END

    elif query.data == 'yes':
        active, _ = ActiveMonitoring.objects.get_or_create(
            profile=profile,
            text=product,
        )
        update.callback_query.edit_message_text(
            text='Благодарю за доверие. Уже завтра я сообщу, если цена изменится.',
        )
        return ConversationHandler.END


# def send_url_or_answer_about_price(update: Update, context: CallbackContext):
#     """Выдаем ссылку на заказ товара или спрашиваем о желаемой цене"""
#     query = update.callback_query
#     query.answer()
#     data_list = query.data.split('_')
#     profile = Profile.objects.get(external_id=data_list[1])
#     product = Product.objects.get(external_id=data_list[2])
#     active = ActiveMonitoring.objects.get(profile=profile, text=product)
#
#     if query.data[0:3] == 'yes':
#         update.callback_query.edit_message_text(
#             text=f'То, что ты выбрал можно приобрести в магазине: вот прямая ссылка на товар: {site.operator_url}'
#         )
#         root_object = Message.objects.get(profile=profile, text=product)
#         active.delete()
#         root_object.delete()
#         return ConversationHandler.END
#
#     elif query.data[0:2] == 'no':
#         update.callback_query.edit_message_text(
#             text='Жаль конечно, возможно это было самое лучшее предложение.\n'
#                  'По какой цене ты готов приобрести данный товар?'
#         )
#         context.user_data['info'] = f'{data_list[1]}_{data_list[2]}'
#         return bot.FORTH
