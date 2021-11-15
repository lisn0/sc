import rfoo

class MyHandler(rfoo.BaseHandler):
    def __init__(self, handler, conn):
        self._handler = handler
        self._conn = conn
        self._buffer = ''
        self._counter = 0
        self._server = rfoo.Server(self._handler)
        self._methods = {}

    def add(self, a, b):
        return a + b
    # TODO add exersice 3.1


rfoo.InetServer(MyHandler).start()  # "Start server - depratcated."""
# https://github.com/aaiyer/rfoo/blob/1555bd4eed204bb6a33a5e313146a6c2813cfe91/rfoo/_rfoo.py#L621
