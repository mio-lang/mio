from subprocess import check_output


version = None


def build_version():
    return check_output(["hg", "id", "-i"]).strip().rstrip("+")


if version is None:
    version = build_version()
