import os


def key_exists(key: str, config: object):
    return key in config


def key_not_exists(key: str, config: object):
    return key not in config


def str_to_bool(var: str) -> bool:
    return True if var == 'True' else False


def env(var: str):
    value = os.environ.get(var)

    if value.capitalize() == 'True' or value.capitalize() == 'False':
        return str_to_bool(value.capitalize())
    return value
