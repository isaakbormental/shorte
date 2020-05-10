from string import ascii_letters, digits

ALPHANUMERIC = ascii_letters + digits


def encode_to_base62(number: int) -> str:
    string = ''
    while number > 0:
        string += ALPHANUMERIC[number % 62]
        number = number // 62
    return string[::-1]
