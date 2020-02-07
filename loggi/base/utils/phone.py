# coding: utf-8
import re
import phonenumbers

_phone_regex = re.compile(r'\D')


def normalize_phone_number(phone):
    if not phone:
        return None
    return _phone_regex.sub('', phone)


def format_phone_number(phone_number):
    """Format phone number of Brazilian region codes for human readers.
    Example:
        With country and region code
        >>> _format_phone_number('+5511912341234')
         '(11) 91234-1234'
        >>> _format_phone_number('5511912341234')
         '(11) 91234-1234'

        Without country code
        >>> _format_phone_number('11912341234')
         '(11) 91234-1234'

        Without country and region code
        >>> _format_phone_number('912341234')
         '91234-1234'
    :param phone_number (str): A phone number with or without region codes
    :return (str): A nicely formatted phone number
    """
    if not phone_number:
        return phone_number

    phone_number = normalize_phone_number(phone_number)
    has_bra_country_code = phone_number.startswith('55')
    phone = '{}{}'.format('+' if has_bra_country_code else '+55', phone_number)

    try:
        phone_parsed = phonenumbers.parse(phone)

        return phonenumbers.format_in_original_format(phone_parsed, 'BRA')
    except phonenumbers.NumberParseException:
        return None