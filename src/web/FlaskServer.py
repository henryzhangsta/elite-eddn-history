from flask import *
from db import GetCommodityUpdatesSince
import struct

app = Flask('Flask')
app.debug = True

@app.route('/api/v<int:apiversion>/update/<int:timestamp>', methods=['GET', 'POST'])
def get_updates(apiversion, timestamp=None):
    if request.method == 'GET':
        data = ''
        items = GetCommodityUpdatesSince(timestamp)

        for i in items:
            data += struct.pack('!l', len(i)) + i

        return data