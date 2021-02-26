# -*- coding: utf-8 -*-

import logging
import logging.handlers
import os
import time

from telegram.ext import PicklePersistence, Updater, Defaults

import bot.utils as utils
import bot.setup as setup

# Enable logging


def main():

    (
        token,
        pickle,
        chats,
        admins,
        defaults,
        default_settings,
        log_file,
        log_size,
        log_backups,
        sheets_file,
        sheets_email,
    ) = utils.parse_cfg("bot.ini")

    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    rfh = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=log_size, backupCount=log_backups
    )

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    rfh.setFormatter(formatter)

    needRoll = os.path.isfile(log_file)

    logger.addHandler(rfh)

    if needRoll:
        logger.info("\n---------\nLog closed on %s.\n---------\n" % time.asctime())
        logger.handlers[0].doRollover()

    persistence = PicklePersistence(pickle, single_file=False)

    upd = Updater(
        token=token,
        use_context=True,
        persistence=persistence,
        defaults=Defaults(**defaults),
    )

    setup.register_dispatcher(
        upd,
        admins=admins,
        chats=chats,
        default_settings = default_settings,
        gsheets_file=sheets_file,
        gsheets_email=sheets_email,
    )

    upd.start_polling()
    logger.info("\n---------\nLog started on %s.\n---------\n" % time.asctime())

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    upd.idle()


if __name__ == "__main__":
    main()
