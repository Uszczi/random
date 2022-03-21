import base64


def basic_auth_str(username):
    """
    Basic auth string
    """
    return 'Basic ' + base64.b64encode(('%s:' % username).encode('latin1')).strip().decode('latin1')


if __name__ == "__main__":
    import sys

    key = basic_auth_str(sys.argv[1])
    print(key)
