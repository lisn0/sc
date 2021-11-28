import rfoo


if __name__ == '__main__':
    handler = rfoo.InetConnection().connect()
    proxy = rfoo.Proxy(handler)
    print(proxy.add(15, 20))
    handler.close()
