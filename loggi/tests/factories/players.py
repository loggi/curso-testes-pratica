import factory

from players.models import Company, LoggiUser


class CompanyFactory(factory.DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Faker('company', locale='pt_BR')
    cnpj = factory.Sequence(lambda n: n)
    landline_1 = '1123653243'

    class Params:
        with_cx_priority = factory.Trait(
            has_cx_priority=True,
            verified=True,
        )


class LoggiUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = LoggiUser

    username = factory.LazyAttribute(
        lambda user: '{}.{}'.format(user.first_name, user.last_name).lower()
    )
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    mobile_1 = '11999888777'
    email = factory.LazyAttribute(
        lambda user: '{}.{}@loggi.com'.format(user.first_name, user.last_name).lower()
    )
    password = factory.PostGenerationMethodCall('set_password', 'senha-segura')
    company = factory.SubFactory(CompanyFactory)

    class Params:
        is_admin = factory.Trait(
            is_superuser=True,
            is_staff=True,
        )
        with_priority_company = factory.Trait(
            company=factory.SubFactory(CompanyFactory, with_cx_priority=True)
        )
