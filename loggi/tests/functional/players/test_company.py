from tests.factories.players import CompanyFactory


def test_company_factor_creation():
    company = CompanyFactory.build(with_cx_priority=True)
    company_2 = CompanyFactory.build()


def test_company_can_make_orders_when_is_verified():
    company = CompanyFactory.build(verified=True, name='Rochinha')

    assert company.can_make_orders() is True
    assert company.name == 'Rochinha'
