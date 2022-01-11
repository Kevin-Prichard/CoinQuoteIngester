#!/usr/bin/env python3

import functools
import json
import sys
import time

import requests
import sqlite3

from config import *

BASE_URI = """
https://min-api.cryptocompare.com/data/price?fsym={from_curr}&tsyms={to_curr}"""

CURRENCY_QUOTE_SQL = """
CREATE TABLE IF NOT EXISTS coinquote_{from_curr}_{to_curr} (
    ts INTEGER NOT NULL,
    price REAL NOT NULL
)"""


CURRENCY_INSERT_SQL = """
INSERT INTO coinquote_{from_curr}_{to_curr}
(ts, price) VALUES ({ts}, {price})"""


@functools.lru_cache
def fstring(t, **kwargs):
    return t.format(**kwargs)


def get_db_conn(from_curr, to_curr):
    db_conn = sqlite3.connect(
        database=fstring("{DB_PATH}/coinquote_{from_curr}_"
                         "{to_curr}.sqlite",
                         DB_PATH=DB_PATH,
                         from_curr=from_curr,
                         to_curr=to_curr))
    db_conn.execute(fstring(
        CURRENCY_QUOTE_SQL, from_curr=from_curr, to_curr=to_curr))
    return db_conn


def _make_http_request(url, method="GET", post=None, headers=None):
    req = requests.Request(
        method=method,
        url=url,
        headers=headers)
    return requests.Session().send(req.prepare())


def ingest_quote(from_curr, to_curr):
    uri = fstring(BASE_URI, from_curr=from_curr, to_curr=to_curr)
    resp = _make_http_request(uri)
    price = json.loads(resp.content)[to_curr]
    db = get_db_conn(from_curr, to_curr)
    db.execute(fstring(CURRENCY_INSERT_SQL,
                       from_curr=from_curr,
                       to_curr=to_curr,
                       ts=time.time_ns(),
                       price=price))
    db.commit()


if __name__ == '__main__':
    ingest_quote(sys.argv[1], sys.argv[2])
