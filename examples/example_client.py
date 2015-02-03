from google.protobuf.text_format import PrintMessage
from struct import Struct
from schemas import StationCommodities
import requests

long_encoded = Struct('!l')
GetLen = lambda x: long_encoded.unpack(x[0:4])[0]

SERVER = 'http://elite.servers.henryzh.com'

def GetData(timestamp):
    data = requests.get(SERVER + '/api/v0/update/%d' % timestamp).content

    unpacked_data = []

    while len(data) > 0:
        l = GetLen(data)

        item = StationCommodities()
        item.ParseFromString(data[4:4+l])
        unpacked_data.append(item)
        data = data[4+l:]

    return unpacked_data

if __name__ == '__main__':
    for i in GetData(0)[:10]:
        print i