from mock import patch, Mock

from tests.factories.players import LoggiUserFactory


def test_email_generation():
    user = LoggiUserFactory.build()


@patch('players.models.Company.has_cx_priority')
def test_has_cx_priority_with_priority_company(mocked_has_cx_priority):
    user = LoggiUserFactory.build(with_priority_company=True)

    mocked_has_cx_priority.side_effect = Exception('DEU PAU')
    assert user.has_cx_priority()


def test_has_cx_priority_with_no_company():
    user = LoggiUserFactory.build(company=None)

    assert not user.has_cx_priority()


def test_admin_user_can_edit():
    user = LoggiUserFactory.build(is_admin=True)

    assert user.can_edit()


def test_non_admin_user_cannot_edit():
    user = LoggiUserFactory.build()

    assert not user.can_edit()
