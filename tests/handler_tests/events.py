from ocbot.external.utils import ResponseContainer

GREETED_EVENT = {'type': 'interactive_message', 'actions': [{'name': 'greeted', 'type': 'button', 'value': 'greeted'}],
                 'callback_id': 'greeted', 'team': {'id': 'T8M8SQEN7', 'domain': 'test-domain'},
                 'channel': {'id': 'G8NDRJJF9', 'name': 'community'}, 'user': {'id': 'U8N6XBL7Q', 'name': 'bob'},
                 'action_ts': '1515178407.575368', 'message_ts': '1515177650.000464', 'attachment_id': '1',
                 'token': 'token', 'is_app_unfurl': False,
                 'original_message': {'type': 'message', 'user': 'U8M8UMEGK',
                                      'text': ':tada: <@U8N6XBL7Q> has joined! :tada:', 'bot_id': 'B8N6Z8M8E',
                                      'attachments': [
                                          {'callback_id': 'greeted', 'fallback': 'I will greet them!', 'id': 1,
                                           'color': '3AA3E3', 'actions': [
                                              {'id': '1', 'name': 'greeted', 'text': 'I will greet them!',
                                               'type': 'button', 'value': 'greeted', 'style': 'primary'}]}],
                                      'edited': {'user': 'U8M8UMEGK', 'ts': '1515177793.000000'},
                                      'ts': '1515177650.000464'},
                 'response_url': 'https://hooks.slack.com/actions/T8M8SQEN7/295887186759/xsDQQ9IBRIZNh9sMMywJ52Ov',
                 'trigger_id': '294748330979.293298830755.22eacc99fde6d0c5d7fee4e682ee7f3a'}

CORRECT_GREETED_PARAMS = {
    'text': GREETED_EVENT['original_message']['text'],
    'channel': GREETED_EVENT['channel']['id'],
    'ts': GREETED_EVENT['message_ts'],
    'as_user': True
}

RESET_GREET_EVENT = {'type': 'interactive_message',
                     'actions': [{'name': 'reset_greet', 'type': 'button', 'value': 'reset_greet'}],
                     'callback_id': 'greeted', 'team': {'id': 'T8M8SQEN7', 'domain': 'test-domain'},
                     'channel': {'id': 'G8NDRJJF9', 'name': 'community'},
                     'user': {'id': 'U8N6XBL7Q', 'name': 'bob'}, 'action_ts': '1515178551.160473',
                     'message_ts': '1515177650.000464', 'attachment_id': '1', 'token': 'token',
                     'is_app_unfurl': False, 'original_message': {'type': 'message', 'user': 'U8M8UMEGK',
                                                                  'text': ':tada: <@U8N6XBL7Q> has joined! :tada:',
                                                                  'bot_id': 'B8N6Z8M8E', 'attachments': [
            {'callback_id': 'greeted', 'text': ':100:<@U8N6XBL7Q> has greeted the new user!:100:', 'id': 1,
             'color': '3AA3E3', 'actions': [
                {'id': '1', 'name': 'reset_greet', 'text': 'Reset claim', 'type': 'button', 'value': 'reset_greet',
                 'style': 'danger'}]}], 'edited': {'user': 'U8M8UMEGK', 'ts': '1515178408.000000'},
                                                                  'ts': '1515177650.000464'},
                     'response_url': 'https://hooks.slack.com/actions/T8M8SQEN7/295888527511/HKyQH1VOrfb2x1LxWtZy3wgq',
                     'trigger_id': '294859183604.293298830755.1ca157e51fae911fe1319553649e1d3e'}

CORRECT_RESET_PARAMS = {
    'text': RESET_GREET_EVENT['original_message']['text'],
    'channel': RESET_GREET_EVENT['channel']['id'],
    'ts': RESET_GREET_EVENT['message_ts'],
    'as_user': True
}

CORRECT_GREET_MESSAGE = {'text': ':tada: <@U8N6XBL7Q> has joined! :tada:', 'channel': 'G8NDRJJF9',
                         'ts': '1515177650.000464', 'as_user': True, 'attachments': [
        {'text': ':100:<@U8N6XBL7Q> has greeted the new user!:100:', 'fallback': '', 'color': '#3AA3E3',
         'callback_id': 'greeted', 'attachment_type': 'default', 'actions': [
            {'name': 'reset_greet', 'text': 'Reset claim', 'type': 'button', 'style': 'danger',
             'value': 'reset_greet'}]}]}

CORRECT_RESET_MESSAGE = {'text': ':tada: <@U8N6XBL7Q> has joined! :tada:', 'channel': 'G8NDRJJF9',
                         'ts': '1515177650.000464', 'as_user': True, 'attachments': [
        {'text': '', 'fallback': 'I will greet them!', 'color': '#3AA3E3', 'callback_id': 'greeted',
         'attachment_type': 'default', 'actions': [
            {'name': 'greeted', 'text': 'I will greet them!', 'type': 'button', 'style': 'primary',
             'value': 'greeted'}]}]}

GREETED_RESPONSE_CONTAINER = ResponseContainer(route='Slack', method='chat.update',
                                               payload={'text': ':tada: <@U8N6XBL7Q> has joined! :tada:',
                                                        'channel': 'G8NDRJJF9',
                                                        'ts': '1515177650.000464', 'as_user': True, 'attachments': [
                                                       {'text': ':100:<@U8N6XBL7Q> has greeted the new user!:100:',
                                                        'fallback': '',
                                                        'color': '#3AA3E3', 'callback_id': 'greeted',
                                                        'attachment_type': 'default', 'actions': [
                                                           {'name': 'reset_greet', 'text': 'Reset claim',
                                                            'type': 'button', 'style': 'danger',
                                                            'value': 'reset_greet'}]}]})




RESET_RESPONSE_CONTAINER = \
    ResponseContainer(route='Slack', method='chat.update',
                      payload={'type': 'interactive_message', 'actions': [
                          {'name': 'reset_greet', 'type': 'button', 'value': 'reset_greet'}],
                               'callback_id': 'greeted',
                               'team': {'id': 'T8M8SQEN7',
                                        'domain': 'test-domain'},
                               'channel': {'id': 'G8NDRJJF9', 'name': 'community'},
                               'user': {'id': 'U8N6XBL7Q', 'name': 'bob'},
                               'action_ts': '1515178551.160473',
                               'message_ts': '1515177650.000464',
                               'attachment_id': '1', 'token': 'token',
                               'is_app_unfurl': False,
                               'original_message': {'type': 'message',
                                                    'user': 'U8M8UMEGK',
                                                    'text': ':tada: <@U8N6XBL7Q> has joined! :tada:',
                                                    'bot_id': 'B8N6Z8M8E',
                                                    'attachments': [
                                                        {'callback_id': 'greeted',
                                                         'text': ':100:<@U8N6XBL7Q> has greeted the new user!:100:',
                                                         'id': 1,
                                                         'color': '3AA3E3',
                                                         'actions': [{'id': '1',
                                                                      'name': 'reset_greet',
                                                                      'text': 'Reset claim',
                                                                      'type': 'button',
                                                                      'value': 'reset_greet',
                                                                      'style': 'danger'}]}],
                                                    'edited': {'user': 'U8M8UMEGK',
                                                               'ts': '1515178408.000000'},
                                                    'ts': '1515177650.000464'},
                               'response_url': 'https://hooks.slack.com/actions/T8M8SQEN7/295888527511/HKyQH1VOrfb2x1LxWtZy3wgq',
                               'trigger_id': '294859183604.293298830755.1ca157e51fae911fe1319553649e1d3e'})

NEW_MEMBER = {
    'token': None, 'team_id': 'T8CJ90MQV', 'api_app_id': 'A8DG4MXJT',
    'event': {'type': 'team_join',
              'user': {'id': 'U8JUVGU65', 'team_id': 'T8CJ90MQV', 'name': 'keianna.bentlee',
                       'deleted': False, 'color': '2b6836', 'real_name': 'test2',
                       'tz': 'America/Los_Angeles', 'tz_label': 'Pacific Standard Time',
                       'tz_offset': -28800, 'profile': {'real_name': 'test2', 'display_name': 'test2',
                                                        'avatar_hash': 'gffb53a06c94', 'title': '',
                                                        'real_name_normalized': 'test2',
                                                        'display_name_normalized': 'test2',
                                                        'image_24': 'https://secure.gravatar.com/avatar/ffb53a06c9414ee6b735b3b3fac1e3b7.jpg?s=24&d=https%3A%2F%2Fa.slack-edge.com%2F0180%2Fimg%2Favatars%2Fava_0025-24.png',
                                                        'image_32': 'https://secure.gravatar.com/avatar/ffb53a06c9414ee6b735b3b3fac1e3b7.jpg?s=32&d=https%3A%2F%2Fa.slack-edge.com%2F66f9%2Fimg%2Favatars%2Fava_0025-32.png',
                                                        'image_48': 'https://secure.gravatar.com/avatar/ffb53a06c9414ee6b735b3b3fac1e3b7.jpg?s=48&d=https%3A%2F%2Fa.slack-edge.com%2F66f9%2Fimg%2Favatars%2Fava_0025-48.png',
                                                        'image_72': 'https://secure.gravatar.com/avatar/ffb53a06c9414ee6b735b3b3fac1e3b7.jpg?s=72&d=https%3A%2F%2Fa.slack-edge.com%2F66f9%2Fimg%2Favatars%2Fava_0025-72.png',
                                                        'image_192': 'https://secure.gravatar.com/avatar/ffb53a06c9414ee6b735b3b3fac1e3b7.jpg?s=192&d=https%3A%2F%2Fa.slack-edge.com%2F7fa9%2Fimg%2Favatars%2Fava_0025-192.png',
                                                        'image_512': 'https://secure.gravatar.com/avatar/ffb53a06c9414ee6b735b3b3fac1e3b7.jpg?s=512&d=https%3A%2F%2Fa.slack-edge.com%2F7fa9%2Fimg%2Favatars%2Fava_0025-512.png',
                                                        'fields': None, 'team': 'T8CJ90MQV'},
                       'is_admin': False, 'is_owner': False, 'is_primary_owner': False,
                       'is_restricted': False, 'is_ultra_restricted': False, 'is_bot': False,
                       'updated': 1514339410, 'is_app_user': False, 'presence': 'away'},
              'cache_ts': 1514339410, 'event_ts': '1514339410.000044'}, 'type': 'event_callback',
    'event_id': 'Ev8JQQG672', 'event_time': 1514339410, 'authed_users': ['U8BUVSE1F', 'U8DG4B3EK']
}

USER_INFO_HAS_REAL_NAME = {
    "ok": 'true',
    "user": {
        "id": "W012A3CDE",
        "team_id": "T012AB3C4",
        "name": "spengler",
        "deleted": 'false',
        "color": "9f69e7",
        "real_name": "episod",
        "tz": "America\/Los_Angeles",
        "tz_label": "Pacific Daylight Time",
        "tz_offset": -25200,
    }
}

USER_INFO_HAS_NAME = {
    "ok": 'true',
    "user": {
        "id": "W012A3CDE",
        "team_id": "T012AB3C4",
        "name": "spengler",
        "deleted": 'false',
        "color": "9f69e7",
        "real_name": "",
    }
}

USER_INFO_NO_NAME = {
    "ok": 'true',
    "user": {
        "id": "W012A3CDE",
        "team_id": "T012AB3C4",
        "name": "",
        "deleted": 'false',
        "color": "9f69e7",
        "real_name": "",
    }
}


default_interest = [
    {
        "name": "javascript",
        "text": "JavaScript",
        "type": "button",
        "value": "javascript"
    },
    {
        "name": "python",
        "text": "Python",
        "type": "button",
        "value": "python"
    },
    {
        "name": "ruby",
        "text": "Ruby",
        "type": "button",
        "value": "ruby"
    }, {
        "name": "webdev",
        "text": "Web Dev",
        "type": "button",
        "value": "webdev"
    }

]

base_resources = {
    "text": "We recommend the following resources.",
    "attachments": [
        {
            "text": "",
            "fallback": "",
            "color": "#3AA3E3",
            "callback_id": "resource_buttons",
            "attachment_type": "default",
            "actions": default_interest
        },
        {
            "text": "",
            "fallback": "",
            "color": "#3AA3E3",
            "callback_id": "suggestion",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "suggestion_button",
                    "text": "Are we missing something? Click!",
                    "type": "button",
                    "value": "suggestion_button"
                }
            ]
        }
    ]
}

CORRECT_NAME_GREET = ("Hi spengler,\n\n Welcome to Operation Code! I'm a bot designed to help answer questions and "
              "get you on your way in our community.\n\n Our goal here at Operation Code is to get veterans and "
              "their families started on the path to a career in programming. We do that through providing you with "
              "scholarships, mentoring, career development opportunities, conference tickets, and more!\n")

UNPROCESSED_MAIN_GREET = ("Hi {real_name},\n\n Welcome to Operation Code! I'm a bot designed to help answer questions and "
              "get you on your way in our community.\n\n Our goal here at Operation Code is to get veterans and "
              "their families started on the path to a career in programming. We do that through providing you with "
              "scholarships, mentoring, career development opportunities, conference tickets, and more!\n")

CORRECT_JOINED_MESSAGE = ":tada: <@{}> has joined! :tada:"

CORRECT_GREET_BUTTON = [
        {
            'text': "",
            "fallback": "Someone should greet them!",
            "color": "#3AA3E3",
            "callback_id": "greeted",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "greeted",
                    "text": "I will greet them!",
                    "type": "button",
                    "style": "primary",
                    "value": "greeted",
                },
            ]
        }
    ]