
# [OperationCodePyBot](https://github.com/OperationCode/operation_code_pybot)



OperationCode PyBot is a python implementation slack chat bot built to deal with the [Slack Events API](https://api.slack.com/events).

## First Version

### New implementation of introduction bot

When new individuals join \#General we wish to contact them through a private message. 

Using the previous version of [OperationCodeBot](https://github.com/OperationCode/operationcode_bot), we are given a general idea for how to handle events:

When a subscribed event occurs:
  * Slack sends a POST to this bot
  * The bot processes the event and calls a method with the same name as the event passed in
  * The event named method does whatever tasks are needed


This first iteration will perform the following: 
  * Subscribe to the `team-join` event
  * Grab user name and construct message
  * Send private message to user with formatted information. 
  

## Version

Due to the [PEP 404](https://www.python.org/dev/peps/pep-0404/) announcement support of python 3 will be the standard. The initial release will be with 3.6.X. 



## Resources

* [Slack Bot Tutorial](https://www.fullstackpython.com/blog/build-first-slack-bot-python.html)
* [Slack Events API Framework](https://github.com/slackapi/python-slack-events-api)
* [Python Slack Client](https://github.com/slackapi/python-slackclient)
* [Slack RTM API Framework](https://github.com/slackapi/python-rtmbot)
* [Slack API/Documentation](https://api.slack.com/apps/A7NGBPBUL/general)




## Contributing

Bug reports and pull requests are welcome on [Github](https://github.com/OperationCode/operation_code_pybot). This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the [Contributor Covenant](http://contributor-covenant.org) code of conduct. If you wish to assist, join the [\#new-team-rewrite](https://operation-code.slack.com/messages/C7NJLCCMB/) rewrite to learn how to contribute. 


## License

This package is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).

