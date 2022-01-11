# CoinQuoteIngester

### Introduction
Ingest coin quotes from min-api.cryptocompare.com, storing them to a local Sqlite database.

Example URL: https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD

Just for fun, meant to build a basic pricing history for TA, and cryptocompare.com provides the quotes for free.

Cryptocompare.com do impose a rate-limit of 50k requests per month per IP. For the four (4) coins I want to track in USD, that means 12500 requests per month per coin, or 410 requests per day (assuming 365.25 days in a year.) One request each five minutes works out to 288 requests per day, which is enough data for my TA needs, and I run this script from cron.

The script is meant to be run from a cron-like invoker, as it fetches a single coin quote per invocation.

### Installation
After forking/cloning the repo-

1. Create a virtual environment:
```
$ python3 -m venv .venv
```
2. Activate the venv
```
$ . .venv/bin/activate
```
3. Install dependencies
```
(env) $ pip install -r requirements
```
4. Edit config.py to change DB_PATH to point at wherever you've chosen to store your Sqlite files.

### Usage
The script captures a single quote, for a given coin, valued at a given currency's (assumed) current price. 
```
$ ./ingester.py BTC USD
```

No output means all went well. Probably. Run it a few times manually, and perform a SELECT to see whether records were, in fact, inserted.

I use vanilla cron to run the script every five minutes of the day.
