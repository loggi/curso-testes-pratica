import pytest

from tests.factories.players_example import LoggiUserFactory


@pytest.mark.django_db
def test_is_mobile_unique_should_be_false_if_another_user_exists():
    mobile_phone = '11988039119'

    user_1 = LoggiUserFactory.create(mobile_1=mobile_phone)

    assert user_1.is_mobile_unique() is True

    user_2 = LoggiUserFactory.create(mobile_1=mobile_phone)

    assert user_1.is_mobile_unique() is False
    assert user_2.is_mobile_unique() is False


@pytest.mark.django_db
def test_has_cx_priority():
    user = LoggiUserFactory.create(with_priority_company=True)

    assert user.company
    assert user.company.has_cx_priority is True

    assert user.has_cx_priority() is True


@pytest.mark.django_db
def test_disable():
    user = LoggiUserFactory.create()
    assert user.is_active

    expected_original_email = user.email

    user.disable()

    assert (user.is_active and user.is_superuser and user.is_staff) is False

    assert user.original_email == expected_original_email


@pytest.mark.django_db
def test_save_should_set_full_name():
    user = LoggiUserFactory.build(first_name='Zeca', last_name='Pagodinho', company=None)

    assert user.full_name == ''
    user.save()

    assert user.full_name == 'Zeca Pagodinho'
