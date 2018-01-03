from typing import List

from .abc import RouteHandler
from ocbot.pipeline.utils import get_response_type

from ocbot.external.route_slack import SlackBuilder


class ActionMenuHandler(RouteHandler):
    """
        Handles the interactive message sent to the #community channel
        when a new member joins.

        Displays the user that claimed the greeting along with the option
        to un-claim
    """

    def __init__(self, *, event_dict):
        self._user_id = event_dict['user']['id']
        self._event = event_dict
        self._click_type = get_response_type(self._event)
        super().__init__()

    def api_calls(self):
        pass

    # TODO get resource from clicked event
    def database_calls(self):
        if self._click_type == 'resource_buttons':
            pass
        pass

    def build_templates(self):
        self.trigger_id = self._event['trigger_id']

        # suggestion
        if self._click_type == 'suggestion_button':
            self.text_dict['call'] = 'dialog'
            self.text_dict['dialog'] = {
                'trigger_id': self.trigger_id,
                'dialog': self.SUGGESTION_MODAL()
            }


        # mentor
        elif self._click_type == 'mentor':
            self.text_dict['call'] = 'dialog.open'
            self.text_dict['dialog'] = MENTOR_REQUEST_MODAL
            self.text_dict['dialog']['trigger_id'] = self.trigger_id

        # resources
        else:
            self._click_type = self._event['actions'][0]['name']
            self.text_dict['call'] = 'update'
            self.text_dict['dialog'] = self.make_base_params()

    def build_responses(self):
        params = self.text_dict['dialog']
        method = self.text_dict['call']

        self.include_resp(getattr(SlackBuilder, method), **params)

    def make_base_params(self):
        text = HELP_MENU_RESPONSES[self._click_type]
        return {'text': text,
                'channel': self._event['channel']['id'],
                'ts': self._event['message_ts'],
                'as_user': True
                }

    def SUGGESTION_MODAL(self):
        return {
            "callback_id": "suggestion_modal",
            "title": "Help topic suggestion",
            "submit_label": "Submit",
            "trigger_id": self.trigger_id,
            "elements": [
                {
                    "type": "text",
                    "label": "Suggestion",
                    "name": "suggestion",
                    "placeholder": "Underwater Basket Weaving"
                },
            ]
        }


MENTOR_REQUEST_MODAL = {
    "callback_id": "mentor_request",
    "title": "Mentor Service Request",
    "submit_label": "Submit",
    "elements": [
        {
            "value": "test",
            "type": "text",
            "label": "Slack User Name",
            "name": "Slack User",
            "placeholder": ""
        },
        {
            "value": "test@test.com",
            "type": "text",
            "subtype": "email",
            "label": "Email",
            "name": "Email",
            "placeholder": ""
        },
        {

            "type": "select",
            "label": "Service Type",
            "name": "service",
            "placeholder": "Choose a service type",
            "options": [
                {
                    "label": "General Guidance - Voice Chat",
                    "value": "General Guidance - Voice Chat"
                },
                {
                    "label": "General Guidance - Slack Chat",
                    "value": "General Guidance - Slack Chat"
                },
                {
                    "label": "Pair Programming",
                    "value": "Pair Programming"
                },
                {
                    "label": "Code Review",
                    "value": "Code Review"
                },
                {
                    "label": "Mock Interview",
                    "value": "Mock Interview"
                },
                {
                    "label": "Resume Review",
                    "value": "Resume Review"
                },

            ]
        },
        {
            "type": "select",
            "label": "Mentor Skillset",
            "name": "skillset",
            "optional": "true",
            "placeholder": "Choose a service type",
            "options": [
                {
                    "label": "Web (Frontend Development)",
                    "value": "Web (Frontend Development)",
                },
                {
                    "label": "Web (Backend Development)",
                    "value": "Web (Backend Development)",
                },
                {
                    "label": "Mobile (Android)",
                    "value": "Mobile (Android)",
                },
                {
                    "label": "Mobile (iOS)",
                    "value": "Mobile (iOS)",
                },
                {
                    "label": "C / C++",
                    "value": "C / C++",
                },
                {
                    "label": "C# / .NET",
                    "value": "C# / .NET",
                },
                {
                    "label": "Data Science",
                    "value": "Data Science",
                },
                {
                    "label": "DevOps",
                    "value": "DevOps",
                },
                {
                    "label": "Design / UX",
                    "value": "Design / UX"
                },
                {
                    "label": "Java",
                    "value": "Java",
                },
                {
                    "label": "Javascript",
                    "value": "Javascript",
                },
                {
                    "label": "Python",
                    "value": "Python",
                },
                {
                    "label": "Ruby / Rails",
                    "value": "Ruby / Rails",
                },
                {
                    "label": "SQL",
                    "value": "SQL",
                },
            ]
        },
        {
            "type": "textarea",
            "label": "Additional Details",
            "name": "Additional Details",
            "optional": "true",
            "placeholder": "Please provide us with any more info that may help in us in assigning a mentor to this "
                           "request. "
        },
    ]
}

HELP_MENU = {
    "text": "Click a button below and info will show up here!",
    "attachments": [
        {
            "text": "",
            "fallback": "",
            "color": "#3AA3E3",
            "callback_id": "greeting_buttons",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "mentor",
                    "text": "I need a mentor!",
                    "type": "button",
                    "value": "mentor",

                },
                {
                    "name": "slack",
                    "text": "Slack Info",
                    "type": "button",
                    "value": "slack",

                },

                {
                    "name": "javascript",
                    "text": "JavaScript",
                    "type": "button",
                    "value": "js_help",
                },
                {
                    "name": "python",
                    "text": "Python",
                    "type": "button",
                    "value": "python_help",
                },
                {
                    "name": "ruby",
                    "text": "Ruby",
                    "type": "button",
                    "value": "ruby_help",
                },

            ]
        },
        {
            "text": "",
            "fallback": "",
            "color": "#3AA3E3",
            "callback_id": "greeting_buttons",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "suggestion",
                    "text": "Are we missing something? Click!",
                    "type": "button",
                    "value": "suggestion",
                },
            ]
        }
    ]
}


def greeted_response_attachments(clicker: str) -> List[dict]:
    return [
        {
            "text": f":100:<@{clicker}> has greeted the new user!:100:",
            "fallback": "",
            "color": "#3AA3E3",
            "callback_id": "greeted",
            "attachment_type": "default",
            "actions": [{
                "name": "reset_greet",
                "text": f"Reset {clicker}'s claim",
                "type": "button",
                "style": "danger",
                "value": "reset_greet",
            }]
        }
    ]


def needs_greet_button() -> List[dict]:
    return [
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


#  This is super ugly.  Maybe convert to JSON and store in another file?
HELP_MENU_RESPONSES = {
    'slack': """Slack is an online chatroom service that the Operation Code community uses.
It can be accessed online, via https://operation-code.slack.com/ or via
desktop or mobile apps, located at https://slack.com/downloads/. In addition to
chatting, Slack also allows us to share files, audio conference and even program
our own bots! Here are some tips to get you started:
  - You can customize your notifications per channel by clicking the gear to the
    left of the search box
  - Join as many channels as you want via the + next to Channels in the side bar.""",

    'python': """Python is a widely used high-level programming language used for general-purpose programming.
It's very friendly for beginners and is great for everything from web development to 
data science.

Here are some python resources:
    Operation Code Python Room: <#C04D6M3JT|python>
    Python's official site: https://www.python.org/
    Learn Python The Hard Way: https://learnpythonthehardway.org/book/
    Automate The Boring Stuff: https://automatetheboringstuff.com/""",
    'mentor': """The Operation Code mentorship program aims to pair you with an experienced developer in order to further your programming or career goals. When you sign up for our mentorship program you'll fill out a form with your interests. You'll then be paired up with an available mentor that best meets those interests.

If you're interested in getting paired with a mentor, please fill out our sign up form here: http://op.co.de/mentor-request.
    """,

    'javascript': """Javascript is a high-level programming language used for general-purpose programming.
In recent years it has exploded in popularity and with the popular node.js runtime
environment it can run anywhere from the browser to a server.

Here are some javascript resources:
    Operation Code Javascript Room: <#C04CJ8H2S|javascript>
    Javascript Koans: https://github.com/mrdavidlaing/javascript-koans
    Eloquent Javascript: http://eloquentjavascript.net/
    Node School: http://nodeschool.io/
    Node University: http://node.university/courses""",
    'ruby': """Ruby is one of the most popular languages to learn as a beginner.
While it can be used in any situation it's most popular for it's
web framework 'Rails' which allows people to build websites quickly 
and easily.

Here are some ruby resources:
    Operation Code Ruby Room: <#C04D6GTGT|ruby>
    Try Ruby Online: http://tryruby.org/
    Learn Ruby The Hard Way: http://ruby.learncodethehardway.org/book
    Learn To Program: http://pine.fm/LearnToProgram/
    Ruby Koans: http://rubykoans.com/"""
}
