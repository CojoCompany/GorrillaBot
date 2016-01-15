"""
GorrillaBot main file.
"""
import inspect
import requests


class GorrillaBot():
    """
    Bot class.
    """
    def __init__(self):
        self.timeout = 10
        with open('.token', 'r') as f:
            token = f.read().rstrip()
        self.url = 'https://api.telegram.org/bot{}/'.format(token)
        self.keep_alive = True
        self.last_update = 0
        self.command_handler = {}

    def run(self):
        """
        Main loop.
        """
        while self.keep_alive:
            updates = self.get_updates(self.last_update, self.timeout)
            self.process_updates(updates)
        # Get remaining updates from the server or, at least, notify the
        # reception of the messages processed
        while True:
            updates = self.get_updates(self.last_update, 0)
            if not self.process_updates(updates):
                break

    def get_updates(self, offset, timeout):
        """
        Get updates from the server.
        """
        params = {'offset': offset + 1, 'timeout': timeout}
        updates = requests.get(self.url + 'getUpdates', params)
        return updates

    def process_updates(self, updates):
        """
        Process updates from the server.
        """
        # TODO: handle response errors
        updates = updates.json()
        if not updates['result']:
            return False
        for update in updates['result']:
            # TODO: custom class for `update`
            self.last_update = update['update_id']
            if 'message' not in update:
                continue
            if self.process_command(update):
                continue
            self.process_message(update)
        return True

    def send_message(self, chat_id, text):
        """
        Send a message.
        """
        params = {'chat_id': chat_id, 'text': text}
        requests.get(self.url + 'sendMessage', params)

    def add_command_handler(self, command, handler):
        """
        Add a command handler.
        """
        if ' ' in command:
            raise ValueError('Command must not have spaces!')
        if not command.startswith('/'):
            command = '/' + command
        self.command_handler[command] = handler

    def process_command(self, update):
        """
        Process a message and return `True` if the message was successfuly
        processed as a command.
        """
        message = update['message']['text']
        if not message.startswith('/'):
            return False
        command = message.split()[0]
        if not command in self.command_handler:
            return False
        handler = self.command_handler[command]
        nparams = len(inspect.signature(handler).parameters)
        if nparams == 1:
            handler(self)
        elif nparams == 2:
            handler(self, update)
        return True

    def process_message(self, update):
        """
        Process an incoming message.
        """
        chat_id = update['message']['chat']['id']
        text = update['message']['text']
        self.send_message(chat_id, text)

    def log(self, data):
        """
        A simple logging method which, for now, only prints to stdout.
        """
        print(data)


def die(bot):
    bot.log('Dying...')
    bot.keep_alive = False


def echo(bot, command):
    message = ' '.join(command['message']['text'].split(' ')[1:])
    bot.send_message(command['message']['chat']['id'], message)


if __name__ == '__main__':

    bot = GorrillaBot()
    bot.add_command_handler('die', die)
    bot.add_command_handler('echo', echo)
    bot.run()
