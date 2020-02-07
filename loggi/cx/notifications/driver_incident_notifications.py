# coding: utf-8
SMS_MAX_LENGTH = 160
MIN_COMPANY_NAME_SIZE = 6


def calculate_company_max_name_size(template, name, timeout_str, url):
    """Calculate the space available for the company_name in the SMS message"""
    msg_without_company_name = template.format(
        self_help_timeout=timeout_str,
        shared_short_url=url,
        company_name='',
        name=name,
    )
    max_name_size = SMS_MAX_LENGTH - len(msg_without_company_name)
    if max_name_size < MIN_COMPANY_NAME_SIZE:
        raise Exception('Space available to company name in SMS message is too small')

    return max_name_size
