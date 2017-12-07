import websocket
import json
import requests
from urllib3 import disable_warnings, exceptions  # allow to disable InsecureRequestWarning, not sure if needed
from urllib.parse import quote  # replace special characters with web safe ones. ???
import logging
from .log_manager import setup_logging
from .creds import TOKEN  # locally saved file "creds.py" this is added to .gitignore

logger = logging.getLogger(__name__)

# Suppress InsecureRequestWarning
disable_warnings(exceptions.InsecureRequestWarning)

MESSAGE = 'Hi there {real_name}, welcome to Operation Code!'
UNFURL = False
# https://test-op-code.slack.com/services/B86CT5GQH?added=1



def build_message(token=None,
                  message=None,
                  channel_id=None
                  ):
    ending = '' if not UNFURL else '&unfurl_links=false'
    parsed_message = quote(message)
    logging.debug(parsed_message)
    return (
        'https://slack.com/api/chat.postMessage?'
        f'token={token}&'
        f'channel={channel_id}&'
        f'text={parsed_message}&'
        'parse=full&as_user=true&'
        f'unfurl_links=false{ending}'
    )


def parse_new_member(json_message,
                     message=None
                    ):
    user_request_url = ('https://slack.com/api/im.open?token='
                        f'{TOKEN}'
                        f'&user={json_message["user"]["id"]}'
                        )

    user_message_response = requests.get(user_request_url)
    logging.info(user_message_response)
    response_json = user_message_response.json()

    channel_id = response_json["channel"]["id"]
    built_message = build_message(token=TOKEN,
                                  message=message,
                                  channel_id=channel_id
                                  )
    response_posted = requests.post(built_message)
    logging.info(response_posted)



# Connects to Slack and initiates socket handshake
def start_rtm():
    get_response = requests.get(f'https://slack.com/api/rtm.start?token={TOKEN}',
                                verify=False
                                )
    json_response = get_response.json()
    if json_response['ok']:
        response_url = json_response["url"]
        logger.info(f'response url from json: {response_url}')
        logging.debug('Good auth response')
        return response_url
    logging.debug('Bad Auth')

def on_message(ws, message):
    # logger.info(message)
    json_message = json.loads(message)
    logger.info(json_message)

    logging.info(f'new message of type: {json_message["type"]}')
    if json_message['type'] == "team_join":
        user_name = json_message['user']['real_name']
        logging.info('team_join message')
        custom_message = MESSAGE.format(real_name=user_name)
        parse_new_member(json_message,
                         message=custom_message
                         )
    # logging.info('Equality of type: {}'.format(json_message['type'] == "team_join"))

def on_error(ws, error):
    logger.error(f'SOME ERROR HAS HAPPENED: {error}')


def on_close(ws):
    logger.info('Connection Closed')

def on_open(ws):
    logger.debug('Connection Started - Auto Greeting new joiners to the network')

def run_bot():
    setup_logging()
    url_response = start_rtm()
    web_socket = websocket.WebSocketApp(url_response,
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close
                                        )
    # ws.on_open
    web_socket.run_forever()

if __name__ == '__main__':
    run_bot()