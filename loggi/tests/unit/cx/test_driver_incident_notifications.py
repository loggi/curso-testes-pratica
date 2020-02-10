# coding: utf-8

from __future__ import absolute_import, unicode_literals
import pytest
from cx.notifications.driver_incident_notifications import calculate_company_max_name_size


SMS_TEMPLATE_WITHOUT_ENOUGH_SPACE_FOR_COMPANY_NAME = \
    '{company_name} precisa que você resolva o incidente em até ' \
    '{self_help_timeout} através do link {shared_short_url} ' \
    '[Complemento pra atingir 160 caracteres xxxxxxxxxxxxxxxxxxx]'


@pytest.mark.parametrize(
    'url,result',
    [('www.resolvaaqui.com', 13),
     ('www.resolvaaquixxxxxxx.com', 6)])
def test_calculate_company_max_name_size(
        url, result
):

    max_company_name_size = calculate_company_max_name_size(
        template=SMS_TEMPLATE_WITHOUT_ENOUGH_SPACE_FOR_COMPANY_NAME,
        timeout_str='13:08',
        name='',
        url=url
    )
    assert max_company_name_size == result


@pytest.mark.parametrize(
    'url',
    ['www.resolvaaquixxxxxxxx.com',
     'www.resolvaaquixxxxxxxxxxxxx.com',
     'www.resolvaaquixxxxxxxxxxxxxxx.com'])
def test_calculate_company_max_name_size_raises(
        url
):
    with pytest.raises(Exception) as excinfo:
        calculate_company_max_name_size(
            template=SMS_TEMPLATE_WITHOUT_ENOUGH_SPACE_FOR_COMPANY_NAME,
            timeout_str='13:08',
            name='',
            url=url
        )
    assert str(excinfo.value) == 'Space available to company name in SMS message is too small'

