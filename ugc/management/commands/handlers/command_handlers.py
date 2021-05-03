from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from ugc.models import PassiveMonitoring, ActiveMonitoring
from ...commands import bot
import datetime
from pytz import timezone
from ugc.management.commands.admin_commands.update_price import update_price
# from ugc.management.commands.admin_commands.send_operator_message import send_operator_message
from django.conf import settings
from ugc.management.commands.admin_commands.passive_notification import passive_notification
from ugc.management.commands.admin_commands.daily_notification import daily_notification


def start(update: Update, context: CallbackContext):
    """Обработчик команды '/start', приветствует пользователя и просит прислать ссылку на товар"""
    update.message.reply_text(
        text='Привет! Я бот Гоша и я умею отслеживать изменение цены на выбранный тобой товар в каталоге онлайнера. '
             'Я буду очень старательно обучаться и научусь искать минимальную цену на товар во всех интернет-магазинах.'
    )
    update.message.reply_text(
        text='Скопируй мне ссылку из каталога онлайнера, либо перешли её мне из мобильного приложения '
             '«Каталог онлайнер» и я буду тебе сообщать об изменение цены на этот товар.',
    )
    return bot.FIRST


def change_percent(update: Update, context: CallbackContext):
    """Команда оператора по смене процента для пассивного мониторинга"""
    if update.message.chat_id == settings.OPERATOR_ID:
        monitoring_list = PassiveMonitoring.objects.all()
        for i in monitoring_list:
            i.monitoring_percent = int(context.args[0])
            i.save()
        update.message.reply_text(
            text=f'Процент изменен c {bot.all_monitoring_percent} '
                 f'на {int(context.args[0])} у {len(monitoring_list)} пользователей '
        )
        bot.all_monitoring_percent = int(context.args[0])
    else:
        update.message.reply_text(
            text='Неверная команда!'
        )


def done(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Начни с команды "/start"',
    )

    return ConversationHandler.END


def set_general_jobs(update: Update, context: CallbackContext):
    """Команда оператора по установлению обновления информации по ценам на товары"""
    chat_id = update.message.chat_id
    if chat_id == settings.OPERATOR_ID:
        context.job_queue.run_daily(update_price,
                                    datetime.time(settings.UPDATE_TIME[0],
                                                  settings.UPDATE_TIME[1],
                                                  tzinfo=timezone('Europe/Minsk')),
                                    context=chat_id,
                                    name=f'{str(chat_id)}_update_price')
        update.message.reply_text(
            text='Команда по ежедневному обновлению цен установлена!'
        )
        context.job_queue.run_daily(daily_notification,
                                    time=datetime.time(settings.ACTIVE_TIME[0],
                                                       settings.ACTIVE_TIME[1],
                                                       tzinfo=timezone('Europe/Minsk')),
                                    context=chat_id,
                                    name=f'{str(chat_id)}_daily')
        update.message.reply_text(
            text='Команда по ежедневному мониторингу установлена!'
        )
        # context.job_queue.run_daily(send_operator_message,
        #                             datetime.time(settings.MONITORING_TIME[0],
        #                                           settings.MONITORING_TIME[1],
        #                                           tzinfo=timezone('Europe/Minsk')),
        #                             context=chat_id,
        #                             name=f'{str(chat_id)}_send_operator_message')
        # update.message.reply_text(
        #     text='Команда по отправке сообщений оператора установлена!'
        # )
        # context.job_queue.run_daily(send_operator_message_waiting,
        #                             datetime.time(settings.MONITORING_WAITING_TIME[0],
        #                                           settings.MONITORING_WAITING_TIME[1],
        #                                           tzinfo=timezone('Europe/Minsk')),
        #                             context=chat_id,
        #                             name=f'{str(chat_id)}_send_operator_waiting_message')
        context.job_queue.run_daily(passive_notification,
                                    time=datetime.time(settings.PASSIVE_TIME[0],
                                                       settings.PASSIVE_TIME[1],
                                                       tzinfo=timezone('Europe/Minsk')),
                                    context=chat_id,
                                    name=f'{str(chat_id)}_daily')
        update.message.reply_text(
            text='Команда по отправке сообщений оператора с желаемыми пользователями ценами установлена!'
        )
    else:
        update.message.reply_text(
            text='Неверная команда',
        )


def helper(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Этот бот поможет найти тебе подходящую цену на нужный тебе товар.\n'
             'Для начала работы бота введите команду "/start".\n'
             'Бот принимает ссылки с онлайнера, если они начинаются следующим образом:\n'
             '"catalog.onliner.by/..." или "https://catalog.onliner.by/...".\n'
             'Заходите на сайт и выбирайте подходящий вам товар)))'
    )


def helper_first(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Бот принимает ссылки с онлайнера, если они начинаются следующим образом:\n'
             '"catalog.onliner.by/..." или "https://catalog.onliner.by/...".\n'
             'Заходите на сайт и выбирайте подходящий вам товар)))'
    )
    return bot.FIRST


def helper_forth(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Здесь необходимо ввести число'
    )
    return bot.FORTH


def stop_command(update: Update, context: CallbackContext):
    active_monitoring_list = ActiveMonitoring.objects.all()
    for i in active_monitoring_list:
        if i.profile.external_id == update.message.chat_id:
            i.delete()
    update.message.reply_text(
        text='Мониторинг отключен'
    )
