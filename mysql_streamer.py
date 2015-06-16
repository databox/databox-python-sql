#!/usr/bin/env python
# -*- coding: utf-8 -*-

from databox import Client
from db import *
from time import sleep
import itertools
from sys import stderr
import argparse


class Streamer(object):
    databox_client = Client
    delay = 10

    def __init__(self, db_name, db_user, databox_push_token, delay=10):
        self.delay = delay

        db_proxy.initialize(MySQLDatabase(db_name, user=db_user))
        self.databox_client = Client(token=databox_push_token)

    def observe_and_stream(self):
        """Function will start infinitive loop that will retrive biggest id from
        stocks table. If will compare that id with current biggest id. If its bigger
        it will stream new records from old biggest id on."""

        max_id = Stock.max_id()
        while True:
            new_max_id = Stock.max_id()
            if new_max_id > max_id:
                if self.stream_records_from(max_id):
                    print "Inserted new records from %d,..." % max_id
                    max_id = new_max_id
                else:
                    print >>stderr, "Error inserting batch!"
            else:
                print "Nothing to do. Sleeping,..."

            sleep(self.delay)

    def stream_records_from(self, min_id):
        """Selects IDs bigger than min_id and converts them into KPIs.
        Converted KPIs are then pushed to Databox with helo of Databox
        Python SDK."""

        print "Streaming from %d" % min_id

        kpis = [stock.kpis for stock in Stock.select() \
            .where(Stock.id > min_id) \
            .order_by(Stock.id.asc())]

        flat_kpis = list(itertools.chain.from_iterable(kpis))
        return self.databox_client.insert_all(flat_kpis)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Streaming MySQL → Databox')
    parser.add_argument('database', metavar='database', type=str)
    parser.add_argument('-u', required=True, metavar='mysql_user', type=str, help="MySQL user")
    parser.add_argument('-t', required=True, metavar='push_token', type=str, help="Databox push token")

    args = parser.parse_args()
    options = vars(args)

    Streamer(options['database'], options['u'], options['t']).observe_and_stream()
