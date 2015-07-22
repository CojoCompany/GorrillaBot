"""
GorrillaBot main file.
"""
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

    def run(self):
        """
        Main loop.
        """
        while self.keep_alive:
            response = self.get_updates(self.last_update, self.timeout)
            self.process_response(response)
        # Get remaining updates from the server or, at least, notify the
        # reception of the messages processed
        while True:
            response = self.get_updates(self.last_update, 0)
            # TODO: handle response errors
            data = response.json()
            if not data['result']:
                break
            self.process_response(response)

    def get_updates(self, offset, timeout):
        """
        Get updates from the server.
        """
        params = {'offset': offset + 1, 'timeout': timeout}
        response = requests.get(self.url + 'getUpdates', params)
        return response

    def process_response(self, response):
        """
        Process response from the server.
        """
        # TODO: handle response errors
        data = response.json()
        for update in data['result']:
            self.last_update = update['update_id']
            if 'message' not in update:
                continue
            if self.process_command(update['message']['text']):
                continue
            params = {'chat_id': update['message']['chat']['id'],
                      'text': update['message']['text']}
            requests.get(self.url + 'sendMessage', params)

    def process_command(self, text):
        """
        Process a message and return `True` if the message was successfuly
        processed as a command.
        """
        if text[0] != '/':
            return False
        command = text.split()
        if command[0] == '/upgrade':
            print('ooops')
            self.keep_alive = False
        return True


if __name__ == '__main__':

    bot = GorrillaBot()
    bot.run()
