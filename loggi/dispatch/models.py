# coding: utf-8

CITY_ENABLE = {
    'São Paulo': True,
    'Belo Horizonte': False
}

ORDER_ALLOCATING = 'allocating'
ORDER_ACCEPTED = 'accepted'
ORDER_STARTED = 'started'
ORDER_REQUIRES_VERIFICATION = 'requires_verification'
ORDER_AWAITING_COMPLETION = 'awaiting_completion'
ORDER_FINISHED = 'finished'
ORDER_CANCELLED = 'cancelled'
ORDER_DROPPED = 'dropped'

ONGOING_STATUS = {
    ORDER_STARTED: True,
    ORDER_ACCEPTED: True
}

VALID_ORDER_STATUSES_FOR_EDIT_REQUEST = set([
    ORDER_ALLOCATING,
    ORDER_ACCEPTED,
    ORDER_STARTED,
])


def check_feature_switch():
    return True


class EditOrderWorkMemory(object):
    def can_be_cancelled(self):
        self.order.status = ORDER_STARTED


class Order(object):
    def __init__(self, city, status):
        self.city = city

    def is_ongoing(self):
        return ONGOING_STATUS.get(self.status)

    def can_edit_for_classic(self):

        order = self
        is_feature_enabled = CITY_ENABLE.get(self.city)

        return (order.status == 'allocating' or self.is_ongoing()) and is_feature_enabled

    def can_edit_for_retail(self):
        handler = EditOrderWorkMemory(order=self)

        has_editable_status = (
            self.status in VALID_ORDER_STATUSES_FOR_EDIT_REQUEST
        )

        if has_editable_status and handler.can_be_cancelled:
            return check_feature_switch()

        return False
