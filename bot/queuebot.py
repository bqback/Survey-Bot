from telegram import Bot
from telegram.ext import messagequeue, Updater

class MQBot(Bot):
    def __init__(self, *args, is_queued_def = True, mqueue = None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)

        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or messagequeue.MessageQueue()

    def stop(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @messagequeue.queuedmessage
    def send_message(self, *args, **kwargs):
        return super(MQBot, self).send_message(*args, **kwargs)
    def send_poll(self, *args, **kwargs):
        return super(MQBot, self).send_poll(*args, **kwargs)
    def edit_message_text(self, *args, **kwargs):
        return super(MQBot, self).edit_message_text(*args, **kwargs)

class QueueUpdater(Updater):
    def __init__(self, bot: MQBot, *args, **kwargs):
        super().__init__(bot = bot, *args, **kwargs)

    def signal_handler(self, signum, frame):
        super().signal_handler(signum, frame)
        self.bot.stop()