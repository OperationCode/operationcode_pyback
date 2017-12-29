text_greet = "Hi {real_name},\n\n Welcome to Operation Code! I'm a bot designed to help answer questions and get you on your way in our community.\n\n Our goal here at Operation Code is to get veterans and their families started on the path to a career in programming. We do that through providing you with scholarships, mentoring, career development opportunities, conference tickets, and more!\n\nWant to make your first change to a program right now?"

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
external_buttons = {
    "text": "The aid we provide requires veteran status *please click the attached link* to verify your status if you qualify for optional services.\n\nYou're currently in Slack, a chat application that serves as the hub of Operation Code. If you're visiting us via your browser, Slack provides a stand alone program to make staying in touch even more convenient.\n\nAll active Operation Code Projects are located on our source control repository.Our projects can be viewed on Github\n\n Lastly, please take a moment to review our Code of Conduct",
    "attachments": [
        {
            "text": "",
            "fallback": "",
            "color": "#3AA3E3",
            "callback_id": "external_buttons",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "verify",
                    "text": "Verify Veteran Status",
                    "type": "button",
                    "value": "verify",
                    "url": "https://operationcode.org/profile",
					"style":"primary"
                },
				{
                    "name": "github",
                    "text": "GitHub",
                    "type": "button",
                    "value": "github",
                    "url": "https://github.com/OperationCode"
                },
                {
                    "name": "download",
                    "text": "Slack Client",
                    "type": "button",
                    "value": "download",
                    "url": "https://slack.com/downloads"
                },
                {
                    "name": "code_of_conduct",
                    "text": "Code of Conduct",
                    "type": "button",
                    "value": "code_of_conduct",
                    "url": "https://op.co.de/code-of-conduct"
                }
            ]
        }
    ]
}

resources = {
    "text": "We recommend the following resources.",
    "attachments": [
        {
            "text": "",
            "fallback": "",
            "color": "#3AA3E3",
            "callback_id": "resource_buttons",
            "attachment_type": "default",
            "actions": None          # add in builder step
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