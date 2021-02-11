from bot.queuebot import MQBot, QueueUpdater
from telegram.ext import PicklePersistence, Updater, messagequeue, Defaults
from telegram.utils.request import Request
from typing import Dict

def build(token: str, use_context: bool, persistence: PicklePersistence, defaults: Dict) -> Updater:
    queue = messagequeue.MessageQueue(all_burst_limit = 20, all_time_limit_ms = 60000)
    request = Request(con_pool_size = 8)
    defaults = Defaults(defaults)
    bot = MQBot(token = token, request = request, mqueue = queue, defaults = defaults)
    updater = QueueUpdater(bot = bot, use_context = True, persistence = persistence)
    return updater
