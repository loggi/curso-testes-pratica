import pytest

from tests.factories.players_example import LoggiUserFactory


def test_can_edit_should_be_true_for_superuser():
    user = LoggiUserFactory.build(is_admin=True)

    assert user.can_edit() is True


def test_has_cx_priority():
    user = LoggiUserFactory.build(with_priority_company=True)

    assert user.company
    assert user.company.has_cx_priority is True

    assert user.has_cx_priority() is True


def test_has_cx_priority_another():
    user = LoggiUserFactory.build(company__has_cx_priority=True)

    assert user.has_cx_priority() is True
