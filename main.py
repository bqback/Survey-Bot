# -*- coding: utf-8 -*-

import logging
import logging.handlers
import os
import time

from re import match

from telegram.ext import PicklePersistence

from configparser import ConfigParser
from bot.build import build
from bot.setup import register_dispatcher

# Enable logging

def main():

    config = ConfigParser(comment_prefixes = '/', allow_no_value = True)
    config.read_file(open('bot.ini'))

    token = config['bot']['token']
    pickle = config['bot']['pickle']
    admin_list = config['bot']['admins']
    if match(' ', admin_list):
        admin_list.replace(' ', '')
        config['bot']['admins'] = admin_list
        config.write(open('bot.ini', 'w'))
    admins = [int(admin_id) for admin_id in config['bot']['admins'].split(',')]
    defaults = dict(config.items('defaults'))

    log_file = config['log']['filename']
    log_size = int(config['log']['log_size']) * 1024
    log_backups = int(config['log']['log_backups'])

    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    rfh = logging.handlers.RotatingFileHandler(log_file, maxBytes = log_size, backupCount = log_backups)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    rfh.setFormatter(formatter)

    needRoll = os.path.isfile(log_file)

    logger.addHandler(rfh)

    if needRoll:
        logger.info('\n---------\nLog closed on %s.\n---------\n' % time.asctime())
        logger.handlers[0].doRollover()

    persistence = PicklePersistence(pickle, single_file = False)
    
    upd = build(token = token, use_context = True, persistence = persistence, defaults = defaults)

    register_dispatcher(upd, admins = admins)

    upd.start_polling()
    logger.info('\n---------\nLog started on %s.\n---------\n' % time.asctime())

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    upd.idle()

if __name__ == '__main__':
    main()