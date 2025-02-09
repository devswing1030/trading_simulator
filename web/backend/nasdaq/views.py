import json

from django.http import HttpResponse
from django.shortcuts import render

from nasdaq.models import Snapshot


def index(request):
    return render(request, 'nasdaq/index.html')

def topN(request):
    result = Snapshot.objects.all()
    # generate json
    symbols = []
    for r in result:
        symbols.append({
            'symbol': r.symbol,
            'name': r.name,
            'bid_px': r.bid_px,
            'bid_qty': r.bid_qty,
            'ask_px': r.ask_px,
            'ask_qty': r.ask_qty,
            'last_px': r.last_px,
            'volume': r.volume,
            'close_px': r.close_px,
            'market_status': r.market_status,
            'timestamp': r.timestamp
        })
    return HttpResponse(json.dumps({'data': symbols}), content_type="application/json")

