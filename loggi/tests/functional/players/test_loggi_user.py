import pytest

from tests.factories.players import LoggiUserFactory


@pytest.mark.django_db
def test_is_mobile_unique_should_be_true():
    user = LoggiUserFactory.create(mobile_1='11988039111')

    assert user.is_mobile_unique()


@pytest.mark.django_db
def test_is_mobile_unique_should_not_be_true():
    user = LoggiUserFactory.create(mobile_1='11988039111')
    user_2 = LoggiUserFactory.create(mobile_1='11988039111')

    assert not user.is_mobile_unique()
    assert not user_2.is_mobile_unique()


@pytest.mark.django_db
def test_save_sets_full_name():
    user = LoggiUserFactory.build(first_name='Zeca', last_name='Pagodinho', company=None)
    assert user.full_name == ''

    user.save()

    assert user.full_name == 'Zeca Pagodinho'


@pytest.mark.django_db
def test_disable():
    user = LoggiUserFactory.create(is_admin=True, email='zeca@loggi.com')

    assert user.original_email is None
    assert user.mobile_1 is not ''
    assert user.is_active
    assert user.is_superuser
    assert user.is_staff

    user.disable()

    assert user.original_email == 'zeca@loggi.com'
    assert user.email == 'inativo+{}@loggi.com'.format(user.pk)
    assert user.mobile_1 == ''
    assert not user.is_active
    assert not user.is_superuser
    assert not user.is_staff
