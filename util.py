import requests
from hashlib import sha512
import random

def get_price(ticker):
    iex_base = "https://api.iex.cloud/v1/data/CORE/IEX_TOPS/"
    quote_endpoint = iex_base + "{}?token="
    # TODO: get token
    token = "pk_5a751015049443ac85c68c5c25a71fd9"
    response = requests.get(quote_endpoint.format(ticker) + token)
    print(response.json()[0])
    data = response.json()[0]['lastSalePrice']
    peRatio = response.json()[0]['lastSaleTime']
    company = response.json()[0]['sector']
    symbol = response.json()[0]['symbol']
    market = response.json()[0]['volume']
    return [company,symbol,data,peRatio,market] 

def hash_pass(password, salt="SALT"):
    new_pw = password + salt
    hashed_pw = sha512(new_pw.encode()).hexdigest()
    return hashed_pw

def generate_key(length=15):
    seed = (str(random.random()) + str(random.random())).encode()
    hashed_output = sha512(seed).hexdigest()
    return hashed_output[:length]

def get_price_of_ticker(ticker):
    iex_base = "https://api.iex.cloud/v1/data/CORE/IEX_TOPS/"
    quote_endpoint = iex_base + "{}?token="
    # TODO: get token
    token = "pk_5a751015049443ac85c68c5c25a71fd9"
    response = requests.get(quote_endpoint.format(ticker) + token)
    print(response.json()[0])
    data = response.json()[0]['lastSalePrice']
    return data

# def rec(ticker):
#     end= "https://sandbox.iexapis.com/stable/stock/{}/recommendation-trends?token=tsk_bc007805b9a3487db96520c1baac3a07"
#     response = requests.get(end.format(ticker))
#     data = response.json()
#     new_data=data['ratingBuy']
#     return new_data

def chart(ticker):
  dates = []
  prices =[]
  quote_endpoint =("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&outputsize=compact&apikey=74MPQ68EA8UASL2C")
  response = requests.get(quote_endpoint.format(ticker))
  data = response.json()['Time Series (Daily)']
  for i in data:
    dates.append(i)
    prices.append(data[i]['1. open'])
  return dates,prices

def usd_chart():
  dates = []
  prices =[]
  quote_endpoint =("https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=EUR&to_symbol=USD&outputsize=compact&apikey=74MPQ68EA8UASL2C")
  response = requests.get(quote_endpoint)
  data = response.json()['Time Series FX (Daily)']
  for i in data:
    dates.append(i)
    prices.append(data[i]['1. open'])
  return dates,prices


def crypto_chart(ticker):
  dates = []
  prices =[]
  quote_endpoint =("https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={}&market=USD&apikey=74MPQ68EA8UASL2C")
  response = requests.get(quote_endpoint.format(ticker))
  data = response.json()['Time Series (Digital Currency Daily)']
  for i in data:
    dates.append(i)
    prices.append(data[i]['1b. open (USD)'])
  return dates,prices

def seven_day_crypto_chart(ticker):
  dates = []
  prices =[]
  quote_endpoint =("https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={}&market=USD&apikey=74MPQ68EA8UASL2C")
  response = requests.get(quote_endpoint.format(ticker))
  data = response.json()['Time Series (Digital Currency Daily)']
  for i in data:
    dates.append(i)
    prices.append(data[i]['1b. open (USD)'])
  return dates[:7],prices[:7]

def crypto_news():
  articles =[]
  quote_endpoint =("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
  response = requests.get(quote_endpoint)
  data = response.json()
  for article in data['Data']:
    articles.append(article)
  return articles[-10:]

def crypto_stats(ticker):
  quote_endpoint =("https://www.alphavantage.co/query?function=CRYPTO_RATING&symbol={}&apikey=74MPQ68EA8UASL2C")
  response = requests.get(quote_endpoint.format(ticker))
  end = response.json()['Crypto Rating (FCAS)']
  name = end['2. name']
  rating = end['3. fcas rating']
  score = end['4. fcas score']
  market = end['6. market maturity score']
  utlity = end['7. utility score']
  return name,rating,score,market,utlity

import requests

def Gemini_volume():
  solutions =[]
  quote_endpoint =("https://min-api.cryptocompare.com/data/exchange/top/volume?e=Gemini&direction=TO")
  response = requests.get(quote_endpoint)
  data = response.json()
  print(data['Data'])
  for i in data['Data']:
    solutions.append(i)
  return solutions

def Coinbase_volume():
  solutions =[]
  quote_endpoint =("https://min-api.cryptocompare.com/data/exchange/top/volume?e=Coinbase&direction=TO")
  response = requests.get(quote_endpoint)
  data = response.json()
  print(data['Data'])
  for i in data['Data']:
    solutions.append(i)
  return solutions

def Binance_volume():
  solutions =[]
  quote_endpoint =("https://min-api.cryptocompare.com/data/exchange/top/volume?e=Binance&direction=TO")
  response = requests.get(quote_endpoint)
  data = response.json()
  print(data['Data'])
  for i in data['Data']:
    solutions.append(i)
  return solutions


def crypto_market_cap():
  solutions =[]
  quote_endpoint =("https://min-api.cryptocompare.com/data/top/mktcapfull?limit=10&tsym=USD")
  response = requests.get(quote_endpoint)
  data = response.json()
  for i in data['Data']:
    solutions.append(i['CoinInfo'])
  return solutions[:5]


def Crypto (ticker):
  quote_endpoint =("https://min-api.cryptocompare.com/data/price?fsym={}&tsyms=USD")
  response = requests.get(quote_endpoint.format(ticker))
  data = response.json()['USD']
  return data

# def stock_description(ticker):
#   quote_endpoint =("https://cloud.iexapis.com/stable/stock/{}/company?token=pk_bc007805b9a3487db96520c1baac3a07")
#   response = requests.get(quote_endpoint.format(ticker))
#   desc = response.json()['description']
#   ceo = response.json()['CEO']
#   empl = response.json()['employees']
#   industry = response.json()['industry']
#   state = response.json()['state']
#   city = response.json()['city']
#   sector = response.json()['sector']
#   return [desc,ceo,empl,industry,state,city,sector]

# def stats(ticker):
#   quote_endpoint ="https://cloud.iexapis.com/stable/stock/{}/quote?token=pk_bc007805b9a3487db96520c1baac3a07"
#   response = requests.get(quote_endpoint.format(ticker))
#   high = response.json()['week52High']
#   return high

# def related_Companies(ticker):
#   quote_endpoint ="https://cloud.iexapis.com/stable//stock/{}/news/last?token=pk_bc007805b9a3487db96520c1baac3a07"
#   response = requests.get(quote_endpoint.format(ticker))
#   related = response.json()
#   return related[-1:]

# def Logo(ticker):
#   quote_endpoint ="https://cloud.iexapis.com/stable/stock/{}/logo?token=pk_bc007805b9a3487db96520c1baac3a07"
#   response = requests.get(quote_endpoint.format(ticker))
#   logo = response.json()['url']
#   return logo

def Crypto_Exchange_Data():
  quote_endpoint =("https://min-api.cryptocompare.com/data/exchanges/general")
  response = requests.get(quote_endpoint)
  data = response.json()['Data']
  gemini = data['13228']
  binance = data['283442']
  Coinbase = data['2493']
  Kraken = data['2439']
  bitstamp = data['2431']
  return gemini,binance,Coinbase,Kraken,bitstamp

def crypto_coins():
  quote_endpoint =("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,XRP,BCH,LTC,ZEC,ADA,XLM,DOT,LINK,BSV,EOS,XMR,TRX,NEO,AAVE,MKR,SNX,UMA&tsyms=USD")
  response = requests.get(quote_endpoint)
  data = response.json()['RAW']
  btc = data['BTC']['USD']
  eth = data['ETH']['USD']
  xrp = data['XRP']['USD']
  bch = data['BCH']['USD']
  zec = data['ZEC']['USD']
  ltc = data['LTC']['USD']
  ada = data['ADA']['USD']
  DOT = data['DOT']['USD']
  xlm = data['XLM']['USD']
  link = data['LINK']['USD']
  bsv = data['BSV']['USD']
  eos =data['EOS']['USD']
  xmr =data['XMR']['USD']
  trx =data['TRX']['USD']
  neo = data['NEO']['USD']
  mkr = data['MKR']['USD']
  aave = data['AAVE']['USD']
  snx = data['SNX']['USD']
  uma = data['UMA']['USD']
  return btc,eth,xrp,bch,zec,ltc,ada,DOT,xlm,link,bsv,eos,xmr,trx,neo,mkr,aave,snx,uma

# def stats_low(ticker):
#   quote_endpoint ="https://cloud.iexapis.com/stable/stock/{}/quote?token=pk_bc007805b9a3487db96520c1baac3a07"
#   response = requests.get(quote_endpoint.format(ticker))
#   low = response.json()['week52Low']
#   return low

def tracking_chart(ticker):
  dates = []
  prices =[]
  quote_endpoint =("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=60min&outputsize=compact&apikey=74MPQ68EA8UASL2C")
  response = requests.get(quote_endpoint.format(ticker))
  data = response.json()['Time Series (60min)']
  for i in data:
    dates.append(i)
    prices.append(data[i]['1. open'])
  return dates[:15],prices[:15]

def chart(ticker):
  dates = []
  prices =[]
  quote_endpoint =("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&outputsize=compact&apikey=74MPQ68EA8UASL2C")
  response = requests.get(quote_endpoint.format(ticker))
  data = response.json()['Time Series (Daily)']
  for i in data:
    dates.append(i)
    prices.append(data[i]['1. open'])
  return dates,prices
  
  

# def pe_ratio(ticker):
#   quote_endpoint ="https://cloud.iexapis.com/stable/stock/{}/quote?token=pk_bc007805b9a3487db96520c1baac3a07"
#   response = requests.get(quote_endpoint.format(ticker))
#   ratio = response.json()['peRatio']
#   return ratio

# def ytd_change(ticker):
#   quote_endpoint ="https://cloud.iexapis.com/stable/stock/{}/quote?token=pk_bc007805b9a3487db96520c1baac3a07"
#   response = requests.get(quote_endpoint.format(ticker))
#   ratio = response.json()['ytdChange']
#   return ratio

def top_gainers():
  end = ("https://financialmodelingprep.com/api/v3/gainers?apikey=8db666fce01a371b534ff479f0d23295")
  res = requests.get(end)
  data = res.json()
  output = []
  for i in data:
    output.append(i)
  return output[:5]

def top_losers():
  end = ("https://financialmodelingprep.com/api/v3/losers?apikey=8db666fce01a371b534ff479f0d23295")
  res = requests.get(end)
  data = res.json()
  output = []
  for i in data:
    output.append(i)
  return output[:5]
  
  

# def day_change(ticker):
#   quote_endpoint ="https://cloud.iexapis.com/stable/stock/{}/quote?token=pk_bc007805b9a3487db96520c1baac3a07"
#   response = requests.get(quote_endpoint.format(ticker))
#   change = response.json()['change']
  
#   return change

# def chart(ticker):
#   dates = []
#   open_price = []
#   end =  "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&outputsize=compact&apikey=74MPQ68EA8UASL2C"
#   response = requests.get(end.format(ticker))
#   low = response.json()['Time Series (Daily)']
#   for key in low:
#     dates.append(key)
#     # example = low[key]['1. open']
#     # open_price.append(example)
#   return dates


if __name__=="__main__":
    from pprint import pprint
    pprint(get_price("ibm"))
    print(hash_pass("password"))
