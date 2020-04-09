import factory

from players.models import LoggiUser, Company


class CompanyFactory(factory.DjangoModelFactory):

    class Meta:
        model = Company

    name = factory.Faker('company', locale='pt_BR')
    shared_name = factory.Faker('last_name')
    cnpj = factory.Sequence(lambda n: n)
    landline_1 = '1123864321'

    company = factory.RelatedFactory('tests.factories.players_example.LoggiUserFactory', 'company')

    @factory.post_generation
    def with_user(self, create, extracted, **kwargs):

        if not create or not extracted:
            return
        return LoggiUserFactory.create(company=self)

    class Params:
        with_cx_priority = factory.Trait(
            has_cx_priority=True,
            verified=True,
        )


class LoggiUserFactory(factory.DjangoModelFactory):

    class Meta:
        model = LoggiUser

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    mobile_1 = '11999888777'
    email = factory.LazyAttribute(lambda user: '{0}.{1}@loggi.com'.format(user.first_name, user.last_name).lower())
    username = factory.LazyAttribute(lambda user: user.email.split('@')[0])
    password = factory.PostGenerationMethodCall('set_password', 'senha-segura')

    company = factory.SubFactory(CompanyFactory)

    @factory.post_generation
    def with_company(self, create, extracted, **kwargs):

        if not create or not extracted:
            return

        company = CompanyFactory.create()
        self.company = company
        self.save()

        return company

    class Params:
        is_admin = factory.Trait(
            is_superuser=True,
            is_staff=True,
        )
        with_priority_company = factory.Trait(
            company=factory.SubFactory(CompanyFactory, with_cx_priority=True)
        )
