#!/usr/bin/env python
# Warning: Don't use this in production.

from databox import Client
from db import *
from time import sleep
import itertools

class Streamer(object):
    databox_client = Client
    delay = 10

    def __init__(self, db_name, db_user, databox_push_token, delay=10):
        self.delay = delay

        db_proxy.initialize(MySQLDatabase(
            db_name,
            user=db_user
        ))

        self.databox_client = Client(token=databox_push_token)

    def observe_and_stream(self):
        max_id = Stock.max_id()
        while True:
            new_max_id = Stock.max_id()
            if new_max_id > max_id:
                if self.stream_records_from(max_id):
                    print "Inserted new records from %d,..." % max_id
                    max_id = new_max_id
                else:
                    print "Error inserting batch!"
            else:
                print "Nothing to do. Sleeping,..."

            sleep(self.delay)

    def stream_records_from(self, min_id):
        print "Streaming from %d" % min_id

        kpis = [stock.kpis for stock in Stock.select() \
            .where(Stock.id > min_id) \
            .order_by(Stock.id.asc())]

        flat_kpis = list(itertools.chain.from_iterable(kpis))
        return self.databox_client.insert_all(flat_kpis)


if __name__ == '__main__':

    s = Streamer("databox_example", "root", "adxg1kq5a4g04k0wk0s4wkssow8osw84")
    s.observe_and_stream()
