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

HELP_MENU = {
    "text": "Click any of the buttons below to receive more information on the topic.",
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
        }
    ]
}


def greeted_response_attachments(clicker: str) -> list:
    return [
        {
            "text": f":100:<@{clicker}> has greeted the new user!:100:",
            "fallback": "",
            "color": "#3AA3E3",
            "callback_id": "greeted",
            "attachment_type": "default",
            "actions": [{
                "name": "reset_greet",
                "text": "I lied!  I can't greet them!",
                "type": "button",
                "style": "danger",
                "value": "reset_greet",
            }]
        },
    ]


def needs_greet_button() -> list:
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
