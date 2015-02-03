import pymongo
from pymongo import MongoClient
from bson import Binary

client = MongoClient()
db = client.EliteDataArchive
col_updates = db.updates
col_commodities = db.station_commodities

def InsertCommodityUpdate(data):
    return col_updates.insert({
        'timestamp': data.timestamp,
        'payload': Binary(data.SerializeToString())
    })

def GetCommodityUpdatesSince(timestamp):
    return [x['payload'] for x in col_updates.find({'timestamp': {'$gte': timestamp}}, limit=1000).sort('_id', pymongo.ASCENDING)]