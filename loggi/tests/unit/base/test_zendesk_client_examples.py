import mock
from zenpy.lib.api_objects import Ticket

from base.zendesk.zendesk_client import ZendeskClient


# Exemplo 1
def test_get_ticket():
    # given
    client = ZendeskClient(email='email@loggi.com', token='secret_token', subdomain='loggisubdomain')

    zenpy_client_mock = mock.MagicMock()
    client._zenpy_client_instance = zenpy_client_mock

    # when
    client.get_ticket(tid=123)

    # then
    assert zenpy_client_mock.tickets.called
    assert zenpy_client_mock.tickets.call_count == 1
    zenpy_client_mock.tickets.assert_called_once_with(id=123)


# Exemplo 2.a
def test_add_tag_when_has_no_tag():
    # given
    client = ZendeskClient(email='email@loggi.com', token='secret_token', subdomain='loggisubdomain')

    zenpy_client_mock = mock.MagicMock()
    mocked_ticket = mock.MagicMock(spec=Ticket, tags=[])
    zenpy_client_mock.tickets.return_value = mocked_ticket

    client._zenpy_client_instance = zenpy_client_mock

    # when
    client.add_tag(ticket_id=123, tag='any_tag')

    # then
    zenpy_client_mock.tickets.update.assert_called_once_with(mocked_ticket)


# Exemplo 2.b
def test_add_tag_when_has_tag():
    # given
    client = ZendeskClient(email='email@loggi.com', token='secret_token', subdomain='loggisubdomain')

    zenpy_client_mock = mock.MagicMock()
    mocked_ticket = mock.MagicMock(spec=Ticket, tags=['existent_tag'])
    zenpy_client_mock.tickets.return_value = mocked_ticket

    client._zenpy_client_instance = zenpy_client_mock

    # when
    client.add_tag(ticket_id=123, tag='existent_tag')

    # then
    zenpy_client_mock.tickets.update.assert_not_called()


def test_sync_ticket_comments():
    ticket_comments = ['comment1']
    actual_comments = ['comment1', 'comment2']
    expected_unpublished = ['comment1', 'comment2']

    zendesk_client = ZendeskClient(email='email@loggi.com', token='secret_token', subdomain='loggisubdomain')
    zenpy_client_mock = mock.MagicMock()

    zendesk_client._zenpy_client_instance = zenpy_client_mock

    # given
    ticket = mock.MagicMock(spec=Ticket)
    zendesk_client._publish_comment = mock.MagicMock()
    zendesk_client._publish_comment.return_value = None

    zendesk_client.zenpy_client.tickets = mock.MagicMock()
    zendesk_client.zenpy_client.tickets.return_value = ticket
    zendesk_client.zenpy_client.tickets.update.return_value = None

    zendesk_client._fetch_ticket_comments = mock.MagicMock()
    zendesk_client._fetch_ticket_comments.return_value = ticket_comments

    # when
    ticket_id = 666
    zendesk_client.sync_ticket_comments(ticket_id=ticket_id, expected_comments=actual_comments)

    # then
    zendesk_client._fetch_ticket_comments.assert_called_once_with(ticket_id=ticket_id)
    expected_publish_comment_calls = [
        mock.call(
            ticket=ticket,
            comment=comment,
            public=False,
        )
        for comment in expected_unpublished
    ]
    zendesk_client._publish_comment.assert_has_calls(
        expected_publish_comment_calls,
        any_order=False,
    )