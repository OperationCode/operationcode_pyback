import logging
import time
from slackclient import SlackClient
from utils.log_manager import setup_logging
# from src.creds import TOKEN, PROXY
from decouple import config
import traceback

logger = logging.getLogger(__name__)
new_event_logger = logging.getLogger(f'{__name__}.new_member')
all_event_logger = logging.getLogger(f'{__name__}.all_events')


# constants
MESSAGE = (
    "Hi {real_name},\n\n Welcome to Operation Code! I'm a bot designed to help answer questions and get you on your way in our community.\n\n"
    "Please take a moment to review our <https://op.co.de/code-of-conduct|Code of Conduct.>\n\n"
    "Our goal here at Operation Code is to get veterans and their families started on the path to a career in programming. "
    "We do that through providing you with scholarships, mentoring, career development opportunities, conference tickets, and more!\n\n"
    "You're currently in Slack, a chat application that serves as the hub of Operation Code. "
    "If you're currently visiting us via your browser, Slack provides a stand alone program to make staying in touch even more convenient. "
    "You can download it <https://slack.com/downloads|here.>\n\n"
    "Want to make your first change to a program right now? "
    "All active Operation Code Projects are located on our source control repository. "
    "Our projects can be viewed on <https://github.com/OperationCode/START_HERE|Github.>")


PROXY = config('PROXY')
TOKEN = config('TOKEN')
PROXY = PROXY if PROXY else None
slack_client = SlackClient(TOKEN, proxies=PROXY)


def build_message(message_template, **kwargs):
    return message_template.format(**kwargs)


def event_handler(event_dict):
    all_event_logger.info(event_dict)
    if event_dict['type'] == 'team_join':
        new_event_logger.info('New member event recieved')
        new_member(event_dict)

    if event_dict['type'] == 'presence_change':
        all_event_logger.info('User {} changed state to {}'.format(user_name_from_id(event_dict['user']), event_dict['presence']))

    # can be used for development to trigger the event instead of the team_join
    if event_dict['type'] == 'message' and 'user' in event_dict.keys():

        # Will need to be removed.  Currently for testing
        logger.info('Message event')
    if event_dict['type'] == 'message' and 'user' in event_dict.keys() and event_dict['text'] == 'test4611':
        event_dict['user'] = {'id': event_dict['user']}
        new_member(event_dict)



def new_member(event_dict):
    new_event_logger.info('Recieved json event: {}'.format(event_dict))

    user_id = event_dict['user']['id']
    # user_id = event_dict['user']
    logging.info('team_join message')

    custom_message = build_message(MESSAGE,
                                   real_name=user_name_from_id(user_id))


    new_event_logger.info('Built message: {}'.format(event_dict))
    response = slack_client.api_call('chat.postMessage',
                                     channel=user_id,
                                     text=custom_message,
                                     as_user=True)


    if response['ok'] == 'true':
        new_event_logger.info('New Member Slack response: {}'.format(response))
    else:
        new_event_logger.error('FAILED -- Message to new member returned error: {}'.format(response))


def parse_slack_output(slack_rtm_output):
    """
    The Slack Real Time Messaging API is an events firehose.
    This parsing function returns None unless a message
    is directed at the Bot, based on its ID.
    """
    for output in slack_rtm_output:
        # process a single item in list at a time
        event_handler(output)


def user_name_from_id(user_id):
    # get detailed user info
    response = slack_client.api_call('users.info', user=user_id)

    if response['user']['real_name']:
        return response['user']['real_name'].title()
    elif response['user']['name']:
        return response['user']['name'].title()
    else:
        return 'New Member'

def join_channels():
    response = slack_client.api_call('channels.join', name='general')
    print(response)



# set the defalt to a 1 second delay
def run_bot(delay=1):
    setup_logging()
    if slack_client.rtm_connect():
        print(f"StarterBot connected and running with a {delay} second delay")

        while True:
            try:
                parse_slack_output(slack_client.rtm_read())
                time.sleep(delay)
            except Exception as e:
                logger.error(f'Some exception occured: {e}')
                logger.error(f'traceback: {traceback.format_exc(e)}')
                slack_client.rtm_connect()
    else:
        print("Connection failed.  Invalid Slack token or bot ID")


if __name__ == '__main__':
    run_bot()
