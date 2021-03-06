import zlib, zmq, json, sys, threading

class EDDNClient(object):
    def __init__(self):
        self.context = zmq.Context()

    def Listen(self, callback, debug=None):
        if not callback:
            raise Exception('No callback specified.')

        subscriber = self.context.socket(zmq.SUB)
        subscriber.setsockopt(zmq.SUBSCRIBE, "")
        subscriber.connect('tcp://eddn-relay.elite-markets.net:9500')

        poller = zmq.Poller()
        poller.register(subscriber, zmq.POLLIN)

        def Worker():
            while True:
                socks = dict(poller.poll())
                if subscriber in socks and socks[subscriber] == zmq.POLLIN:
                    raw_data = subscriber.recv()

                    try:
                        if debug:
                            debug(raw_data)

                        market_json = zlib.decompress(raw_data)
                        market_data = json.loads(market_json)
                        callback(market_data)
                    except Exception as e:
                        sys.stderr.write('%s\n', str(e))

        self.thread = threading.Thread(target=Worker)
        self.thread.daemon = True
        self.thread.start()

    def Join(self, *args):
        self.thread.join(*args)
