from peewee import *
import time

db_proxy = Proxy()


class BaseModel(Model):
    class Meta:
        database = db_proxy

class Stock(BaseModel):
    class Meta:
        db_table = "stocks"

    ticker = CharField(max_length=10)
    granularity = CharField(max_length=3)
    mdate = DateField(formats='%Y-%m-%d')
    open = DoubleField()
    high = DoubleField()
    low = DoubleField()
    close = DoubleField()
    volume = IntegerField()
    adj_close = DoubleField()

    @staticmethod
    def max_id():
        return Stock.select(
            fn.Max(Stock.id)
        ).scalar(as_tuple=False, convert=True)

    @property
    def kpis(self):
        return [{
                    'key': ".".join(["stock", self.ticker, f]),
                    'value': v,
                    'date': self.mdate.strftime("%Y-%m-%d 12:00:00")
                } for f, v in self._data.iteritems() if f not in ["id", "mdate", "ticker", "granularity"]]