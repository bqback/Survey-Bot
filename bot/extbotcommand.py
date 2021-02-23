from telegram import BotCommand

class ExtBotCommand(BotCommand):
    def __init__(self, command: str, description: str, long_description: str = None):
        super().__init__(command, description)
        if long_description is not None:
            self.long_description = long_description
        else:
            self.long_description = description