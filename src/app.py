import logging
import time
from slackclient import SlackClient
from utils.log_manager import setup_logging
from archived.creds import TOKEN

logger = logging.getLogger(__name__)
new_event_logger = logging.getLogger(f'{__name__}.new_member')


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

slack_client = SlackClient(TOKEN)


def build_message(message_template, **kwargs):
    return message_template.format(**kwargs)


def event_handler(event_dict):
    if event_dict['type'] == 'team_join':
        new_event_logger.info('New member event recieved')
        new_member(event_dict)
    if event_dict['type'] == 'message' and 'user' in event_dict.keys():

        # Will need to be removed.  Currently for testing
        logger.info('Message event')


def new_member(event_dict):
    new_event_logger.info('Recieved json event: {}'.format(event_dict))

    user_id = event_dict['user']['id']
    # user_id = event_dict['user']
    logging.info('team_join message')

    custom_message = build_message(MESSAGE,
                                   real_name=user_name_from_id(user_id))

    new_event_logger.info('Built message: {}'.format(event_dict))
    slack_client.api_call('chat.postMessage',
                          channel=user_id,
                          text=custom_message,
                          as_user=True)

    new_event_logger.info('New Member Slack response: {}'.format(event_dict))


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


# set the defalt to a 1 second delay
def run_bot(delay=1):
    setup_logging()

    if slack_client.rtm_connect():
        print(f"StarterBot connected and running with a {delay} second delay")
        while True:
            parse_slack_output(slack_client.rtm_read())
            time.sleep(delay)
    else:
        print("Connection failed.  Invalid Slack token or bot ID")


if __name__ == '__main__':
    run_bot()
