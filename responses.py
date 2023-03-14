def handle_response(message) -> str:

    if message == 'hello':
        return 'Hey there !'

    if message == '!help':
        return "`Vous avez besoin d'aide... je suis là !`"

    if message == "benji ?":
        return 'benji stop tes ui ui !'

    if message.endswith('quoi') or message.endswith('quoi ?'):
        return 'feur'

