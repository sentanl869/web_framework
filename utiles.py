from time import (
    localtime,
    strftime,
)


def formatted_time() -> str:
    time_format = '%Y/%m/%d %H:%M:%S'
    value = localtime()
    formatted = strftime(time_format, value)
    return formatted


def log(*args, **kwargs):
    print(formatted_time(), *args, **kwargs)
