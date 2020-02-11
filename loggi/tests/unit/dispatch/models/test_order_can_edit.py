# coding: utf-8
from __future__ import absolute_import, unicode_literals
import pytest

from dispatch.models import (
    ORDER_ALLOCATING,
    ORDER_ACCEPTED,
    ORDER_STARTED,
    ORDER_REQUIRES_VERIFICATION,
    ORDER_AWAITING_COMPLETION,
    ORDER_FINISHED,
    ORDER_CANCELLED,
    ORDER_DROPPED,
    BELO_HORIZONTE,
    SAO_PAULO,
    Order,
)


@pytest.mark.parametrize('order_status, city, method, expected_value', [
    (ORDER_ACCEPTED, SAO_PAULO, 'can_edit_for_retail', True),
    (ORDER_CANCELLED, BELO_HORIZONTE, 'can_edit_for_retail', False),
    (ORDER_ACCEPTED, SAO_PAULO, 'can_edit_for_classic', True),
    (ORDER_CANCELLED, BELO_HORIZONTE, 'can_edit_for_classic', False),
    (ORDER_STARTED, SAO_PAULO, 'can_edit_for_classic', True)
])
def test_should_validate_can_edit_field(
    order_status, city, method, expected_value
):
    order = Order(status=order_status, city=city)

    assert getattr(order, method)() is expected_value
