# coding: utf-8

RESOLVER_RATING_TO_DRIVER_CALL_CODE = 'driver_incident.driver_call_rating'

RESPONSE_RATING_TO_DRIVER_CALL_GOOD = 'BOA'
RESPONSE_RATING_TO_DRIVER_CALL_BAD = 'RUIM'
WHATSAPP_RATINGS_REPLY_GOOD = \
    'Que bom, {first_name}. Ficamos felizes que a sua experiência tenha sido boa.\n\n' \
    'Obrigada por nos ajudar, respondendo à pesquisa. :blue_heart:'


WHATSAPP_RATINGS_REPLY_BAD = \
    'Poxa, {first_name}, ' \
    'a gente sente muito que a experiência de ligação não tenha sido boa.\n\n' \
    'Vamos trabalhar por aqui para melhorar esse ponto.\n\n' \
    'Obrigada por nos ajudar, respondendo à pesquisa. :blue_heart:'

WHATSAPP_RATINGS_REPLY_DONT_UNDERTAND = \
    'Eita, a gente não conseguiu entender a sua resposta. :thinking_face:\n\n' \
    'Digite *BOA*, se correu tudo bem durante a ligação.\n\n' \
    'Ou mande *RUIM*, se você não teve uma boa experiência.\n\n' \
    '---\n' \
    ':point_right:Essa é uma mensagem automática. ' \
    'Para nos contar sua experiência, é preciso digitar uma das duas palavras ' \
    'que estão acima em negrito.'


WHATSAPP_RATINGS = {
    RESOLVER_RATING_TO_DRIVER_CALL_CODE: {
        RESPONSE_RATING_TO_DRIVER_CALL_GOOD: WHATSAPP_RATINGS_REPLY_GOOD,
        RESPONSE_RATING_TO_DRIVER_CALL_BAD: WHATSAPP_RATINGS_REPLY_BAD,
    }
}


class Recipient(object):
    def __init__(self, first_name):
        self.first_name = first_name


def whatsapp_rating_reply_message(intention, response, recipient):

    if intention in WHATSAPP_RATINGS:
        reply_message = WHATSAPP_RATINGS.get(intention).get(response)
        if reply_message:
            return reply_message.format(first_name=recipient.first_name)

    return WHATSAPP_RATINGS_REPLY_DONT_UNDERTAND
