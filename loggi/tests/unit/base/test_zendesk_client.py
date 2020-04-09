import mock
import pytest
from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket

from base.zendesk.zendesk_client import ZendeskClient

ZENDESK_CLIENT_FAKE_CREDENTIALS = dict(
    email='email@loggi.com',
    token='secret_token',
    subdomain='loggisubdomain',
)


@pytest.fixture(
    params=[True, False],
    ids=["ticket_has_tag", "ticket_has_not_tag"]
)
def ticket(request):
    ticket = mock.MagicMock(spec=Ticket)
    ticket.tags = mock.MagicMock(spec=list)
    ticket.tags.__contains__.return_value = request.param
    return ticket


@pytest.fixture
def mock_zendesk_logger():
    p = 'base.zendesk.zendesk_client.logger'
    with mock.patch(p) as m:
        yield m


@pytest.fixture
def zendesk_client():
    return ZendeskClient(**ZENDESK_CLIENT_FAKE_CREDENTIALS)


def test_zendesk_client_lazy_instanciation_of_zenpy_client(zendesk_client):
    assert not zendesk_client._zenpy_client_instance

    # assert client is instantiated when called
    assert isinstance(zendesk_client.zenpy_client, Zenpy)


def test_add_tag(ticket, zendesk_client):

    # given
    zendesk_client.zenpy_client.tickets = mock.MagicMock()
    zendesk_client.zenpy_client.tickets.return_value = ticket
    zendesk_client.zenpy_client.tickets.update.return_value = None

    # when
    tag_to_add = 'xablau'
    ticket_id = 666
    zendesk_client.add_tag(ticket_id=ticket_id, tag=tag_to_add)

    # then
    zendesk_client.zenpy_client.tickets.assert_called_once_with(id=ticket_id)
    if tag_to_add in ticket.tags:
        assert not ticket.tags.append.called
        assert not zendesk_client.zenpy_client.tickets.update.called
    else:
        ticket.tags.append.assert_called_once_with(tag_to_add)
        zendesk_client.zenpy_client.tickets.update.assert_called_once_with(ticket)


def test_remove_tag(ticket, zendesk_client):

    # given
    zendesk_client.zenpy_client.tickets = mock.MagicMock()
    zendesk_client.zenpy_client.tickets.return_value = ticket
    zendesk_client.zenpy_client.tickets.update.return_value = None

    # when
    tag_to_remove = 'tagtag'
    ticket_id = 666
    zendesk_client.remove_tag(ticket_id=ticket_id, tag=tag_to_remove)

    # then
    zendesk_client.zenpy_client.tickets.assert_called_once_with(id=ticket_id)
    if tag_to_remove in ticket.tags:
        ticket.tags.remove.assert_called_once_with(tag_to_remove)
        zendesk_client.zenpy_client.tickets.update.assert_called_once_with(ticket)
    else:
        assert not ticket.tags.remove.called
        assert not zendesk_client.zenpy_client.tickets.update.called


def test_get_unpublished_comments_keep_order_of_expected_comments(zendesk_client):
    expected_comments = [1, 2, 20, 6, 210, 5]
    current_ticket_comments = [6, 20, 1]

    actual_unpublished_comments = zendesk_client._get_unpublished_comments(
        expected_comments=expected_comments,
        current_comments=current_ticket_comments,
    )

    expected_unpublished_comments = [2, 210, 5]

    assert actual_unpublished_comments == expected_unpublished_comments


@pytest.mark.parametrize(
    'ticket_comments, actual_comments, expected_unpublished',
    [
        ([], [], []),
        ([], ['comment1', 'comment2'], ['comment1', 'comment2']),
        (['comment1'], ['comment1', 'comment2', 'comment3'], ['comment2', 'comment3']),
        (['comment1', 'comment2'], ['comment1', 'comment2'], []),
    ],
    ids=[
        'none_comments',
        'all_comments_are_unsynced',
        'a_few_unsynced_comments',
        'synced_comments',
    ]
)
def test_sync_ticket_comments(
        ticket_comments,
        actual_comments,
        expected_unpublished,
        zendesk_client
 ):

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
    # pytest.set_trace()
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


@pytest.mark.parametrize(
    'ticket_comment',
    ['', 'comment', None],
    ids=['empty_comments', 'text_comment', 'None comment']
)
@mock.patch('base.zendesk.zendesk_client.Ticket', return_value=Ticket(id=666))
def test_add_ticket_comment(
        mock_zenpy_ticket,
        ticket_comment,
        zendesk_client
 ):
    # given
    ticket = mock_zenpy_ticket()
    zendesk_client._publish_comment = mock.MagicMock()
    zendesk_client._publish_comment.return_value = None

    # when
    ticket_id = ticket.id
    zendesk_client.add_ticket_comment(ticket_id=ticket_id, comment=ticket_comment)

    # then
    zendesk_client._publish_comment.assert_called_once_with(
        ticket=ticket,
        comment=ticket_comment,
        public=False
    )


# @pytest.mark.parametrize(
#     'ticket_comment',
#     ['', 'comment', None],
#     ids=['empty_comments', 'text_comment', 'None comment']
# )
# def test_add_ticket_comment(
#         ticket_comment,
#         zendesk_client
#  ):
#     # given
#     ticket = mock.MagicMock(spec=Ticket)
#     zendesk_client._publish_comment = mock.MagicMock()
#     zendesk_client._publish_comment.return_value = None
#
#     zendesk_client.zenpy_client.tickets = mock.MagicMock()
#     zendesk_client.zenpy_client.tickets.return_value = ticket
#     zendesk_client.zenpy_client.tickets.update.return_value = None
#
#     zendesk_client._fetch_ticket_comments = mock.MagicMock()
#     zendesk_client._fetch_ticket_comments.return_value = []
#
#     # when
#     ticket_id = 666
#     zendesk_client.add_ticket_comment(ticket_id=ticket_id, comment=ticket_comment)
#
#     # then
#     zendesk_client._fetch_ticket_comments.assert_called_once_with(ticket_id=ticket_id)
#
#     zendesk_client._publish_comment.assert_called_once_with(
#         ticket=ticket,
#         comment=ticket_comment,
#         public=False
#     )
