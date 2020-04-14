import mock
import pytest
from zenpy.lib.api_objects import Ticket

from base.zendesk.zendesk_client import ZendeskClient


@pytest.fixture
def zendesk_client():
    client = ZendeskClient(email='email@loggi.com', token='secret_token', subdomain='loggisd')

    zenpy_client_mock = mock.Mock()
    client._zenpy_client_instance = zenpy_client_mock

    return client


@mock.patch('base.zendesk.zendesk_client.logger')
def test_get_ticket(
    mocked_logger,
    zendesk_client
):
    mocked_ticket = mock.MagicMock(spec=Ticket, id=123)

    zenpy_client_mock = zendesk_client._zenpy_client_instance
    zendesk_client._zenpy_client_instance.tickets.return_value = mocked_ticket

    actual_ticket = zendesk_client.get_ticket(tid=123)

    assert actual_ticket == mocked_ticket
    assert actual_ticket.id == mocked_ticket.id

    assert zenpy_client_mock.tickets.called
    zenpy_client_mock.tickets.assert_called()
    zenpy_client_mock.tickets.assert_called_once()
    zenpy_client_mock.tickets.assert_called_once_with(id=123)

    mocked_logger.info.assert_called_once_with('A ticket was fetch from Zendesk')


def test_get_tickets():
    client = ZendeskClient(email='email@loggi.com', token='secret_token', subdomain='loggisd')

    zenpy_client_mock = mock.Mock()
    client._zenpy_client_instance = zenpy_client_mock

    client.get_tickets(tids=321)

    zenpy_client_mock.tickets.assert_called_once_with(ids=321)


def test_mark_as_open(zendesk_client):
    mocked_ticket = mock.MagicMock(spec=Ticket, id=123)

    zenpy_client_mock = zendesk_client._zenpy_client_instance
    zendesk_client._zenpy_client_instance.tickets.return_value = mocked_ticket

    zendesk_client.mark_as_open(tid=123)

    assert zenpy_client_mock.update.called
    zenpy_client_mock.update.assert_called_once_with(mocked_ticket)


def test_add_tag_when_has_no_tag(zendesk_client):
    mocked_ticket = mock.MagicMock(spec=Ticket, id=123, tags=[])
    zendesk_client.get_ticket = mock.Mock(return_value=mocked_ticket)

    zenpy_mock = zendesk_client._zenpy_client_instance

    zendesk_client.add_tag(ticket_id=123, tag='any_tag')

    # using assert_called_once_with
    zenpy_mock.tickets.update.assert_called_once_with(mocked_ticket)

    # same assert using assert_has_calls, can be used for multiple calls
    expected_calls = [mock.call(mocked_ticket)]
    zenpy_mock.tickets.update.assert_has_calls(expected_calls, any_order=False)


def test_add_tag_when_has_tag(zendesk_client):
    mocked_ticket = mock.MagicMock(spec=Ticket, id=123, tags=['any_tag'])
    zendesk_client.get_ticket = mock.Mock(return_value=mocked_ticket)

    zenpy_mock = zendesk_client._zenpy_client_instance

    zendesk_client.add_tag(ticket_id=123, tag='any_tag')

    assert not zenpy_mock.tickets.update.called
    assert zenpy_mock.tickets.update.call_count == 0
    zenpy_mock.tickets.update.assert_not_called()
