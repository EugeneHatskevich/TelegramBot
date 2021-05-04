from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, ConversationHandler
from ugc.models import Product, Profile, ActiveMonitoring, PassiveMonitoring, Message
from ..parse import parse_data
from ...commands import bot
import django.db.utils
import re

pattern = r'^(catalog.onliner|https://catalog.onliner)'


def find_onliner_price(update: Update, context: CallbackContext):
    """Поиск цен на товар ссылку на который предоставил пользователь"""
    chat_id = update.message.chat_id
    text = update.message.text
    result = re.search(pattern, text)
    if result:
        try:
            price_data = parse_data(text, 'price')
            product_data = parse_data(text)
            product_name = product_data['extended_name']
            min_price = price_data['prices']['min']['amount']
            current_price = price_data['prices']['current']['amount']
            if product_data['max_cobrand_cashback']:
                cashback = product_data['max_cobrand_cashback']['percentage']
            else:
                cashback = 0
        except KeyError:
            update.message.reply_text(
                text='Неверная ссылка, попробуйте снова!'
            )
            return bot.FIRST
    else:
        update.message.reply_text(
            text='Неверная ссылка, попробуйте снова!'
        )
        return bot.FIRST

    try:
        profile, _ = Profile.objects.get_or_create(
            external_id=chat_id,
            defaults={
                'name': update.message.from_user.first_name
            }
        )
        product, _ = Product.objects.get_or_create(
            external_id=text.split("/")[-1],
            product_url=text,
            product_name=product_name,
            defaults={
                'current_price': current_price,
                'average_price': min_price,
                'cashback': cashback
            },
        )
        context.user_data['product_id'] = text.split("/")[-1]

        m, _ = Message.objects.get_or_create(
            profile=profile,
            product=product,
        )

    except django.db.utils.IntegrityError:
        update.message.reply_text(
            text='Неверная ссылка, попробуйте снова!'
        )
        return bot.FIRST

    if float(current_price) == 0.0:
        update.message.reply_text(
            text='Данный товар в продаже отсутствует, я продолжу мониторинг и если он появится в продаже – '
                 'обязательно сообщу'
        )
        passive, _ = PassiveMonitoring.objects.get_or_create(
            profile=profile,
            text=product,
            monitoring_percent=bot.all_monitoring_percent
        )
        return ConversationHandler.END
    else:
        if product.cashback:
            cashback = product_data['max_cobrand_cashback']['percentage']
            reply_text = f'Спасибо! На сегодняшний день в каталоге  минимальная представленная цена {current_price} рублей.\n' \
                         f'При оплате в каталоге онлайнера картой «Онлайнер клевер» доступен дополнительный кэшбек {cashback}%.\n' \
                         f'Минимальная зафиксированная цена на данный товар составляла {min_price} рублей.'
        else:
            reply_text = f'Спасибо! На сегодняшний день в каталоге  минимальная представленная цена {current_price} рублей.\n' \
                         f'Минимальная зафиксированная цена на данный товар составляла {min_price} рублей.'

        update.message.reply_text(
            text=reply_text,
        )
        keyboard = [
            [
                InlineKeyboardButton('Да', callback_data='yes')
            ],
            [
                InlineKeyboardButton('Нет', callback_data='no')
            ]
        ]
        reply_keyboard = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            text='Я могу начать ежедневный мониторинг по выбранной позиции и каждый день сообщать об изменении цены. '
                 'Я начинаю?',
            reply_markup=reply_keyboard
        )

        return bot.SECOND


def user_price(update: Update, context: CallbackContext):
    """Принимает желаемую цену пользователя на мониторящийся им товар"""
    try:
        user_id, product_id = context.user_data['info'].split('_')
        profile = Profile.objects.get(external_id=user_id)
        product = Product.objects.get(external_id=product_id)
        test = ActiveMonitoring.objects.get(profile=profile, text=product)
        test.waiting_price = float(update.message.text)
        test.save()
        return ConversationHandler.END
    except ValueError:
        update.message.reply_text(
            text='Неверный формат, попробуйте снова'
        )
        return bot.FORTH
    # active = ActiveMonitoring.objects.get(profile=profile, text=product)
    # active.delete()


def warning_message(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Выберите "Да" или "Нет"!',
    )
    return bot.SECOND


def buy_function(update: Update, context: CallbackContext):
    message = update.message.text.lower()
    if message in ['где купить?', 'где купить', 'как купить', 'как купить?', 'купить', 'приобрести']:
        profile = Profile.objects.get(external_id=update.message.chat_id)
        monitoring_list = ActiveMonitoring.objects.filter(profile=profile)
        for elem in monitoring_list:
            if elem.text.operator_price:
                product_name = elem.text.product_name
                text=f'{product_name} можно купить у нашего партнера: в интернет-магазине 21vek по ' \
                     f'промокоду price_cheker_bot.'
            else:
                product_url = elem.text.product_url
                text=f'Данный товар с минимальной ценой представлен в каталоге онлайнер и ' \
                     f'{product_url}.'
            update.message.reply_text(text=text)
