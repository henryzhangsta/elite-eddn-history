#!/usr/bin/env python
from eddn import EDDNClient
from schemas import ApplicationIdentifier, StationCommodities
from google.protobuf.text_format import PrintMessage
from dateutil.parser import parse as ParseDate
from dateutil.tz import tzutc
import zlib, datetime, sys

def GetUnixTime(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    epoch = epoch.replace(tzinfo=tzutc())

    if not dt.tzinfo:
        dt = dt.replace(tzinfo=tzutc())
    else:
        dt = dt.astimezone(tzutc())
    delta = dt - epoch
    return int(delta.total_seconds() * 1000.0)

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
        print m
        print len(m.SerializeToString())

    def length(x):
        print len(x)
        print len(zlib.decompress(x))

    eddn.Listen(write, length)

    while input():
        pass