from typing import List


def get_response_type(response_data):
    return response_data['actions'][0]['value']


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
