def parse_int(s):
    return int(s)


def parse_float(s):
    return float(s)


def unquote_string(s):
    if s and s[0] not in ["'", "\""]:
        return

    s = s[:-1]
    s = s[1:]

    return s
