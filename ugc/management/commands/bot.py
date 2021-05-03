from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import ConversationHandler, CallbackQueryHandler
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.utils.request import Request
from .handlers import command_handlers, message_handlers, callback_handlers

all_monitoring_percent = 2
FIRST, SECOND, THIRD, FORTH, FIFTH = range(5)


class Command(BaseCommand):
    help = 'Телеграм бот'

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            #request=request,
            token=settings.TOKEN,
        )
        print(bot.get_me())

        updater = Updater(
            bot=bot,
            use_context=True,
        )
        """Изменение процента пассивного мониторинга"""
        change_percent_handler = CommandHandler('change_percent', command_handlers.change_percent)
        """Команда по ежедневному обновлению базы данных"""
        general_job_handler = CommandHandler('all_jobs', command_handlers.set_general_jobs)
        """Команда для вызова помощи"""
        helper_handler = CommandHandler('help', command_handlers.helper)

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', command_handlers.start)],
            states={
                FIRST: [
                    CommandHandler('some', command_handlers.done),
                    CommandHandler('help', command_handlers.helper_first),
                    MessageHandler(Filters.text, message_handlers.find_onliner_price),
                ],
                SECOND: [
                    CommandHandler('some', command_handlers.done),
                    CallbackQueryHandler(callback_handlers.answer_about_monitoring),
                    MessageHandler(Filters.text, message_handlers.warning_message),
                ],
            },
            fallbacks=[CommandHandler('some', command_handlers.done)]
        )

        # conv_handler_end = ConversationHandler(
        #     entry_points=[CallbackQueryHandler(callback_handlers.send_url_or_answer_about_price)],
        #     states={
        #         FORTH: [
        #             CommandHandler('help', command_handlers.helper_forth),
        #             CommandHandler('some', command_handlers.done),
        #             MessageHandler(Filters.text, message_handlers.user_price),
        #         ],
        #     },
        #     fallbacks=[CommandHandler('some', command_handlers.done)]
        # )

        updater.dispatcher.add_handler(conv_handler)
        # updater.dispatcher.add_handler(conv_handler_end)
        updater.dispatcher.add_handler(change_percent_handler)
        updater.dispatcher.add_handler(general_job_handler)
        updater.dispatcher.add_handler(helper_handler)

        updater.start_polling()
        updater.idle()
