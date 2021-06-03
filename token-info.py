import urllib.request as urllib
import json
import requests
from enum import Enum
import dateutil.parser as parser

class DeltaTime(Enum):
    H24 = 1440
    H12 = 1440
    H4 = 4*60
    H2 = 2*60
    H1 = 60

    def __new__(cls, value):
        member = object.__new__(cls)
        member._value_ = value
        return member

    def __int__(self):
        return self.value



def get_cotract_txs(api_token: str, token_address:str = "0x4D5eCA1e4FE912904544043feCEB6858DDd3d866"):


    url = f"https://api.bscscan.com/api?module=account&action=txlist&address={token_address}&startblock=1&endblock=99999999&sort=asc&apikey={api_token}"

    response = urllib.urlopen(url)

    data = json.loads(response.read())
    data_clean = [{
        'blockNumber' : tx['blockNumber'],
        'timeStamp' : tx['timeStamp'],
        'hash' : tx['hash'],
        'from' : tx['from'],
    } for tx in data['result']]
    return data_clean

def get_cotract_internal_txs_bep20(api_token: str, token_address:str = "0x4D5eCA1e4FE912904544043feCEB6858DDd3d866"):

    #&page=1&offset=100
    url = f"https://api.bscscan.com/api?module=account&action=tokentx&contractaddress={token_address}&sort=asc&apikey={api_token}"

    response = urllib.urlopen(url)

    data = json.loads(response.read())
    print
    data_clean = [{
        'blockNumber' : tx['blockNumber'],
        'timeStamp' : tx['timeStamp'],
        'hash' : tx['hash'],
        'from' : tx['from'],
    } for tx in data['result']]
    return data_clean

def get_candles_poo_coin(base_token: str = "0x375483cfa7fc18f6b455e005d835a8335fbdbb1f", minute_window:int = DeltaTime.H1, init_time_str: str = "2021-04-30T19:35:00.000Z", end_time_str = "2021-06-03T19:35:00.000Z"):
    init_time = parser.parse(init_time_str).isoformat() 
    end_time = parser.parse(end_time_str).isoformat()
    
    
    url = "https://chartdata.poocoin.app/"

    payload = {
        "query":'''query GetCandleData(
            $baseCurrency: String!,
            $since: ISO8601DateTime,
            $till: ISO8601DateTime,
            $quoteCurrency: String!,
            $exchangeAddresses: [String!]
            $minTrade: Float
            $window: Int) 
            {
                ethereum(network: bsc) {
                    dexTrades(
                        options: {asc: \"timeInterval.minute\"}
                        date: {since: $since, till: $till}
                        exchangeAddress: {in: $exchangeAddresses}
                        baseCurrency: {is: $baseCurrency}
                        quoteCurrency: {is: $quoteCurrency} # WBNB
                        tradeAmountUsd: {gt: $minTrade}
                    ) 
                    {
                        timeInterval {
                            minute(count: $window, format: \"%Y-%m-%dT%H:%M:%SZ\")
                        }
                        baseCurrency {symbol address}
                        quoteCurrency {symbol address}
                                
                        tradeAmount(in: USD)
                        trades: count quotePrice
                        maximum_price: quotePrice(calculate: maximum)
                        minimum_price: quotePrice(calculate: minimum)
                        open_price: minimum(of: block, get: quote_price)
                        close_price: maximum(of: block, get: quote_price)
                    }
                }
            }''',
        "variables":
            {"baseCurrency":base_token,
            "quoteCurrency":"0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c",
            "since":init_time,
            "till":end_time,
            "window":int(minute_window),
            "exchangeAddresses":["0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73"],
            "minTrade":10}
        }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    return json.loads(response.text)


#WIP
#print([tx['hash']  for tx in get_cotract_internal_txs_bep20()])
#print([tx['hash'] if tx['from'] == "0x1085c0c13c0a6e5b3b1e71b4580c9078009fa881" else ""  for tx in get_cotract_internal_txs_bep20()])



