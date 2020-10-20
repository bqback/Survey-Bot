# -*- coding: utf-8 -*-

from telegram.ext import PicklePersistence
import logging

from configparser import ConfigParser
from bot.build import build
from bot.setup import register_dispatcher

# Enable logging

def main():

    config = ConfigParser()
    config.read('bot.ini')

    log = config['bot']['log']
    token = config['bot']['token']
    pickle = config['bot']['pickle']
    admins = [int(admin_id) for admin_id in config['bot']['admins'].split(', ')]
    defaults = config.items('defaults')
    defaults = dict(defaults)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename=log)

    logger = logging.getLogger(__name__)

    persistence = PicklePersistence(pickle, single_file = False)
    
    upd = build(token = token, use_context = True, persistence = persistence, defaults = defaults)

    register_dispatcher(upd.dispatcher, admins = admins, logger = logger)

    upd.start_polling()
    logger.info('Started polling')

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    upd.idle()

if __name__ == '__main__':
    main()