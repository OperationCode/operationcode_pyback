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
