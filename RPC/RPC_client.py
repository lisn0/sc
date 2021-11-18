import rfoo


# TODO handle exceptions 'Si la connexion ne se passe pas bien'
handler = rfoo.InetConnection().connect()  # [host=host , port=port] in case the server in another machine
#https://github.com/aaiyer/rfoo/blob/1555bd4eed204bb6a33a5e313146a6c2813cfe91/rfoo/_rfoo.py#L628

proxy = rfoo.Proxy(handler)
a = proxy.add(1, 5)
print(a)
a = proxy.mult(1, 5)
print(a)
a = proxy.diff(1, 5)
print(a)
a = proxy.quotient(1, 0)
print(a)
a = proxy.absolue(-5)
print(a)
handler.close()
