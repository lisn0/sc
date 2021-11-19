import rfoo


class Calcul(rfoo.BaseHandler):
    def __init__(self, handler, conn):
        self._handler = handler
        self._conn = conn
        self._buffer = ''
        self._counter = 0
        self._server = rfoo.Server(self._handler)
        self._methods = {}

    def add(self, a, b):
        return a + b

    def mult(self, a, b):
        return a * b

    def diff(self, a, b):
        return b - a

    def quotient(self, a, b):
        return (a / b) if b != 0 else 'error'

    def absolue(self, a):
        return abs(a)


if __name__ == '__main__':
    port = 52431
    rfoo.InetServer(Calcul).start(host='', port=port)  # "Start server - depratcated."""
    # https://github.com/aaiyer/rfoo/blob/1555bd4eed204bb6a33a5e313146a6c2813cfe91/rfoo/_rfoo.py#L621
