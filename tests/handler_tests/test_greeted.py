import pytest

from ocbot.external.route_slack import SlackBuilder
from tests.handler_tests.events import *
from ocbot.pipeline.handlers.greeted import GreetedHandler


@pytest.fixture
def greeted_handler():
    return GreetedHandler(event_dict=GREETED_EVENT)


@pytest.fixture
def reset_greet_handler():
    return GreetedHandler(event_dict=RESET_GREET_EVENT)


##  built_templates tests ##

@pytest.mark.parametrize("event, correct_params", [
    (GREETED_EVENT, CORRECT_GREETED_PARAMS),
    (RESET_GREET_EVENT, CORRECT_RESET_PARAMS)
])
def test_build_templates_gets_correct_response_type(event, correct_params):
    handler = GreetedHandler(event_dict=event)
    base_params = handler.make_base_params()
    assert base_params == correct_params


def test_build_templates_calls_was_greeted(mocker, greeted_handler):
    greeted_spy = mocker.spy(greeted_handler, "was_greeted_response_attachments")
    greeted_handler.build_templates()
    assert greeted_spy.called


def test_build_templates_calls_not_greeted(mocker, reset_greet_handler):
    not_greeted_spy = mocker.spy(reset_greet_handler, "not_greeted_attachments")
    reset_greet_handler.build_templates()
    assert not_greeted_spy.called


def test_text_dict_is_assigned_correctly_when_greeted(greeted_handler):
    greeted_handler.build_templates()
    assert greeted_handler.text_dict['message'] == CORRECT_GREET_MESSAGE


def test_text_dict_is_assigned_correctly_when_reset(reset_greet_handler):
    reset_greet_handler.build_templates()
    assert reset_greet_handler.text_dict['message'] == CORRECT_RESET_MESSAGE


##  build_response tests ##


def test_include_responses_called_with_correct_params(mocker, greeted_handler):
    greeted_handler.text_dict['message'] = CORRECT_GREET_MESSAGE
    mocker.patch.object(greeted_handler, "include_resp")
    greeted_handler.build_responses()
    assert greeted_handler.include_resp.called_with(SlackBuilder.update, CORRECT_GREET_MESSAGE)


def test_handler_added_response(greeted_handler):
    greeted_handler.text_dict['message'] = CORRECT_GREET_MESSAGE
    greeted_handler.build_responses()
    assert (SlackBuilder.update(**CORRECT_GREET_MESSAGE)) in greeted_handler.response


def test_handler_adds_multiple_responses(greeted_handler):
    greeted_handler.text_dict['message'] = CORRECT_GREET_MESSAGE
    greeted_handler.build_responses()
    greeted_handler.text_dict['message'] = RESET_GREET_EVENT
    greeted_handler.build_responses()

    assert GREETED_RESPONSE_CONTAINER in greeted_handler.response
    assert RESET_RESPONSE_CONTAINER in greeted_handler.response
