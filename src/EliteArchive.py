#!/usr/bin/env python
from eddn import EDDNClient
from schemas import ApplicationIdentifier, StationCommodities
from google.protobuf.text_format import PrintMessage
from dateutil.parser import parse as ParseDate
from db import InsertCommodityUpdate, GetCommodityUpdatesSince
from gevent.pywsgi import WSGIServer
from utils.UnixTime import *
import web
import zlib, sys

def CreateCommodityUpdate(data):
    header = data['header']
    payload = data['message']

    msg = StationCommodities()
    msg.timestamp = GetUnixTime(ParseDate(payload['timestamp']))
    msg.system = payload['systemName']
    msg.station = payload['stationName']

    commodity = msg.commodities.add()
    commodity.operation = StationCommodities.CommodityInfo.Operation.Value('ADD')
    commodity.item_name = payload['itemName']
    commodity.buy_price = payload['buyPrice']
    commodity.sell_price = payload['sellPrice']
    commodity.station_stock = payload['stationStock']
    commodity.station_demand = payload['demand']
    #commodity.supply_level
    #commodity.demand_level
    #commodity.illegal

    application = msg.application
    application.author = header['uploaderID']
    application.package_name = header['softwareName']
    application.version = header['softwareVersion']
    #application.public_key

    return msg

if __name__ == '__main__':
    eddn = EDDNClient()

    def write(x):
        m = CreateCommodityUpdate(x)
        print InsertCommodityUpdate(m)
        print m
        print len(m.SerializeToString())

    def length(x):
        print len(x)
        print len(zlib.decompress(x))

    eddn.Listen(write, length)
    httpserver = WSGIServer(('', 80), web.Server)
    httpserver.serve_forever()

    timestamp = 0
    while True:
        try:
            line = raw_input()
            if len(line):
                timestamp = int(line)
            
            print 'timestamp: %d' % timestamp
            updates = GetCommodityUpdatesSince(timestamp)
            for u in updates:
                a = StationCommodities()
                a.ParseFromString(u)
                print a

            if not len(line):
                timestamp = GetCurrentUnixTime()
        except EOFError as e:
            while True:
                try:
                    eddn.Join(1)
                except KeyboardInterrupt:
                    print 'Exiting...'
                    sys.exit(0)
        except Exception as e:
            print e

