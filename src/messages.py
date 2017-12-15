MESSAGE = (
    "Hi {real_name},\n\n Welcome to Operation Code! I'm a bot designed to help answer questions and get you on your way in our community.\n\n"
    "Please take a moment to review our Code of Conduct.\n\n"
    "Our goal here at Operation Code is to get veterans and their families started on the path to a career in programming. "
    "We do that through providing you with scholarships, mentoring, career development opportunities, conference tickets, and more!\n\n"
    "You're currently in Slack, a chat application that serves as the hub of Operation Code. "
    "If you're currently visiting us via your browser, Slack provides a stand alone program to make staying in touch even more convenient.\n\n"
    "Want to make your first change to a program right now? "
    "All active Operation Code Projects are located on our source control repository. "
    "Our projects can be viewed on Github.\n\n"
    "Click any of the buttons below to receive more information on the topic.\n\n"
    "If you'd like to see something that isn't here let us know!\n\n"
    "------------------------------------------------------------------------------------------")

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

SUGGESTION_MODAL = {
    "callback_id": "suggestion_modal",
    "title": "Help topic suggestion",
    "submit_label": "Submit",
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
