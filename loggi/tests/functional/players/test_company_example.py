import pytest

from tests.factories.players_example import CompanyFactory


# Exemplo 1
@pytest.mark.django_db
def test_company_can_make_orders_should_be_true_when_company_is_verified():
    company = CompanyFactory.create(verified=True)

    assert company.can_make_orders() is True
