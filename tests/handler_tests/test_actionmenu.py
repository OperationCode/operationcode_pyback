import pytest

from ocbot.pipeline.handlers.actionmenu import ActionMenuHandler
from tests.handler_tests.action_menu_events import *


@pytest.fixture
def suggestion_clicked():
    return ActionMenuHandler(event_dict=SUGGESTION_CLICKED_EVENT)

# Suggestion
def test_suggestion_has_correct_call(suggestion_clicked: ActionMenuHandler):
    suggestion_clicked.build_templates()
    assert suggestion_clicked.text_dict['call'] == 'dialog'


def test_suggestion_dialog_has_correct_trigger_id(suggestion_clicked: ActionMenuHandler):
    suggestion_clicked.build_templates()
    assert suggestion_clicked.text_dict['dialog']['trigger_id'] == SUGGESTION_CLICKED_EVENT['trigger_id']


def test_suggestion_dialog_attaches_dialog(mocker, suggestion_clicked: ActionMenuHandler):
    modal_spy = mocker.spy(suggestion_clicked, 'SUGGESTION_MODAL')
    suggestion_clicked.build_templates()
    assert modal_spy.called