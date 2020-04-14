import logging

from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket, Comment

from base.zendesk.const import ZENDESK_TICKET_TYPE

logger = logging.getLogger('loggi.zendesk.base.zendesk_client')


class ZendeskClient(object):
    """Provides a client interface with Zendesk, using `zenpy` API wrappers."""

    def __init__(self, email, token, subdomain):
        self.email = email
        self.token = token
        self.subdomain = subdomain
        self._zenpy_client_instance = None

    @property
    def zenpy_client(self):
        """Zenpy client singleton.

        This property assures that Zenpy client is instantiated only once.
        """
        if self._zenpy_client_instance is None:
            self._zenpy_client_instance = Zenpy(
                        email=self.email,
                        token=self.token,
                        subdomain=self.subdomain,
                    )
        return self._zenpy_client_instance

    def send_message(self, title, message, **extra):
        """Send a given message as a ticket to zendesk.

        Args:
            title (basestring): ticket title.
            message (basestring): ticket message.
            extra (dict): extra arguments to be sent in the ticket, such as:
                tags, custom_fields, ticket_form_id.

        Returns:
            dict: with response from zendesk.

        """
        ticket = Ticket(
            subject=title,
            description=message,
            requester=self.get_requester(extra['requester_email']),
            tags=extra.get('tags', None),
            custom_fields=extra.get('custom_fields', None),
            ticket_form_id=(extra.get('form_id', None) or
                            extra.get('ticket_form_id', None)),
        )

        ticket_status = extra.get('status', None)
        if ticket_status:
            ticket.status = ticket_status

        ticket_is_internal = extra.get('is_internal', None)
        if ticket_is_internal:
            ticket.is_internal = ticket_is_internal

        return self.zenpy_client.tickets.create(ticket)

    def get_ticket(self, tid):
        logger.info('A ticket was fetch from Zendesk')
        return self.zenpy_client.tickets(id=tid)

    def get_tickets(self, tids):
        return self.zenpy_client.tickets(ids=tids)

    def search_tickets(self, status, ticket_form_id):
        return self.zenpy_client.search(
            type=ZENDESK_TICKET_TYPE,
            status=status,
            ticket_form_id=ticket_form_id,
        )

    def mark_as_open(self, tid):
        ticket = self.get_ticket(tid=tid)
        ticket.status = 'open'
        return self.zenpy_client.update(ticket)

    def mark_as_pending(self, tid):
        ticket = self.get_ticket(tid=tid)
        ticket.status = 'pending'
        return self.zenpy_client.update(ticket)

    def mark_as_solved(self, tid):
        ticket = self.get_ticket(tid=tid)
        ticket.status = 'solved'
        return self.zenpy_client.update(ticket)

    def get_requester(self, email):
        """Return requester id by email.

        Args:
            email (basestring): requester email

        Returns:
            Optional[zenpy.lib.api_objects.User]: requester instance if found,
                otherwise ``None``.

        """
        requesters = self.zenpy_client.search(
            type='user',
            email=email
        )
        for requester in requesters:
            return requester
        return None

    def add_tag(self, ticket_id, tag):
        ticket = self.get_ticket(tid=ticket_id)

        has_not_tag = tag not in ticket.tags
        if has_not_tag:
            ticket.tags.append(tag)
            self.zenpy_client.tickets.update(ticket)

    def remove_tag(self, ticket_id, tag):
        ticket = self.get_ticket(tid=ticket_id)

        has_tag = tag in ticket.tags
        if has_tag:
            ticket.tags.remove(tag)
            self.zenpy_client.tickets.update(ticket)

    def sync_ticket_comments(self, ticket_id, expected_comments):
        ticket = self.get_ticket(tid=ticket_id)
        current_ticket_comments = self._fetch_ticket_comments(ticket_id=ticket_id)

        unpublished_ticket_comments = self._get_unpublished_comments(
            expected_comments=expected_comments,
            current_comments=current_ticket_comments,
        )

        return [
            self._publish_comment(ticket=ticket, comment=comment, public=False)
            for comment in unpublished_ticket_comments
        ]

    def add_ticket_comment(self, ticket_id, comment, public=False):
        ticket = Ticket(id=ticket_id)
        return self._publish_comment(ticket=ticket, comment=comment, public=public)

    def _fetch_ticket_comments(self, ticket_id):
        return [
            comment.body
            for comment in self.zenpy_client.tickets.comments(ticket_id=ticket_id)
        ]

    @staticmethod
    def _get_unpublished_comments(expected_comments, current_comments):
        return [
            comment
            for comment in expected_comments
            if comment not in set(current_comments)
        ]

    def _publish_comment(self, ticket, comment, public):
        ticket.comment = Comment(body=comment, public=public)
        return self.zenpy_client.tickets.update(ticket)
