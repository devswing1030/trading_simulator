from django.db import models

# Create your models here.

class Snapshot(models.Model):
    symbol = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    bid_px = models.CharField(max_length=20)
    bid_qty = models.CharField(max_length=20)
    ask_px = models.CharField(max_length=20)
    ask_qty = models.CharField(max_length=20)
    last_px = models.CharField(max_length=20)
    volume = models.CharField(max_length=20)
    close_px = models.CharField(max_length=20)
    market_status = models.CharField(max_length=20)
    timestamp = models.CharField(max_length=20)

