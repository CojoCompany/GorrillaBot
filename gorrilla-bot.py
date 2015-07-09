
import json
import time
import requests


if __name__ == '__main__':

    with open('.token', 'r') as f:
        token = f.read()[:-1]
    url = 'https://api.telegram.org/bot{}/'.format(token)

    update_id = 0
    while True:
        params = {'offset' : update_id + 1}
        response = requests.get(url + 'getUpdates', params)
        # TODO: handle response errors
        data = response.json()
        for update in data['result']:
            update_id = update['update_id']
            if not 'message' in update:
                continue
            params = {'chat_id' : update['message']['chat']['id'],
                      'text' : update['message']['text']}
            requests.get(url + 'sendMessage', params)
        time.sleep(1)

