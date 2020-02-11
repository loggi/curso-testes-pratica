from base.utils.phone import format_phone_number
import pytest


@pytest.mark.parametrize(
    'country_code, region_code',
    (
        ('', '11'),
        ('55', '11'),
        ('+55', '11'),
    ),
    ids=(
        'without_country_code',
        'with_country_and_region_codes',
        'country_code_already_with_plus_sign',
    )
)
@pytest.mark.parametrize(
    'primary_phone_number, expected_formatted_phone_number',
    (
        ('32341234', '(11) 3234-1234'),
        ('912341234', '(11) 91234-1234'),
    ),
    ids=(
        '8_digits_number',
        '9_digits_number',
    )
)
def test_format_phone_number_code_variations(
    country_code, region_code,
    primary_phone_number,
    expected_formatted_phone_number,
):
    primary_phone_number = '{country_code}{region_code}{phone_number}'.format(
        country_code=country_code,
        region_code=region_code,
        phone_number=primary_phone_number,
    )

    actual_phone_number = format_phone_number(primary_phone_number)

    assert actual_phone_number == expected_formatted_phone_number


@pytest.mark.parametrize(
    'primary_phone_number, expected_formatted_phone_number',
    (
        ('12341234', '12341234'),
        ('912341234', '91234-1234'),
        (None, None),
    ),
    ids=(
        '8_digits_number',
        '9_digits_number',
        'no_phone_number',
    )
)
def test_format_phone_number_without_any_code(
    primary_phone_number,
    expected_formatted_phone_number,
):
    actual_phone_number = format_phone_number(primary_phone_number)

    assert actual_phone_number == expected_formatted_phone_number


@pytest.mark.parametrize(
    'primary_phone_number, expected_formatted_phone_number',
    (
        ('undefined', None),
        ('+55invalid', None),
    ),
    ids=(
        'phone_number_with_full_strings',
        'phone_number_with_string',
    )
)
def test_format_phone_number_with_invalid_number_should_return_none(
    primary_phone_number,
    expected_formatted_phone_number,
):
    actual_phone_number = format_phone_number(primary_phone_number)

    assert actual_phone_number == expected_formatted_phone_number
