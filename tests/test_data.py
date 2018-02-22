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

MESSAGE_EVENT = {'token': None, 'team_id': 'T8CJ90MQV', 'api_app_id': 'A8DG4MXJT',
                 'event': {'type': 'message', 'user': 'U8FDR1603', 'text': 'testgreet', 'ts': '1514338591.000084',
                           'channel': 'G8FFLSKTR', 'event_ts': '1514338591.000084'}, 'type': 'event_callback',
                 'event_id': 'Ev8JQNFQ6L', 'event_time': 1514338591, 'authed_users': ['U8BUVSE1F']}

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

CHANNELS = {
    u'C8DA69KM4': {
        u'last_read': u'0000000000.000000', u'created': 1459497074,
        u'unread_count': 1, u'is_open': True, u'user': u'USLACKBOT',
        u'unread_count_display': 1, u'latest': {
            u'text': u'message from slackbot',
            u'type': u'message', u'user': u'USLACKBOT',
            u'ts': u'1459502580.797060'
        }, u'is_im': True, u'id': u'D0X6385P1', u'has_pins': False
    },
}
# not my tokens
CHALLENGE = {

    "challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P",
    "type": "url_verification"
}
CALLBACK_GENERIC = {
    "actions": [
        {
            "name": "slack",
            "value": "slack",
            "type": "button"
        }
    ],
    "callback_id": None,
    "team": {
        "id": "T47563693",
        "domain": "watermelonsugar"
    },
    "channel": {
        "id": "C065W1189",
        "name": "forgotten-works"
    },
    "user": {
        "id": "U8FDR1603",
        "name": "brautigan"
    },
    "action_ts": "1458170917.164398",
    "message_ts": "1458170866.000004",
    "attachment_id": "1",
    "token": "xAB3yVzGS4BQ3O9FACTa8Ho4",
    "original_message": {"text": "New comic book alert!", "attachments": [
        {"title": "The Further Adventures of Slackbot",
         "fields": [{"title": "Volume", "value": "1", "short": True}, {"title": "Issue", "value": "3", "short": True}],
         "author_name": "Stanford S. Strickland",
         "author_icon": "https://api.slack.comhttps://a.slack-edge.com/bfaba/img/api/homepage_custom_integrations-2x.png",
         "image_url": "http://i.imgur.com/OJkaVOI.jpg?1"}, {"title": "Synopsis",
                                                            "text": "After @episod pushed exciting changes to a devious new branch back in Issue 1, Slackbot notifies @don about an unexpected deploy..."},
        {"fallback": "Would you recommend it to customers?", "title": "Would you recommend it to customers?",
         "callback_id": "comic_1234_xyz", "color": "#3AA3E3", "attachment_type": "default",
         "actions": [{"name": "recommend", "text": "Recommend", "type": "button", "value": "recommend"},
                     {"name": "no", "text": "No", "type": "button", "value": "bad"}]}]},
    "response_url": "https://hooks.slack.com/actions/T47563693/6204672533/x7ZLaiVMoECAW50Gw1ZYAXEM",
    "trigger_id": "13345224609.738474920.8088930838d88f008e0"
}
