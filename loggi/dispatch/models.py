# coding: utf-8

SAO_PAULO = 'São Paulo'
BELO_HORIZONTE = 'Belo Horizonte'

CITY_ENABLE = {
    SAO_PAULO: True,
    BELO_HORIZONTE: False
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
    def __init__(self, order):
        self.order = order

    def can_be_cancelled(self):
        return not self.order.has_return and not self.order.has_packages_to_be_delivered


class Order(object):
    def __init__(self, city, status, has_return=False, has_packages_to_be_delivered=False):
        self.city = city
        self.status = status
        self.has_return = has_return
        self.has_packages_to_be_delivered=has_packages_to_be_delivered

    def is_ongoing(self):
        return ONGOING_STATUS.get(self.status)

    def can_edit_for_classic(self):

        order = self
        is_feature_enabled = CITY_ENABLE.get(self.city)
        return (order.status == ORDER_ALLOCATING or self.is_ongoing() is True) and is_feature_enabled

    def can_edit_for_retail(self):
        handler = EditOrderWorkMemory(order=self)

        has_editable_status = (
            self.status in VALID_ORDER_STATUSES_FOR_EDIT_REQUEST
        )

        if has_editable_status and handler.can_be_cancelled:
            return check_feature_switch()

        return False
