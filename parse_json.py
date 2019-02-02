import json


def parse_json(data):
    # replace all hex codes with ascii
    data = data.replace('\\x7B', '{')
    data = data.replace('\\x7D', '}')
    data = data.replace('\\x3A', ':')
    data = data.replace('\\x22', '"')
    data = data.replace('\\x20', ' ')
    data = data.replace('\\x2B', '+')
    data = data.replace('\\x2D', '-')
    data = data.replace('\\x3C', '<')
    data = data.replace('\\x3E', '>')
    data = data.replace('\\x5B', '[')
    data = data.replace('\\x5D', ']')
    data = data.replace('\\x5C', '\\')
    data = data.replace('\\x26', '&')
    data = data.replace('\\x23', '#')
    data = data.replace('\\x3B', ';')
    data = data.replace('&#039;', "'")

    # dictionary of data
    data = json.loads(data)

    return data

