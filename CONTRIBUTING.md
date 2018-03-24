## Quick Start Guide

#### Installation
##### Python
- Clone this repository
    - `git clone https://github.com/OperationCode/operationcode_pyback.git`
- (Optional, but recommended) Create a new virtual environment using something like [virtualenv](https://virtualenv.pypa.io/en/stable/) or [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
- Install dependencies
    - In the root project directory: `pip install -r requirements.txt`

##### Slack
As most of our functionality deals with interactions with the slack API the easiest way to setup a development environment is to create a test Slack Workspace.

- Click the `Get Started` button on https://slack.com
- Click `Create a new workspace`
- Create your workspace
- Go to https://api.slack.com/
    - sign in to your workspace if you aren't already
-  Click Your Apps in the upper right
- Select Create New App
    - Enter the App name and select your development workspace

At this point you'll need a few pieces of information to correctly configure the application.
- First create a file `.env` in the root folder of your pyback directory
- Click the `Install App` tab under settings and install the app to your workspace
- Find the following in your slack app
    - `OAuth Access Token` on the Install App page
    - `Verification Token` on the Basic Information page
- Enter the tokens into your .env file in the form on
    - `DEV_BOT_TOKEN = '[Oauth token]'`
    - `DEV_AUTH_TOKEN = '[verification token]'`

![.env image](/images/env.png)

Here's where things get a bit tricky.  You need to find the ID of the channel you want the bot to post messages to.
To do this we're going to use the Slack API, particularly the [channels.list](https://api.slack.com/methods/channels.list) method.

There are a few different ways you can accomplish this.
You can use a tool like curl or [Postman](https://www.getpostman.com/) to interact with the API directly, or you can use the python Slack client.

###### Postman
![postman](/images/postman.png)

###### Python Terminal and Slack Client
![channels](/images/channelsWithClient.png)

Add the channel id to your .env file as `DEV_PRIVATE_CHANNEL = '[channel-id]`

Go ahead and run the `run.py` file, the server should successfully start.

The only thing left to do is configure a public facing URL that slack can use to send events.
You could use a hosting service to accomplish this but we frequently use [ngrok](https://ngrok.com/) to create a temporary URL that forwards
all traffic to your localhost.

After downloading ngrok create a temporary url on port 5000 using `ngrok http 5000` (or a similar command depending on your OS and where you saved the file)

You'll something like the below image.

![ngrok](/images/ngrok.png)

We now need to tell Slack to send all events to your forwarding URL.

Back in the Slack App console select the `Event Subscription` tab and click the enable events slider.

Our app is listening for events at the `/events_endpoint` url, so our request URL is `[ngrok url]/events_endpoint`

![events](/images/events.png)

Similarly for the interactive components, our app is listening at `/user_interaction` and `/options_load`

![interactive](/images/interactive.png)